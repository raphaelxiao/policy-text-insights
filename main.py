from flask import Flask, request, send_file, render_template_string, redirect, url_for
from wordcount import wordcount  # 确保wordcount函数适合作为模块导入
import webbrowser
from threading import Timer
import os

app = Flask(__name__)

# 为了简化，将HTML模板定义为一个多行字符串
# 注意：在实际项目中，最好将HTML内容移到独立的模板文件中
form_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>政策文件词频比较分析工具</title>
    <link rel="icon" type="image/x-icon" href="/static/images/favicon.ico">
    <link rel="stylesheet" href="static/style.css">
    <script>
    function validateForm() {
        var num = document.forms["wordcountForm"]["num"].value;
        if (num === "" || !Number.isInteger(parseFloat(num)) || parseInt(num, 10) <= 0) {
            alert("请输入一个正整数。");
            return false;
        }
        return true;
    }
    </script>
</head>
<body>
    <div class="header">
        <img src="static/images/logo.png" alt="Logo" class="logo">
        <div class="header-text">
            <h1>政策文件词频比较分析工具</h1>
            <p>自动统计文本1高频词汇，并统计它们在文本2中出现的频次</p>
        </div>
    </div>
    <form action="/wordcount" method="post">
        <div class="parameters">
            <div class="parameter-left">
                <h2>参数</h2>
                <label for="num"><b>统计高频词汇数:&emsp;&emsp;&emsp;</b></label>
                <input type="number" name="num" id="num" min="10" placeholder="10" value="10" required style="width: 40px;">
                <br><br>
                <label for="relativeOrNot"><b>是否统计相对频率：&emsp;</b></label>
                <input type="checkbox" name="relativeOrNot" id="relativeOrNot" value="true"><br>
                相对频率 = 词频 ÷ 全文字数<br>
                <br>
            </div>
            <div class="parameter-right">
                <h2>词典</h2>
                <p>默认只统计词典所列出词汇，可编辑（用空格或逗号分隔），若字典留空则按默认中文词库分词。</p>
                <textarea name="custom_dict" style="width:100%;height:60px;resize:none;">中国特色社会主义 中国特色 一带一路 新发展理念 供给侧结构性改革 供给侧改革 国家治理体系 生态文明建设 双循环 国内大循环 科技创新 互联网+ 数字经济 人工智能 5G 高质量发展 绿色 共享经济 精准扶贫 脱贫攻坚 依法治国 国家安全 一国两制 和平 开放型经济 国际合作 全球治理 人民币国际化 金融科技 网络空间安全 民主 社会保障体系 教育 医疗 新型城镇化 文化自信 软实力 军民融合 国防科技 国防 智慧城市 碳达峰 碳中和 双碳 可持续发展 国际关系新格局 多边主义 世界经济 贸易摩擦 国际规则 人类命运共同体 疫情 公共卫生体系 产教融合 创新驱动发展战略 国家重点研发计划 产业升级 高端制造 新质生产力 全要素生产率 中国制造2025 制造业 服务业 工业 区域协调发展 长江经济带 粤港澳大湾区 京津冀协同发展 创业 大众创业万众创新 社会主义核心价值观 信用体系建设 反腐 人权保障 少数民族发展 平等 团结 文化遗产保护 旅游业发展 农业现代化 食品安全 能源结构调整 新能源 清洁能源 气候变化 环境保护法 水资源管理 生物多样性 土地整治 林业发展 海洋经济 灾害防治 应急管理 国际交流 对外援助 文化软实力 体育事业 奥运会 科技奥运 青奥会 世博会 亚投行 金砖国家 上合组织 亚太经合组织 世界卫生组织 信息化发展 国家大数据战略 网络强国 数字化转型 跨境电商 电子政务 智能化升级 区块链 隐私保护 数据安全 国民经济和社会发展 新发展阶段 经济建设 政治建设 文化建设 社会建设 制造强国 交通强国 数字中国 智能社会 科技创新体系 现代产业体系 国家安全体系 开放型经济新体制 社会主义民主法治 生态环境改善 国际竞争新优势 城乡区域协调发展 人民生活质量 绿色发展 创新型国家 全球治理体系 国家自主创新示范区 高新技术产业开发区 经济技术开发区 战略性新兴产业 现代农业 现代金融 社会治理体系 科技成果转化 产学研用深度融合 国际科技合作 新型国际关系 现代化产业体系 新冠疫情防控 国产大飞机 国产大型邮轮 新能源汽车 国家实验室体系 全国统一大市场 自贸试验区 粮食安全 生态环境保护 污染防治攻坚战 “三北”工程 可再生能源 居民人均可支配收入 脱贫攻坚成果 基础教育 养老保险 基本医疗保险 中国特色大国外交 量子技术 东西部协作 民营经济 健康中国 养老金 非物质文化遗产 全民健身 就业 高端装备研制 产业链供应链稳定 新型基础设施建设 国际市场份额 高技能人才 数字基础设施 高素质专业化教师 社会保障 营商环境 制度型开放 乡村振兴</textarea>
            </div>
        </div>
        <div class="text-entry">
            <h2 style="margin-top:0;">文本录入</h2>
            <div class="text-areas-container">
                <textarea name="text1" placeholder="请输入文本1" class="text-area"></textarea>
                <textarea name="text2" placeholder="请输入文本2" class="text-area"></textarea>
            </div>
        </div>
        <div class="footer">
            <button type="submit">词频比较</button>
            <p>公众号：1日闻</p>
        </div>
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(form_page)

@app.route('/wordcount', methods=['POST'])
def handle_wordcount():
    text1 = request.form['text1']
    text2 = request.form['text2']
    custom_dict = request.form['custom_dict']
    num = request.form['num']
    # 使用request.form.get()获取relativeOrNot，并提供默认值'false'
    relativeOrNot_str = request.form.get('relativeOrNot', 'false')
    # 将获取的字符串值转换为布尔值
    relativeOrNot = relativeOrNot_str == 'true'
    # 调用wordcount函数并接收返回的CSV文件路径
    num = int(request.form['num'])  # 转换num为整数
    # 接收返回的CSV和图片文件路径
    csv_file_path, plt_file_path = wordcount(text1, text2, num, relativeOrNot, app.root_path, custom_dict)  # 这里假设wordcount函数已经生成了图表和CSV文件

    # 注意这里的图片路径要对应wordcount.py中的保存路径
    result_page = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>分析结果</title>
        <link rel="icon" type="image/x-icon" href="/static/images/favicon.ico">
        <link rel="stylesheet" href="static/style.css">
    </head>
    <body>
        <div class="header">
        <img src="static/images/logo.png" alt="Logo" class="logo">
        <div class="header-text">
            <h1>政策文件词频比较分析工具</h1>
            <p>自动统计文本1高频词汇，并统计它们在文本2中出现的频次</p>
        </div>
        </div>
        <center><img src="/static/{plt_file_path}" alt="Word Frequencies"></center>
        <center>
            <a href="/download?file_path={csv_file_path}"><button>下载数据</button></a>
            <a href="/"><button>再次分析</button></a>
        </center>
    </body>
    </html>
    '''.format(plt_file_path=plt_file_path, csv_file_path=csv_file_path)  # 使用.format()插入实际的图片路径和CSV文件路径
    return render_template_string(result_page)

@app.route('/download', methods=['GET'])
def download():
    file_path = request.args.get('file_path')
    if file_path:
        csv_file_path = os.path.join(app.root_path, "static", file_path)
        return send_file(csv_file_path, as_attachment=True, download_name='result.csv')
    return redirect(url_for('index'))

def open_browser():
      webbrowser.open_new('http://0.0.0.0:5001/')

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1, open_browser).start()  # 仅在重启后的进程中打开网页
    app.run(debug=True, port=5001, host='0.0.0.0')
