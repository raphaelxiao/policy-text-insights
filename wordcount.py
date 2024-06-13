def wordcount(text1, text2, num, relativeOrNot, app_root_path, custom_dict=None):
    import matplotlib
    matplotlib.use('Agg')  # 设置matplotlib使用Agg后端，不需要GUI支持
    import matplotlib.pyplot as plt

    import jieba
    import jieba.posseg as pseg
    from collections import Counter
    import pandas as pd
    import os
    import numpy as np
    import re
    import uuid

    # 生成唯一的UUID
    unique_id = str(uuid.uuid4())

    # 加载自定义词典，如果有的话
    custom_words = []
    if custom_dict:
        custom_words = re.split(r'[,\n;；\s]', custom_dict)
        custom_words = [word for word in custom_words if word]  # 过滤空字符串
        jieba.load_userdict(custom_words)  # 直接加载自定义词典列表

    # 分词逻辑
    if custom_words:  # 有自定义词典时只统计词典中的词
        words1 = [word for word in jieba.cut(text1, cut_all=True) if word in custom_words]
        words2 = [word for word in jieba.cut(text2, cut_all=True) if word in custom_words]
    else:
        # 没有自定义词典时，分词并过滤出名词和动名词
        words_with_pos1 = [(word, flag) for word, flag in pseg.cut(text1) if flag.startswith('n') or flag == 'vn']
        words1 = [word for word, _ in words_with_pos1]
        words2 = [word for word in jieba.cut(text2, cut_all=True)]

    word_counts1 = Counter(words1)
    word_counts2 = Counter(words2)

    total_chars1 = len(text1)
    total_chars2 = len(text2)

    top_num_nouns = word_counts1.most_common(num)

    data = []
    for word, freq1 in top_num_nouns:
        freq2 = word_counts2[word]
        relative_freq1 = freq1 / total_chars1 if total_chars1 > 0 else 0
        relative_freq2 = freq2 / total_chars2 if total_chars2 > 0 else 0
        if relativeOrNot:
            data.append([word, relative_freq1, relative_freq2])
        else:
            data.append([word, freq1, freq2])

    df = pd.DataFrame(data, columns=['名词', '文本1', '文本2'])

    # 绘图
    # 根据项目数量动态调整图表高度
    fig_height = max(6, num / 3)  # 基础高度为6，每增加3个项目，图表高度增加1
    fig, ax = plt.subplots(figsize=(8, fig_height))  # 宽度固定为8，高度动态调整

    words = df['名词']
    freq1 = df['文本1']
    freq2 = df['文本2']

    # 字体设置
    font_path = os.path.join(app_root_path, 'static/NotoSansHans-Bold.otf')
    from matplotlib.font_manager import FontProperties
    font_prop = FontProperties(fname=font_path)
    plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
    plt.rcParams['axes.unicode_minus'] = False

    bar_width = 0.35
    index = np.arange(len(words))

    bars1 = plt.barh(index, freq1, bar_width, color='black', label='文本1')
    bars2 = plt.barh(index + bar_width, freq2, bar_width, color='#FFE600', label='文本2')

    if relativeOrNot:
        plt.xlabel('相对频次', fontproperties=font_prop)
        plt.title('政策文本相对频次对比', fontproperties=font_prop)
    else:
        plt.xlabel('频次', fontproperties=font_prop)
        plt.title('政策文本频次对比', fontproperties=font_prop)
    plt.ylabel('名词', fontproperties=font_prop)
    plt.yticks(index + bar_width / 2, words, fontproperties=font_prop)
    plt.legend(prop=font_prop)

    # 反转y轴的数据显示顺序
    plt.gca().invert_yaxis()

    plt.tight_layout()

    # 保存图表和数据
    plt_file_path = os.path.join(app_root_path, f"static/download/word_frequencies_{unique_id}.png")
    csv_file_path = os.path.join(app_root_path, f"static/download/output_{unique_id}.csv")
    # 确保保存目录存在
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
    plt.savefig(plt_file_path)
    plt.close()  # 关闭图表，以免在运行脚本时弹出窗口

    # 返回CSV文件的路径
    return f"download/output_{unique_id}.csv", f"download/word_frequencies_{unique_id}.png"
