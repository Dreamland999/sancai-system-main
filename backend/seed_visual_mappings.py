"""Seed the visual_mappings table with tag-to-visual mappings.

Each row: given a source tag (BS/MS/CT/SE/EX/VI), what visual parameters to use.
The 12 VI tags also get self-mappings (VI001 -> {warm colors} etc.).
"""

from .database import get_conn


def seed_visual_mappings():
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM visual_mappings")

    mappings = []

    # ─── Visible VI tag self-mappings (VI001-VI012) ───────

    vi_mappings = [
        ("VI001", "暖色", "#FF8C42 #D4A574 #F5E6D3 #C08552 #FFF8F0",
         "圆润图形、柔和光晕", "居中构图，暖调渐变背景",
         "日系插画风格，温暖奶茶色系，柔和过渡"),
        ("VI002", "冷色", "#4A90D9 #7EC8E3 #A8D8EA #2C5F8A #F0F8FF",
         "流动线条、水纹、气泡", "对角构图，冷调渐变",
         "清新海洋风格，透亮玻璃质感"),
        ("VI003", "高明度", "#FFFFFF #FFFACD #E0F7FA #F5F5DC #FAFAFA",
         "轻盈图形、透亮元素", "大面积留白，中央聚焦",
         "极简清新风，明亮通透"),
        ("VI004", "低饱和", "#B8A9C9 #C4B5A5 #A3B1C6 #C9B8A8 #D5CFE0",
         "柔边图形、淡色渐变", "居中对称，低对比",
         "莫兰迪色系，安静柔和"),
        ("VI005", "圆润", "#FFD4A3 #FFE4C4 #F5DEB3 #FFECD2 #FDF5E6",
         "圆形、椭圆、圆弧线", "圆形环绕布局",
         "圆润可爱风，奶泡质感"),
        ("VI006", "流动线条", "#7EC8E3 #A8D8EA #B8E4F0 #E0F7FA #C8EFF9",
         "水波纹、流线、曲线", "S形或对角流动布局",
         "动态流畅，水彩晕染风"),
        ("VI007", "气泡元素", "#E0F7FA #B8E4F0 #FFFFFF #C8EFF9 #A8D8EA",
         "气泡、圆点、碳酸颗粒", "散点式分布，大小不一",
         "活泼气泡饮风格，跳跃感"),
        ("VI008", "植物元素", "#7CB342 #AED581 #C5E1A5 #81C784 #E8F5E9",
         "叶片、花瓣、藤蔓、果实", "角落簇拥或边框缠绕",
         "自然植物插画，水彩花草"),
        ("VI009", "地域元素", "#D4A574 #C08552 #8D6E63 #BCAAA4 #EFEBE9",
         "骑楼轮廓、木棉花、地方建筑剪影", "底部地平线构图",
         "城市记忆插画，地域文化符号"),
        ("VI010", "运动元素", "#FF6D00 #FF9100 #FFAB40 #FFF3E0 #FFCC80",
         "动感线条、球场图形、篮球轮廓", "对角线动态构图",
         "年轻活力运动风，动感线条"),
        ("VI011", "柔和线条", "#D5CFE0 #C9B8A8 #B8A9C9 #D8C8D0 #E8E0E8",
         "缓弧线、柔边图形、羽毛状", "水平或垂直舒缓排列",
         "安静柔和，薄雾轻纱质感"),
        ("VI012", "强对比", "#FF4444 #2196F3 #FFEB3B #212121 #FFFFFF",
         "几何图形、高反差块面、锐利边缘", "中心放射或四角对峙",
         "波普风格，视觉冲击力强"),
    ]
    for i, (vid, name, colors, graphics, composition, style) in enumerate(vi_mappings, 1):
        mappings.append((f"V{i:03d}", vid, colors, graphics, composition, style,
                         f"饮品主题插画，色板:{colors.split()[0]}，{graphics}，{composition}，风格:{style}"))

    _id_counter[0] = len(vi_mappings)  # resume from after VI entries

    # ─── Body state tags → visual ──────────────────────────

    body_mappings = [
        ("BS001", "疲惫", ["暖色", "低饱和", "柔和线条"],
         "#D4A574 #C4B5A5 #FFF8F0", "柔光圆形、棉絮感图形", "水平舒缓排列",
         "柔和陪伴感，不刺激的低饱和暖调"),
        ("BS002", "困倦", ["冷色", "高明度", "流动线条"],
         "#4A90D9 #FFFFFF #E0F7FA", "水纹、晨露、清凉感元素", "对角上升构图",
         "清晨明亮感，醒神但不刺眼"),
        ("BS003", "睡眠不足", ["暖色", "低饱和", "圆润"],
         "#C4B5A5 #F5DEB3 #FFF8F0", "圆润柔和图形、薄雾光晕", "居中柔和渐变",
         "温柔唤醒感，低负担视觉"),
        ("BS004", "胃敏感", ["暖色", "低饱和", "圆润"],
         "#FFF8F0 #FFECD2 #D4A574", "圆润无棱角图形", "居中对称舒适布局",
         "温和无刺激，干净舒适色调"),
        ("BS005", "乳糖不耐", ["冷色", "高明度", "植物元素"],
         "#E0F7FA #C5E1A5 #F5F5DC", "燕麦、椰子、植物叶片", "左上-右下自然分布",
         "植物基清新风，自然轻盈"),
        ("BS006", "咖啡因敏感", ["暖色", "低饱和", "植物元素"],
         "#C5E1A5 #B8A9C9 #F5F5DC", "花草、叶片、草本图案", "整版稀疏分布",
         "花草茶风格，温和无刺激"),
        ("BS007", "控糖", ["冷色", "高明度", "流动线条"],
         "#E0F7FA #FFFFFF #A8D8EA", "轻盈图形、透亮冰块", "大面积留白",
         "零卡轻盈感，清透干净"),
        ("BS008", "运动后", ["高明度", "冷色", "运动元素", "气泡元素"],
         "#FF6D00 #7EC8E3 #FFFFFF", "动感线条、水珠、气泡", "对角动态构图",
         "运动活力风，清爽补充感"),
    ]
    for tag_id, name, vi_refs, colors, graphics, composition, style in body_mappings:
        mappings.append((_next_vid(mappings), tag_id, colors, graphics, composition, style,
                         f"身体状态:{name}。{', '.join(vi_refs)}。{style}"))

    # ─── Mood state tags → visual ──────────────────────────

    mood_mappings = [
        ("MS001", "低落", ["暖色", "低饱和", "圆润", "柔和线条"],
         "#FFD4A3 #FFE4C4 #FFF8F0", "柔软圆润图形、温暖光晕", "居中包裹式构图",
         "被拥抱的温暖感，柔软不刺眼"),
        ("MS002", "烦躁", ["冷色", "高明度", "流动线条", "气泡元素"],
         "#4A90D9 #FFFFFF #E0F7FA", "水波纹、气泡、清凉流线", "自上而下流动布局",
         "清凉降温感，流动释放"),
        ("MS003", "紧张", ["低饱和", "植物元素", "柔和线条"],
         "#C5E1A5 #D5CFE0 #F5F5DC", "舒展叶片、缓弧线", "水平舒展排列",
         "舒缓平静，自然放松感"),
        ("MS004", "想放松", ["暖色", "低饱和", "植物元素", "柔和线条"],
         "#B8A9C9 #C5E1A5 #FFF8F0", "花瓣、叶片、柔雾光晕", "稀疏自然分布",
         "安静花草茶氛围，缓慢舒适"),
        ("MS005", "想提神", ["冷色", "高明度", "流动线条"],
         "#4A90D9 #FFFFFF #E0F7FA", "锐利流线、明亮光点", "对角上升动态",
         "清醒明亮感，活力注入"),
        ("MS006", "想安抚", ["暖色", "低饱和", "圆润"],
         "#FFE4C4 #FFD4A3 #FFF8F0", "圆形光晕、软绵图形", "居中对称包裹",
         "温暖奶香视觉，稳定陪伴"),
        ("MS007", "想满足", ["暖色", "高明度", "强对比"],
         "#FF8C42 #FFFFFF #F5E6D3", "浓郁质感、层次丰富图形", "中心放射构图",
         "甜品仪式感，浓郁满足"),
        ("MS008", "想释放", ["冷色", "强对比", "气泡元素"],
         "#2196F3 #FFFFFF #FFEB3B", "气泡爆发、锐利几何", "中心爆裂式构图",
         "爽快过瘾感，视觉释放"),
    ]
    for tag_id, name, vi_refs, colors, graphics, composition, style in mood_mappings:
        mappings.append((_next_vid(mappings), tag_id, colors, graphics, composition, style,
                         f"心情状态:{name}。{', '.join(vi_refs)}。{style}"))

    # ─── Scene tags → visual ───────────────────────────────

    scene_mappings = [
        ("CT001", "早晨", ["高明度", "冷色", "流动线条"],
         "#FFFFFF #E0F7FA #FFFACD", "晨光、朝露、清新图形", "左上至右下明亮渐变",
         "清晨第一缕光，清新明亮"),
        ("CT002", "下午学习", ["冷色", "低饱和", "植物元素"],
         "#A3B1C6 #C5E1A5 #F5F5DC", "书本几何、绿植点缀", "水平稳定排列",
         "专注学习氛围，不打扰的安静设计"),
        ("CT003", "夜间休息", ["暖色", "低饱和", "柔和线条"],
         "#C9B8A8 #D5CFE0 #1A1A2E", "星光、月影、微光图形", "下暗上明渐变",
         "安静夜晚氛围，低刺激暗色"),
        ("CT004", "图书馆/自习", ["低饱和", "冷色", "柔和线条"],
         "#A3B1C6 #D5CFE0 #F5F5DC", "直线条理、简约几何", "水平三分构图",
         "理性安静，无干扰设计"),
        ("CT005", "通勤", ["高明度", "流动线条", "冷色"],
         "#FFFFFF #7EC8E3 #E0F7FA", "流线型、速度感线条", "水平流动构图",
         "快速便捷感，移动友好"),
        ("CT006", "社交", ["暖色", "强对比", "植物元素"],
         "#FF8C42 #FFFFFF #FFEB3B", "聚会感图形、分享符号", "中心聚会式构图",
         "活泼社交感，适合分享展示"),
        ("CT007", "运动后", ["高明度", "冷色", "运动元素", "气泡元素"],
         "#7EC8E3 #FF6D00 #FFFFFF", "运动轨迹、汗滴/水珠、气泡", "对角动态",
         "运动清爽补给感"),
        ("CT008", "炎热天气", ["冷色", "高明度", "气泡元素"],
         "#4A90D9 #FFFFFF #E0F7FA", "冰块、水滴、清凉气泡", "大面积冷色铺底",
         "极度清凉感，视觉降温"),
        ("CT009", "寒冷天气", ["暖色", "低饱和", "圆润"],
         "#D4A574 #FFF8F0 #C08552", "热饮蒸汽、毛绒质感、暖光", "居中暖调包裹",
         "温暖热饮视觉，寒冬里的暖意"),
        ("CT010", "考试季", ["冷色", "低饱和", "植物元素", "柔和线条"],
         "#A3B1C6 #C5E1A5 #F5F5DC", "书堆轮廓、绿植、安静几何", "网格整齐排列",
         "紧张中带舒缓，高效学习感"),
    ]
    for tag_id, name, vi_refs, colors, graphics, composition, style in scene_mappings:
        mappings.append((_next_vid(mappings), tag_id, colors, graphics, composition, style,
                         f"场景:{name}。{', '.join(vi_refs)}。{style}"))

    # ─── Sensory/flavor tags → visual ──────────────────────

    flavor_mappings = [
        ("SE001", "清爽", ["冷色", "高明度", "流动线条"],
         "#4A90D9 #FFFFFF #E0F7FA", "水滴、冰晶、轻盈流线", "大面积留白", "极度清爽透亮"),
        ("SE002", "温热", ["暖色", "低饱和", "圆润"],
         "#FF8C42 #FFF8F0 #FFD4A3", "热气蒸腾、暖光圈", "中心暖调渐变", "温暖舒适感"),
        ("SE003", "冰爽", ["冷色", "高明度", "气泡元素"],
         "#A8D8EA #FFFFFF #7EC8E3", "冰块、霜花、冷气泡", "冷色满铺", "极度冰爽降温"),
        ("SE004", "奶香", ["暖色", "圆润", "柔和线条"],
         "#FFF8F0 #FFE4C4 #F5DEB3", "奶泡漩涡、圆润滴落", "居中柔焦", "丝滑奶感视觉"),
        ("SE005", "茶香", ["植物元素", "低饱和", "冷色"],
         "#81C784 #C5E1A5 #F5F5DC", "茶叶轮廓、茶园线条", "自然散布", "茶禅一味，清雅"),
        ("SE006", "果香", ["高明度", "暖色", "植物元素"],
         "#FFAB40 #FF8C42 #FFFFFF", "水果切片、果汁飞溅", "活泼散点", "鲜果明亮感"),
        ("SE007", "花香", ["植物元素", "低饱和", "柔和线条"],
         "#E8D5E0 #D5CFE0 #FFF8F0", "花瓣飘落、花枝轮廓", "浪漫散布", "花园氛围，柔美"),
        ("SE008", "咖啡香", ["暖色", "圆润", "低饱和"],
         "#6D4C41 #8D6E63 #D4A574", "咖啡豆、拉花、杯沿", "居中稳重", "精品咖啡质感"),
        ("SE009", "酸感", ["高明度", "冷色", "强对比"],
         "#FFEB3B #FFFFFF #7EC8E3", "柠檬切面、酸滴飞溅", "中央突出", "酸爽刺激视觉"),
        ("SE010", "甜感", ["暖色", "圆润", "高明度"],
         "#FFAB40 #FFE4C4 #FFFFFF", "蜂蜜滴落、糖粒闪光", "中央甜蜜聚焦", "甜品幸福感"),
        ("SE011", "苦感", ["低饱和", "暖色", "柔和线条"],
         "#6D4C41 #A3B1C6 #D5CFE0", "深色渐变、沉稳线条", "稳重水平构图", "成熟内敛质感"),
        ("SE012", "顺滑", ["圆润", "暖色", "柔和线条"],
         "#FFE4C4 #FFF8F0 #D4A574", "丝滑曲面、奶流弧线", "S形流动", "绸缎般顺滑视觉"),
        ("SE013", "浓郁", ["暖色", "强对比", "圆润"],
         "#6D4C41 #FF8C42 #212121", "厚重质感、丰富层次", "饱满中心构图", "浓郁厚重质感"),
    ]
    for tag_id, name, vi_refs, colors, graphics, composition, style in flavor_mappings:
        mappings.append((_next_vid(mappings), tag_id, colors, graphics, composition, style,
                         f"风味:{name}。{', '.join(vi_refs)}。{style}"))

    # ─── Experience tags → visual ──────────────────────────

    exp_mappings = [
        ("EX001", "提神", ["冷色", "高明度", "流动线条"],
         "#4A90D9 #FFFFFF #E0F7FA", "明亮射线、锐利线条", "对角上升", "清醒提神，视觉焕新"),
        ("EX002", "放松", ["暖色", "低饱和", "植物元素", "柔和线条"],
         "#C5E1A5 #D5CFE0 #FFF8F0", "舒展叶片、慢弧线", "水平舒缓", "慢慢放松，不急不躁"),
        ("EX003", "安抚", ["暖色", "低饱和", "圆润"],
         "#FFD4A3 #FFF8F0 #FFE4C4", "柔光包裹、软图形", "居中环抱", "温暖包裹，被照顾感"),
        ("EX004", "满足", ["暖色", "高明度", "强对比"],
         "#FF8C42 #FFFFFF #FFEB3B", "丰盛图形、层次堆叠", "中心饱满", "丰盛满足，仪式感"),
        ("EX005", "清爽", ["冷色", "高明度", "气泡元素"],
         "#FFFFFF #E0F7FA #7EC8E3", "水珠、冰晶、透亮", "大面积留白", "零负担清爽"),
        ("EX006", "释放", ["强对比", "冷色", "气泡元素"],
         "#2196F3 #FFFFFF #FF4444", "爆发气泡、冲击线条", "中心爆破", "爽快释放，过瘾感"),
        ("EX007", "专注", ["冷色", "低饱和", "植物元素"],
         "#A3B1C6 #C5E1A5 #F5F5DC", "秩序几何、绿色点缀", "网格整齐", "理性专注，零干扰"),
        ("EX008", "陪伴", ["暖色", "圆润", "低饱和"],
         "#FFE4C4 #D4A574 #FFF8F0", "双圆图形、温暖光斑", "左右对称相伴", "温暖陪伴，不孤单"),
        ("EX009", "低刺激", ["低饱和", "暖色", "柔和线条"],
         "#D5CFE0 #C9B8A8 #FFF8F0", "极简图形、柔边", "大面积空白", "温和无刺激，干净"),
        ("EX010", "轻补充", ["高明度", "冷色", "流动线条"],
         "#FFFFFF #E0F7FA #7EC8E3", "水滴、轻盈弧线", "稀疏分布", "轻盈补充，不厚重"),
    ]
    for tag_id, name, vi_refs, colors, graphics, composition, style in exp_mappings:
        mappings.append((_next_vid(mappings), tag_id, colors, graphics, composition, style,
                         f"体验:{name}。{', '.join(vi_refs)}。{style}"))

    # Insert all
    for m in mappings:
        vid, src_tag, colors, graphics, composition, style, prompt = m
        c.execute("""INSERT INTO visual_mappings
            (visual_id, source_tag_id, color_palette, graphics, composition, reference_style, example_prompt)
            VALUES (?,?,?,?,?,?,?)""",
            (vid, src_tag, colors, graphics, composition, style, prompt))

    conn.commit()
    conn.close()
    return len(mappings)


_id_counter = [0]

def _next_vid(existing):
    _id_counter[0] += 1
    return f"V{_id_counter[0]:03d}"


if __name__ == "__main__":
    from .database import init_db
    init_db()
    n = seed_visual_mappings()
    print(f"Seeded {n} visual mappings")
