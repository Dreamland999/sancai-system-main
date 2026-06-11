"""
重建推荐链路 v2 — 移除TYPE，LIMIT不进双塔
"""
from __future__ import annotations
import json, random, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT=Path(__file__).resolve().parent; DATA_DIR=ROOT.parent/"data"
try:
    import torch; import torch.nn as nn; import torch.nn.functional as F; TORCH=True
except ImportError: TORCH=False

BODY_TAGS=['良好','饥饿','饱腹','口渴','疲劳','感觉有点冷','感觉有点热','困倦']
MOOD_TAGS=['开心','平静','兴奋','低落','烦躁','紧张','无聊','孤单']
SCENE_TAGS=['家/宿舍','学校/教学楼','图书馆/自习室','办公室/公司','餐厅/食堂','健身房/运动场','咖啡店/奶茶店','商场/商业街','地铁/公交/车站','公园/户外']
FLAVOR_TAGS=['清爽','奶香','茶香','果香','花香','咖啡香','酸感','甜感','苦感','气泡感']
TEMP_TAGS=['冷饮','热饮','常温']
LIMIT_TAGS=['低糖','低刺激','咖啡因敏感慎用','乳糖不耐慎用','过敏风险']

R_BODY,R_MOOD,R_SCENE,R_FLAVOR,R_TEMP,R_LIMIT='适配身体状态','适配心情状态','适合场景','感官标签','冷热建议','健康约束'
EMB_DIM=64

def ssplit(v): return [t.strip() for t in str(v).replace('，',',').replace('、',',').replace('；',',').split(',') if t.strip()] if v and str(v).strip() not in ('','nan') else []

def build_vocab():
    tokens=[]
    for t in BODY_TAGS: tokens.append(f'BODY_{t}')
    for t in MOOD_TAGS: tokens.append(f'MOOD_{t}')
    for t in SCENE_TAGS: tokens.append(f'SCENE_{t}')
    for t in FLAVOR_TAGS: tokens.append(f'FLAVOR_{t}')
    for t in TEMP_TAGS: tokens.append(f'TEMP_{t}')
    tokens=sorted(tokens); return tokens,{t:i for i,t in enumerate(tokens)}

def encode(ts,t2i):
    v=np.zeros(len(t2i),dtype=np.float32)
    for t in ts:
        if t in t2i: v[t2i[t]]=1.0
    return v

def user_tokens(row,payload=None):
    if payload: return [f'BODY_{t}' for t in payload.body if t.strip()]+[f'MOOD_{t}' for t in payload.mood if t.strip()]+[f'SCENE_{t}' for t in payload.scene if t.strip()]+[f'FLAVOR_{t}' for t in payload.flavor_preference if t.strip()]+[f'TEMP_{t}' for t in payload.temperature_preference if t.strip()]
    return [f'BODY_{t}' for t in ssplit(row.get('身体状态标签',''))]+[f'MOOD_{t}' for t in ssplit(row.get('心情状态标签',''))]+[f'SCENE_{t}' for t in ssplit(row.get('地点/场景',''))]+[f'FLAVOR_{t}' for t in ssplit(row.get('口味偏好',''))]+[f'TEMP_{t}' for t in ssplit(row.get('冷热偏好',''))]

def recipe_tokens(row):
    return list(dict.fromkeys([f'BODY_{t}' for t in ssplit(row.get(R_BODY,''))]+[f'MOOD_{t}' for t in ssplit(row.get(R_MOOD,''))]+[f'SCENE_{t}' for t in ssplit(row.get(R_SCENE,''))]+[f'FLAVOR_{t}' for t in ssplit(row.get(R_FLAVOR,''))]+[f'TEMP_{t}' for t in ssplit(row.get(R_TEMP,''))]))

def hpenalty(ulimits,row):
    p=0.0; lims=set(ulimits) if isinstance(ulimits,list) else set()
    constraints=ssplit(row.get(R_LIMIT,''))
    if '咖啡因敏感慎用' in lims and any('咖啡因' in c for c in constraints): p+=0.3
    if '乳糖不耐慎用' in lims and any('乳糖' in c or '奶' in c for c in constraints): p+=0.3
    if '低糖' in lims and any('高糖' in c or '控糖' in c for c in constraints): p+=0.3
    if '低刺激' in lims and any('刺激' in c or '慎用' in c for c in constraints): p+=0.15
    if '过敏风险' in lims and any('过敏' in c for c in constraints): p+=0.3
    return min(p,1.0)

def main():
    recipe_df=pd.read_csv(DATA_DIR/'饮品方案表_最终检查版.csv',dtype=str,keep_default_na=False,encoding='utf-8-sig')
    user_df=pd.read_csv(DATA_DIR/'用户输入表_最终检查版.csv',dtype=str,keep_default_na=False,encoding='utf-8-sig')
    print(f'[data] recipes={len(recipe_df)} users={len(user_df)}')

    vocab,t2i=build_vocab(); vs=len(vocab)
    cnt={}; [cnt.update({t.split('_')[0]:cnt.get(t.split('_')[0],0)+1}) for t in vocab]
    print(f'[vocab] size={vs} {cnt}')

    with (ROOT/'twin_tower_vocab.json').open('w',encoding='utf-8') as f: json.dump({'vocab':vocab,'token_to_idx':{str(k):int(v) for k,v in t2i.items()},'vocab_size':vs},f,ensure_ascii=False,indent=2)
    print('[vocab] saved')

    # Twin tower training
    if TORCH:
        model=nn.Sequential(nn.Linear(vs,128),nn.ReLU(),nn.Dropout(0.2),nn.Linear(128,EMB_DIM))
        pairs=[]
        for _,ur in user_df.iterrows():
            ut=user_tokens(ur)
            if not ut: continue
            for _,rr in recipe_df.iterrows():
                rt=recipe_tokens(rr)
                s=len(set(ut)&set(rt))/max(len(set(ut)),1) if ut else 0
                pairs.append((ut,rt,s))
        pos=[(u,r) for u,r,s in pairs if s>0.1]; neg=[(u,r) for u,r,s in pairs if s==0][:max(len(pos),10)]
        all_pairs=pos+neg; labels=[1.0]*len(pos)+[0.0]*len(neg)
        print(f'[twin] samples={len(all_pairs)} pos={len(pos)} neg={len(neg)}')
        uv=np.array([encode(u,t2i) for u,_ in all_pairs],dtype=np.float32)
        rv=np.array([encode(r,t2i) for _,r in all_pairs],dtype=np.float32)
        y=torch.tensor(labels).unsqueeze(1); ut=torch.tensor(uv); rt=torch.tensor(rv)
        opt=torch.optim.Adam(model.parameters(),lr=0.005)
        for ep in range(20):
            model.train(); opt.zero_grad()
            ue=F.normalize(model(ut),dim=-1); re=F.normalize(model(rt),dim=-1)
            loss=nn.BCEWithLogitsLoss()((ue*re).sum(-1,keepdim=True)*5.0,y)
            loss.backward(); opt.step()
            if ep%5==0:
                with torch.no_grad():
                    acc=(torch.sigmoid((ue*re).sum(-1,keepdim=True)*5.0)>0.5).float().eq(y).float().mean().item()
                print(f'[twin] ep{ep:3d} loss={loss.item():.4f} acc={acc:.3f}')
        torch.save(model.state_dict(),ROOT/'twin_tower_model.pt'); print('[twin] saved')
        model.eval()

        # MLP: 8 features (no type_bonus)
        feats=[]; targs=[]
        for _,ur in user_df.iterrows():
            ut=user_tokens(ur); ubody=set(ssplit(ur.get('身体状态标签',''))); umood=set(ssplit(ur.get('心情状态标签','')))
            uscene=set(ssplit(ur.get('地点/场景',''))); uflavor=set(ssplit(ur.get('口味偏好',''))); utemp=set(ssplit(ur.get('冷热偏好','')))
            uv=torch.tensor(encode(ut,t2i)).unsqueeze(0).float()
            with torch.no_grad(): uemb=F.normalize(model(uv),dim=-1)
            for _,rr in recipe_df.iterrows():
                rt=recipe_tokens(rr); rbody=set(ssplit(rr.get(R_BODY,''))); rmood=set(ssplit(rr.get(R_MOOD,'')))
                rscene=set(ssplit(rr.get(R_SCENE,''))); rflavor=set(ssplit(rr.get(R_FLAVOR,''))); rtemp=set(ssplit(rr.get(R_TEMP,'')))
                rv=torch.tensor(encode(rt,t2i)).unsqueeze(0).float()
                with torch.no_grad(): remb=F.normalize(model(rv),dim=-1); ts=torch.sigmoid((uemb*remb).sum()*5.0).item()
                bm=len(ubody&rbody)/max(len(ubody),1) if ubody else 0; mm=len(umood&rmood)/max(len(umood),1) if umood else 0
                sm=len(uscene&rscene)/max(len(uscene),1) if uscene else 0; fm=len(uflavor&rflavor)/max(len(uflavor),1) if uflavor else 0
                tm=1.0 if (utemp&rtemp) else 0.0; hp=1.0-hpenalty(ssplit(ur.get('饮食限制','')),rr)
                seed_val=hash(str(rr.get('recipe_id',''))+str(ur.get('session_id','')))%10000; nov=(seed_val/10000.0)*0.3+0.5
                fv=[ts,bm,mm,sm,fm,tm,hp,nov]; targ=ts*0.4+bm*0.15+mm*0.15+fm*0.10+tm*0.10+hp*0.10
                feats.append(fv); targs.append(targ)
        if len(feats)>20:
            X=torch.tensor(feats,dtype=torch.float32); Y=torch.tensor(targs,dtype=torch.float32).unsqueeze(1)
            mlp=nn.Sequential(nn.Linear(8,32),nn.ReLU(),nn.Dropout(0.1),nn.Linear(32,16),nn.ReLU(),nn.Linear(16,1),nn.Sigmoid())
            opt=torch.optim.Adam(mlp.parameters(),lr=0.003)
            for ep in range(30):
                mlp.train(); opt.zero_grad(); loss=nn.MSELoss()(mlp(X),Y); loss.backward(); opt.step()
                if ep%10==0: print(f'[mlp] ep{ep:3d} loss={loss.item():.6f}')
            torch.save(mlp.state_dict(),ROOT/'mlp_ranker_model.pt'); print('[mlp] saved')

    feats_order=['twin_score','body_match','mood_match','scene_match','flavor_match','temp_match','health_penalty','novelty']
    with (ROOT/'ranker_feature_config.json').open('w',encoding='utf-8') as f: json.dump({'features':feats_order,'feature_dim':len(feats_order)},f,ensure_ascii=False,indent=2)
    print(f'[done] model_mode=new_twin_tower_mlp vocab={vs} features={feats_order}')

if __name__=='__main__': main()
