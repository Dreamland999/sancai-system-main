from __future__ import annotations

import json, hashlib, os, random, sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
if str(PROJECT_ROOT) not in sys.path: sys.path.insert(0, str(PROJECT_ROOT))
if str(BACKEND_DIR) not in sys.path: sys.path.insert(0, str(BACKEND_DIR))

from schemas import FeedbackRequest, FeedbackResponse, OptionsResponse, UserStateRequest

try:
    import torch; import torch.nn.functional as F; TORCH = True
except ImportError: TORCH = False

EMB_DIM = 64; SEED = 42; TOP_K = 3

BODY_TAGS = ['良好','饥饿','饱腹','口渴','疲劳','感觉有点冷','感觉有点热','困倦']
MOOD_TAGS = ['开心','平静','兴奋','低落','烦躁','紧张','无聊','孤单']
SCENE_TAGS = ['家/宿舍','学校/教学楼','图书馆/自习室','办公室/公司','餐厅/食堂','健身房/运动场','咖啡店/奶茶店','商场/商业街','地铁/公交/车站','公园/户外']
FLAVOR_TAGS = ['清爽','奶香','茶香','果香','花香','咖啡香','酸感','甜感','苦感','气泡感']
TEMP_TAGS = ['冷饮','热饮','常温']
LIMIT_TAGS = ['低糖','低刺激','咖啡因敏感慎用','乳糖不耐慎用','过敏风险']

R_BODY,R_MOOD,R_SCENE,R_FLAVOR,R_TEMP,R_LIMIT,R_TYPE = '适配身体状态','适配心情状态','适合场景','感官标签','冷热建议','健康约束','饮品类型'

def ssplit(v): return [t.strip() for t in str(v).replace('，',',').replace('、',',').replace('；',',').split(',') if t.strip()] if v and str(v).strip() not in ('','nan') else []

def prefix_tags(body,mood,scene,flavor,temp,limits,needs=None):
    t=[];
    for v in (body or []):
        if v.strip(): t.append(f'BODY_{v.strip()}')
    for v in (mood or []):
        if v.strip(): t.append(f'MOOD_{v.strip()}')
    for v in (scene or []):
        if v.strip(): t.append(f'SCENE_{v.strip()}')
    for v in (flavor or []):
        if v.strip(): t.append(f'FLAVOR_{v.strip()}')
    for v in (temp or []):
        if v.strip(): t.append(f'TEMP_{v.strip()}')
    for v in (limits or []):
        if v.strip(): t.append(f'LIMIT_{v.strip()}')
    for v in (needs or []):
        if v.strip(): t.append(f'NEED_{v.strip()}')
    return list(dict.fromkeys(t))

def encode(tags, token_to_idx):
    v=np.zeros(len(token_to_idx),dtype=np.float32)
    for t in tags:
        if t in token_to_idx: v[token_to_idx[t]]=1.0
    return v

def health_penalty(user_limits, row):
    p=0.0; lims={t.strip() for t in ssplit(user_limits) if t.strip() if hasattr(user_limits,'__iter__') and not isinstance(user_limits,str)}
    if isinstance(user_limits,list): lims=set(user_limits)
    constraints=ssplit(row.get(R_LIMIT,''))
    if '咖啡因敏感慎用' in lims and any('咖啡因' in c for c in constraints): p+=0.3
    if '乳糖不耐慎用' in lims and any('乳糖' in c or '奶' in c for c in constraints): p+=0.3
    if '低糖' in lims and any('高糖' in c or '控糖' in c for c in constraints): p+=0.3
    if '低刺激' in lims and any('刺激' in c or '慎用' in c for c in constraints): p+=0.15
    if '过敏风险' in lims and any('过敏' in c for c in constraints): p+=0.3
    return min(p,1.0)

def match_reason_line(user, row, field, label, prefix):
    u=set(user or []); r=set(ssplit(row.get(field,'')) if field else [row.get(label,'')])
    inter=u&r
    return f'匹配你的{label}：{"、".join(sorted(inter))}' if inter else ''

def match_reason(user_payload, row):
    lines=[]
    l=match_reason_line(user_payload.body, row, R_BODY, '身体状态','')
    if l: lines.append(l)
    l=match_reason_line(user_payload.mood, row, R_MOOD, '心情状态','')
    if l: lines.append(l)
    l=match_reason_line(user_payload.scene, row, R_SCENE, '场景','')
    if l: lines.append(l)
    l=match_reason_line(user_payload.flavor_preference, row, R_FLAVOR, '感官偏好','')
    if l: lines.append(l)
    l=match_reason_line(user_payload.temperature_preference, row, R_TEMP, '冷热偏好','')
    if l: lines.append(l)
    if user_payload.limits: lines.append(f'已考虑你的健康约束：{"、".join(user_payload.limits)}')
    return '；'.join(lines) if lines else '为你匹配了适合的饮品'

class RecommenderService:
    def __init__(self):
        self.root_dir=Path(__file__).resolve().parents[1]
        self.feedback_path=Path(__file__).resolve().parent/"feedback_log.jsonl"
        self.model_mode="new_tag_rule_scorer"

        recipe_path=self.root_dir/"data"/"饮品方案表_最终检查版.csv"
        self.recipe_df=pd.read_csv(recipe_path,dtype=str,keep_default_na=False,encoding='utf-8-sig')
        self.recipe_rows=[row for _,row in self.recipe_df.iterrows()]
        print(f'[backend] recipes loaded: {len(self.recipe_rows)}')

        vocab_path=self.root_dir/"algorithm"/"twin_tower_vocab.json"
        self.vocab,self.token_to_idx,self.vocab_size,self.vocab_loaded=self._load_vocab(vocab_path)
        if not self.vocab_loaded:
            print('[backend] Warning: vocab not found, using rule scorer only')

        self.twin_model=None; self.ranker_model=None
        if self.vocab_loaded and TORCH:
            twin_path=self.root_dir/"algorithm"/"twin_tower_model.pt"
            self.twin_model=self._load_twin(twin_path,self.vocab_size)
            if self.twin_model:
                self.model_mode="new_twin_tower_rule_rank"
                mlp_path=self.root_dir/"algorithm"/"mlp_ranker_model.pt"
                self.ranker_model=self._load_mlp(mlp_path)
                if self.ranker_model: self.model_mode="new_twin_tower_mlp"

        # precompute recipe embeddings
        self._precompute_recipe_embeddings()

        print(f'[backend] model_mode={self.model_mode} vocab_size={self.vocab_size}')

    def _load_vocab(self,path):
        if not path.exists(): return [],[],0,False
        try:
            p=json.loads(path.read_text('utf-8'))
            v=[str(x) for x in p.get('vocab',[])]
            m={str(k):int(v) for k,v in p.get('token_to_idx',{}).items()}
            s=int(p.get('vocab_size',len(v)))
            return v,m,s,True
        except: return [],[],0,False

    def _load_twin(self,path,vs):
        if not path.exists() or not TORCH: return None
        m=torch.nn.Sequential(torch.nn.Linear(vs,128),torch.nn.ReLU(),torch.nn.Dropout(0.2),torch.nn.Linear(128,EMB_DIM))
        try:
            m.load_state_dict(torch.load(path,map_location='cpu'),strict=True)
            m.eval(); return m
        except Exception as e: print(f'[backend] twin load failed: {e}'); return None

    def _load_mlp(self,path):
        if not path.exists() or not TORCH: return None
        try:
            state=torch.load(path,map_location='cpu')
            w=state.get('0.weight'); input_dim=w.shape[1] if w is not None else 8
            m=torch.nn.Sequential(torch.nn.Linear(input_dim,32),torch.nn.ReLU(),torch.nn.Dropout(0.1),torch.nn.Linear(32,16),torch.nn.ReLU(),torch.nn.Linear(16,1),torch.nn.Sigmoid())
            m.load_state_dict(state,strict=True); m.eval(); return m
        except Exception as e: print(f'[backend] mlp load failed: {e}'); return None

    def _precompute_recipe_embeddings(self):
        self._recipe_embs=[]
        for row in self.recipe_rows:
            tags=prefix_tags(ssplit(row.get(R_BODY,'')),ssplit(row.get(R_MOOD,'')),ssplit(row.get(R_SCENE,'')),ssplit(row.get(R_FLAVOR,'')),ssplit(row.get(R_TEMP,'')),None)
            vec=encode(tags,self.token_to_idx)
            self._recipe_embs.append(vec)

    def recommend(self,payload:UserStateRequest):
        utags=prefix_tags(payload.body,payload.mood,payload.scene,payload.flavor_preference,payload.temperature_preference,payload.limits)
        uvec=encode(utags,self.token_to_idx)

        # Separate user tags by prefix for match computations
        u_body_set=set(payload.body); u_mood_set=set(payload.mood); u_scene_set=set(payload.scene)
        u_flavor_set=set(payload.flavor_preference); u_temp_set=set(payload.temperature_preference)

        candidates=[]
        for i,row in enumerate(self.recipe_rows):
            rvec=self._recipe_embs[i]
            score=0.0
            if self.twin_model and TORCH:
                with torch.no_grad():
                    ue=F.normalize(self.twin_model(torch.tensor(uvec).unsqueeze(0).float()),dim=-1)
                    re=F.normalize(self.twin_model(torch.tensor(rvec).unsqueeze(0).float()),dim=-1)
                    score=(ue*re).sum().sigmoid().item()
            else:
                score=float(np.dot(uvec,rvec)/max(np.linalg.norm(uvec)*np.linalg.norm(rvec),1e-8))

            # Temperature hard filter: user选热饮则只推热饮，以此类推
            r_temp_set=set(ssplit(row.get(R_TEMP,'')))
            if u_temp_set and not (u_temp_set & r_temp_set):
                continue  # 跳过不匹配温度的饮品

            hp=health_penalty(payload.limits,row)
            # Flavor overlap for sort boost
            r_flavor_set=set(ssplit(row.get(R_FLAVOR,'')))
            fm_pre=len(u_flavor_set&r_flavor_set)/max(len(u_flavor_set),1) if u_flavor_set else 0
            candidates.append((i,score,hp,fm_pre))

        # Sort: twin_score + 0.12*flavor_match - 0.8*health_penalty
        candidates.sort(key=lambda x:x[1]+0.12*x[3]-x[2]*0.8,reverse=True)
        top_n=candidates[:TOP_K]

        results=[]
        for idx,sc,hpen,fm_pre in top_n:
            row=self.recipe_rows[idx]
            rtags=prefix_tags(ssplit(row.get(R_BODY,'')),ssplit(row.get(R_MOOD,'')),ssplit(row.get(R_SCENE,'')),ssplit(row.get(R_FLAVOR,'')),ssplit(row.get(R_TEMP,'')),None)
            reason=match_reason(payload,row)

            if self.ranker_model and TORCH:
                u_body=set(payload.body); u_mood=set(payload.mood); u_scene=set(payload.scene)
                u_flavor=set(payload.flavor_preference); u_temp=set(payload.temperature_preference)
                r_body=set(ssplit(row.get(R_BODY,''))); r_mood=set(ssplit(row.get(R_MOOD,'')))
                r_scene=set(ssplit(row.get(R_SCENE,''))); r_flavor=set(ssplit(row.get(R_FLAVOR,'')))
                r_temp=set(ssplit(row.get(R_TEMP,'')))
                bm=len(u_body&r_body)/max(len(u_body),1) if u_body else 0
                mm=len(u_mood&r_mood)/max(len(u_mood),1) if u_mood else 0
                sm=len(u_scene&r_scene)/max(len(u_scene),1) if u_scene else 0
                fm=len(u_flavor&r_flavor)/max(len(u_flavor),1) if u_flavor else 0
                tm=1.0 if (u_temp&r_temp) else 0.0
                nov=0.7; nv=1.0-hpen
                feats=torch.tensor([[sc,bm,mm,sm,fm,tm,nv,nov]],dtype=torch.float32)
                with torch.no_grad(): score=self.ranker_model(feats).item()
                # flavor_boost: 用户明确风味偏好时提升匹配饮品
                if u_flavor and fm > 0:
                    score = min(1.0, score + 0.10 + 0.05 * fm)

            results.append({
                'recipe_id':row.get('recipe_id',''),
                'name':row.get('饮品名称',''),
                'type':row.get(R_TYPE,''),
                'score':round(float(score),4),
                'match_reason':reason,
                'description':row.get('推荐解释',''),
                'polished_text':row.get('推荐解释',''),
                'visual_prompt':row.get('视觉标签',''),
                'visual_mapping':[{'tag':t} for t in ssplit(row.get('视觉标签',''))],
                'sweetness':row.get('甜度建议',''),
                'temperature':row.get(R_TEMP,''),
                'health_notes':ssplit(row.get(R_LIMIT,'')),
            })
        return {'session_id':'SESS_'+hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],'status':{},'avoided_items':[],'pipeline':['new_twin_tower_mlp' if self.ranker_model else 'new_twin_tower'],'model_mode':self.model_mode,'recommendations':results}

    def get_options(self):
        return OptionsResponse(
            scene_options=SCENE_TAGS, body_options=BODY_TAGS, mood_options=MOOD_TAGS,
            need_options=[], limit_options=LIMIT_TAGS, flavor_options=FLAVOR_TAGS, temperature_options=TEMP_TAGS)

    def save_feedback(self,payload:FeedbackRequest):
        try:
            entry=payload.dict(); entry['timestamp']=entry.get('timestamp') or datetime.now().isoformat()
            with self.feedback_path.open('a',encoding='utf-8') as f: f.write(json.dumps(entry,ensure_ascii=False)+'\n')
            return FeedbackResponse(feedback_id='FB_'+hashlib.md5(str(entry).encode()).hexdigest()[:8],status='saved')
        except Exception as e: return FeedbackResponse(status='error',message=str(e))

from datetime import datetime
