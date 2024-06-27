# 政策词频分析器

欢迎来到 **政策词频分析器** 仓库！

## 概述

**政策词频分析器** 是一款强大的工具，旨在帮助您通过词频分析来分析和比较中文政策文件。无论您是研究人员、政策分析师，还是对理解政策语言细微差别感兴趣的个人，这款工具都能通过突出政策文件中最常用的词语和短语，为您提供有价值的洞察。

## 特点

- **易于使用**：用户友好的界面，便于进行分析。
- **全面分析**：提供详细的词频统计。
- **比较功能**：可以比较政策文件，识别常见主题和独特术语。
- **可定制**：支持定制词典以满足特定分析需求。
- **可视化**：生成清晰且信息丰富的词频可视化图表。

## 入门

要开始使用 **政策词频分析器**，请按照以下简单步骤操作：

1. **克隆仓库**：
   ```bash
   git clone https://github.com/raphaelxiao/policy-text-insights.git
   ```
2. **安装依赖项**：
   ```bash
   cd policy-text-insights
   pip install -r requirements.txt
   ```
3. **运行分析器**：
   ```bash
   python main.py
   ```

## 使用方法

1. 将最新的会议文本贴在左侧文本框，想对比的文本贴在右侧文本框
2. 设定要统计的词数（至少10）
3. 设定是否为相对词频（相对词频 = 词频 ÷ 全文字数；绝对词频则就是纯粹的词频数）
4. 按需看看是否要修改词典（用空格或逗号分隔），若字典留空则按jieba默认中文词库分词
5. 查看分析结果（可以下载csv文档或保存图片）

# Policy Text Insights

Welcome to the **Policy Text Insights** repository!

## Overview

**Policy Text Insights** is a powerful tool designed to help you analyze and compare Chinese policy documents through word frequency analysis. Whether you are a researcher, policy analyst, or someone interested in understanding the nuances of policy language, this tool provides valuable insights by highlighting the most frequently used words and phrases in policy documents.

## Features

- **Easy to Use**: User-friendly interface for seamless analysis.
- **Comprehensive Analysis**: Provides detailed word frequency statistics.
- **Comparison Capabilities**: Allows for comparing policy documents to identify common themes and unique terminology.
- **Customizable**: Supports custom dictionaries to meet specific analysis needs.
- **Visualizations**: Generates clear and informative visual representations of word frequencies.

## Getting Started

To get started with **Policy Text Insights**, follow these simple steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/raphael/policy-text-insights.git
   ```
2. **Install Dependencies**:
   ```bash
   cd policy-text-insights
   pip install -r requirements.txt
   ```
3. **Run the Analyzer**:
   ```bash
   python main.py
   ```

## Usage

1. Paste the latest conference text into the left text box, and the text you want to compare into the right text box.
2. Set the number of words to be counted (at least 10).
3. Set whether to use relative word frequency (relative word frequency = word frequency ÷ total number of words; absolute word frequency is simply the word count).
4. Optionally, modify the dictionary (separate words with spaces or commas). If left blank, the default Chinese dictionary of jieba will be used for word segmentation.
5. View the analysis results (you can download the CSV file or save the image).
