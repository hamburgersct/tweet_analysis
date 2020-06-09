# tweet_analysis

## 数据来源
https://github.com/echen102/COVID-19-TweetIDs

## Notes！
- **推荐使用anaconda创建虚拟环境**
- 首先运行``` pip install -r requirements.txt ```或```conda install --yes --file requirements.txt```</br>
- 使用conda安装```conda install -c plotly plotly-orca```
- 要在项目所在文件位置建立./tweets文件夹用来存储所有的tweet json（命名格式为coronavirus-tweet-id-2020-01-21-23.json）</br>
- 然后运行launch.py

## 当前状态
- [x] 英文分词</br>
- [x] ngram分析及图表</br>
- [ ] 英文LIWC</br>
- [ ] 其他语言
- [ ] 地理特征分析

## 输出文件
- ```./tweet_result```存放由tweet json转换而来的csv文件
- ```./tweet_per_day```存放每日的tweet csv汇总
- ```./clean_en_tweet```把csv中clean_text写入文件，每条一行（用来做LIWC）
- ```./tokenize_en_result```分词处理后的文本写入
- ```./bi(tri)_gram_folder```存储每日bgram、trigram分析结果
- ```./bi(tri)_images```存储每日的2/3gram图像
