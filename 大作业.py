from selenium import webdriver;#导入selenium模块
import time;
import jieba
import jieba.posseg as pseg
import jieba.analyse as anls
import json;
web = webdriver.Chrome()#用webdriver启动浏览器
#加载网页
web.get("https://www.court.gov.cn/wenshu.html?keyword=%E5%88%91%E4%BA%8B%E8%A3%81%E5%AE%9A%E4%B9%A6&caseid=&starttime=&stoptime=")
time.sleep(1)
n=1
y=1
#爬取117份的裁判文书
while y<10:
    alst=web.find_elements_by_class_name('list_tit')
    for x in alst:
        x.find_element_by_tag_name("a").click();
        web.switch_to.window(web.window_handles[-1])
        text=web.find_element_by_xpath('//*[@id="container"]/div/div').text
        f=open("文书text/裁判文书_%s.txt" % n,mode="w")
        f.write(text)
        f.close()
        web.close()
        web.switch_to.window(web.window_handles[0])
        time.sleep(1)
        n=n+1
    web.find_element_by_xpath('//*[@id="yw0"]/li[last()-1]/a').click()
    y=y+1;
#使用jieba对获取到的text进行分析
m=1;
while m<118 :
    text = ''
    with open('文书text/裁判文书_%s.txt'% m,'r') as inf:
        text=inf.read()
    words = jieba.cut(text)
    result=jieba.analyse.extract_tags(text, topK=20, withWeight=False, allowPOS=())
    seg_list = pseg.cut(text)
    words = jieba.tokenize(text)
    for tk in words:
        print("word:" + tk[0] +
              " start:" + str(tk[1]) +
              " end:" + str(tk[2]))
        #将分析好的文本转为json
    d=dict(zip(seg_list,words))
    s = json.dumps(d)
    f = open("文书json/裁判文书_%s.json" % m, mode="w")
    f.write(s)
    m=m+1;
    f.close()