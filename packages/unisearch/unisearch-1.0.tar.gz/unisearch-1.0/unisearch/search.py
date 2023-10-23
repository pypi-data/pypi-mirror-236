# -*- coding:utf-8 -*-
# import some necessary module
import random
import requests                 # 网页请求
import re                       # 正则表达
from bs4 import BeautifulSoup   # 解析页面
from time import sleep          # 等待时间
import os
import json
import base64
import sqlite3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from selenium import webdriver
import time
from sendemailcyf.operations import send_email

# 定义一些正则表达式
baidu_info_obj = re.compile(r'<div>.*?"dispTime":"(?P<dispTime>.*?)",".*?',re.S)
baidu_search_obj = re.compile(r'<div.*?"newTimeFactorStr":"(?P<newTimeFactorStr>.*?)",".*?',re.S)

# 定义多个请求头，应对反爬
Google_Headers = {                               # google 的请求头
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/",
    "Accept_Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Accept-Encoding":"gzip, deflate, br",
    "Host":"www.google.com",
    "Cookie":""                                   # Cookie实时修改，才能保证获取正确数据
}
google_cookie_model = "HSID=AzJbqO4AEzSs3ZVgQ; SSID=A5g-rQCzPLplW3KH5; APISID=LNQraQrKBpvkbFAi/AyENdXLHfaRqpfmB1; SAPISID=h7Xbu9v-6tUonB55/A3sg67Y0R8RErOpY2; __Secure-1PAPISID=h7Xbu9v-6tUonB55/A3sg67Y0R8RErOpY2; __Secure-3PAPISID=h7Xbu9v-6tUonB55/A3sg67Y0R8RErOpY2; OTZ=7235013_24_24__24_; SID=bgiALd2-wbt_uQkWs8fEd50Tmo8Hd-4MljvbvbEPCyLal_bR7CTGVUKraNmMO58KXaYZDQ.; __Secure-1PSID=BBrURw.; __Secure-3PSID=U06uicvtIE_g.; SEARCH_SAMESITE=CgQIu5kB; AEC=JM0PXOtw; __Secure-ENID=FhHcSGU4; NID=511=ZcFxnGeyax5SBVKJakcqplztBFHghjNxdg1-jpyybNNF5OSfCK1-tWimOMsWbeNzQxJSzMVLFvRxke41ERmft7goSPwDhx5Rc9CTk-pIH6ncFg_c8FJqVBlvpTgNVMr3Xm5afcxv8JyCvypguJlue0eqK3otkBiiczKiU-Zpku5vjTlyhnIKFKDPBEr_ispUnCFzthKRMFwSCMPuSAIy__6LlpdhFICUGm-WLLeUaynJPK_isYaiBWReXZTr4dGoh3HYBDv9pUFCu66XdkcWf32TCCu-UzxH7-VTM4oCYL162rNJbujEs0a6UcwAzEDYR-EtLlGdFg; 1P_JAR=2023-10-13-4; __Secure-1PSIDTS=sidts-CjIB3e41heE93xirL6uA90o46hADLb1NAebDVvF4vcAPAIXkGrQEVHVvqt1JzutSKn4sFBAA; __Secure-3PSIDTS=sidts-CjIB3e41heE93xirL6uA90o46hADLb1NAebDVvF4vcAPAIXkGrQEVHVvqt1JzutSKn4sFBAA; SIDCC=ACA-OxN6sOcr7y44KqwzaRPAdxDfbzmmND6GKQL347hRZ1h_iL1paRGqJX5bLy5aHL4EATCEnY_O; __Secure-1PSIDCC=ACA-OxNo75K5-Dpcs9bsBZQXRSEEQBmjbpaGnLVUJom7u-wcIRfupb50puZMaz89QuoLoJiTgRQp; __Secure-3PSIDCC=ACA-OxNLkRWJg3yDkjNkMZhcdfeBPb8qTBGj0Na_T4SEwxt66nbX_uq7lev-6c-gjOZOSF4BUh4"

baidu_headers = {                                 # 百度 的请求头
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/",
    "Accept_Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Accept-Encoding":"gzip, deflate, br",
    "Host":"www.baidu.com",
    'Cookie':'BIDUPSID=E8E39D2F554F0C91847D231EF4CCAC6C; PSTM=1677725210; BDUSS=U8wNndpc1hhejZ2SEk5OE5abkZYTElZODRTSEVIR01oVlF3ZEh1OUp4UTZtaTlrSVFBQUFBJCQAAAAAAAAAAAEAAADa0tArY2FpeW91ZmVpMjAxMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADoNCGQ6DQhkb; BDUSS_BFESS=U8wNndpc1hhejZ2SEk5OE5abkZYTElZODRTSEVIR01oVlF3ZEh1OUp4UTZtaTlrSVFBQUFBJCQAAAAAAAAAAAEAAADa0tArY2FpeW91ZmVpMjAxMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADoNCGQ6DQhkb; MSA_WH=1537_833; BAIDUID=BF4313DF6BA75BE3055A280F8A812D94:SL=0:NR=10:FG=1; H_WISE_SIDS=234020_110085_259297_265863_266322_266759_265886_266565_266874_268634_259642_269389_256154_269552_245010_269731_268235_268435_269904_270182_270596_270662_270969_271034_268876_271170_271177_271007_267659_271322_271471_269610_270102; BD_UPN=12314753; H_WISE_SIDS_BFESS=234020_110085_259297_265863_266322_266759_265886_266565_266874_268634_259642_269389_256154_269552_245010_269731_268235_268435_269904_270182_270596_270662_270969_271034_268876_271170_271177_271007_267659_271322_271471_269610_270102; MCITY=-257%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=39310_39367_39398_39396_39352_39407_39480_39477_39462_39233_39486_26350_39424; BAIDUID_BFESS=BF4313DF6BA75BE3055A280F8A812D94:SL=0:NR=10:FG=1; delPer=0; BD_CK_SAM=1; PSINO=7; sug=0; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=143cdqz%2BgKVLmB52BPZwJbYuLk2tHsczLTJRBlqUpcajSBgHlrsgTGG91BQ; BA_HECTOR=20850g00alah2k2g2h0524ap1ii809p1p; ZFY=UlYmY9w31jCGvRxq44dkox7qGOsE:AWADYtvt2c6hOxY:C; Hm_lvt_aec699bb6442ba076c8981c6dc490771=1695130455,1695710763,1695821836,1696859263; Hm_lpvt_aec699bb6442ba076c8981c6dc490771=1696859263'
}

# 获搜索目标的实时cookie
def fetch_host_cookie(host,cookie_model):                                          # 实时获取Google的最新Cookie
    try:                                                                           # 判断Chrome流浪器是否打开，如果打开就直接关闭
        os.system('taskkill /F /IM chrome.exe')
    except Exception:
        print("Chrome is not open")
    "获取指定域名下的所有cookie"
    userDataDir = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data'
    localStateFilePath = userDataDir + r'\Local State'
    cookiepath = userDataDir + r'\Default\Cookies'
    if not os.path.exists(cookiepath) or os.stat(cookiepath).st_size == 0:           # 97版本已经将Cookies移动到Network目录下
        cookiepath = userDataDir + r'\Default\Network\Cookies'
    sql = f"select name,encrypted_value from cookies where host_key like '%.{host}'"
    cookies = {}
    with open(localStateFilePath, encoding='u8') as f:                               #"读取chrome保存在json文件中的key再进行base64解码和DPAPI解密得到真实的AESGCM key"
        encrypted_key = json.load(f)['os_crypt']['encrypted_key']
    encrypted_key_with_header = base64.b64decode(encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        for name, encrypted_value in cu.execute(sql).fetchall():
            nonce, cipherbytes = encrypted_value[3:15], encrypted_value[15:]
            aesgcm = AESGCM(key)
            cookies[name] = aesgcm.decrypt(nonce, cipherbytes, None).decode('u8')
    # print(cookies)
    cookie_item = cookie_model.split(' ', -1)                             # 提取关键词
    cookie_all = ''
    for i in range(len(cookie_item)):  # 确认所有的关键词是否存在
        cookie_key = cookie_item[i].split('=', 1)[0]
        try:
            result = cookies[cookie_key]
        except Exception as e:                  # 有不存在的关键词
            print("Cookie中没有关键字：" + cookie_key)
            cookies_new = selenium_get_cookies("https://www.toutiao.com")
            try:
                if cookie_key == '__ac_nonce':                            # 如果已知是这个参数没有的话
                    cookies['__ac_nonce'] = cookies_new['__ac_nonce']
                    cookies['__ac_signature'] = cookies_new['__ac_signature']
                    cookies['__ac_referer'] = cookies_new['__ac_referer']
                    cookies['msToken'] = cookies_new['msToken']
                else:
                    cookies[cookie_key] = ''
            except Exception as e:
                print(e)
    for i in range(len(cookie_item)):
        cookie_key = cookie_item[i].split('=', 1)[0]
        cookie_all = cookie_all + cookie_key + '=' + cookies[cookie_key] + ';'
    return cookie_all

# 进行 < Google > 搜索
def google_search_info(key_word,max_page):                                #google 资讯搜索
    list_all = ''
    list_all = list_all + "\n\nGoogle 资讯:"
    list_all = list_all + "\n-------------------------------------------------------------" + key_word + " -------------------------------------------------------------\n"
    global Google_Headers
    list_title = []                                                        #定义几个关键list，用于存储爬取的结果
    list_href = []
    list_time = []
    for page_num in range(max_page):
        print(key_word+" Google资讯第{}页".format(page_num+1))
        sleep(random.uniform(1,2))                                    # 随机等待小于1-2s
        url = "https://www.google.com/search?q="+key_word+"&sca_esv=572793137&tbm=nws&sxsrf=AM9HkKlR5c4Zsna6fIOIFnUDKhz5gKsRUA:0&source=lnt&tbs=qdr:w&sa=X&ved=2ahUKEwjk9_eJg_CBAxWEV0EAHT2AAk0QpwV6BAgCEA8&biw=1707&bih=910&dpr=1.5"
        try:
            resp = requests.get(url, headers=Google_Headers)
        except Exception as e:
            print("无法连接google，VPN 未开启")
            list_all = list_all + "无法连接google，VPN 未开启"
            continue
        html = BeautifulSoup(resp.text,"html.parser")
        title_list = html.find_all(class_="n0jPhd ynAwRc MBeuO nDgy9d")    # 找到所有的标题
        href_list = html.find_all(class_="WlydOe")                         # 找到所有的href
        time_list = html.find_all(class_="OSrXXb rbYSKb LfVVr")            # 找到所有的time

        for item in title_list:
            list_title.append(item.text)
        for item in href_list:
            list_href.append(item["href"])
        for item in time_list:
            list_time.append(item.find("span").text)
        for i in range(len(list_title)):
            item_content = '''
            %s: --%s--%s--%s
            ''' % (i+1, list_time[i], list_title[i], list_href[i])
            list_all = list_all+item_content
    return list_all

def google_search(key_word,max_page):                                     # goole 内容搜索
    list_all = ''
    list_all = list_all + "\n\nGoogle 搜索:"
    list_all = list_all + "\n-------------------------------------------------------------" + key_word + " -------------------------------------------------------------\n"
    global Google_Headers
    list_title = []
    list_href = []
    list_time = []
    for page_num in range(max_page):
        print(key_word+" Google搜索第{}页".format(page_num+1))
        sleep(random.uniform(0,1))                                   # 随机等待小于1s
        url = "https://www.google.com/search?q="+key_word+"&sca_esv=572781667&sxsrf=AM9HkKmgXmiEZbdDrQVUBvalkBSn7IK27A:1697091487393&source=lnt&tbs=qdr:w&sa=X&ved=2ahUKEwi_l4e67u-BAxXasFYBHTL4BDUQpwV6BAgCECY&biw=1707&bih=910&dpr=1.5&bshm=rimc/1"
        try:
            resp = requests.get(url, headers=Google_Headers)
        except Exception as e:
            print("无法连接google，VPN 未开启")
            list_all = list_all + "无法连接google，VPN 未开启"
            continue
        html = BeautifulSoup(resp.text,"html.parser")
        result_list = html.find_all(class_="g Ww4FFb vt6azd tF2Cxc asEBEc")
        time_list = html.find_all(class_="lhLbod gEBHYd")

        for item in result_list:
            list_title.append(item.find("h3").text)
            list_href.append(item.find("a")["href"])
        for item in time_list:
            list_time.append(item.find("span").text)
        for i in range(len(list_title)):
            item_content = '''
            %s: --%s--%s--%s
            ''' % (i+1, list_time[i], list_title[i], list_href[i])
            list_all = list_all+item_content
    return list_all

# 进行 < 百度 >搜索
def baidu_search_info(v_keyword,v_max_page):
    list_all = ''
    list_all = list_all + "\n\n百度 资讯:"
    list_all = list_all + "\n-------------------------------------------------------------" + v_keyword + " -------------------------------------------------------------\n"
    item_num = 0                                                         # 用来记录当前条目
    for page in range(v_max_page):
        print(v_keyword+" 百度资讯第{}页".format(page+1))
        wait_seconds = random.uniform(0,1)                         #产生一个随机数，模拟人的点击的方式
        sleep(wait_seconds)
        url = "https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd="+str(v_keyword)+"&medium=0&pn="+str(page*10)
        resp = requests.get(url,headers=baidu_headers)
        html = resp.text
        soup = BeautifulSoup(html,"html.parser")
        result_list = soup.find_all(class_="result-op c-container xpath-log new-pmd")
        for result in result_list:
            item_num = item_num+1
            title = result.find("a").text                              # 拿到标题
            href =result.find("a")["href"]                             # 拿到链接
            intro = result.find(class_="c-font-normal c-color-text").text[0:50]+"...."   # 拿到简介
            info = baidu_info_obj.finditer(str(result))                     # 获取链接时间
            dispTime = 'None'
            for item in info:
                dispTime = item.group("dispTime")

            item_content = '''
            %s: --%s--%s--%s
            ''' % (item_num, dispTime,title, href)
            list_all = list_all+item_content
    return list_all

def baidu_search(v_keyword,v_max_page):
    list_all = ''
    list_all = list_all + "\n\n百度 搜索:"
    list_all = list_all + "\n-------------------------------------------------------------" + v_keyword + " -------------------------------------------------------------\n"
    item_num = 0                                                         # 用来记录当前条目
    for page in range(v_max_page):
        print(v_keyword + " 百度搜索第{}页".format(page+1))
        wait_seconds = random.uniform(0,1)                          #产生一个随机数，模拟人的点击的方式
        sleep(wait_seconds)
        url = "https://www.baidu.com/s?wd="+v_keyword+"&gpc=stf%3D1696325537%2C1696930336%7Cstftype%3D1&pn="+str(page*10)
        resp = requests.get(url,headers=baidu_headers)
        html = resp.text
        soup = BeautifulSoup(html,"html.parser")
        result_list = soup.find_all(class_="result c-container xpath-log new-pmd")

        for result in result_list:
            item_num = item_num+1
            title = result.find("a").text                                  # 拿到标题
            url =result.find("a")["href"]                                  # 拿到链接
            url = get_baidu_real_url(url)
            displaytime = 'None'                                           # 获取链接时间
            info = baidu_search_obj.finditer(str(result))
            for item in info:
                displaytime = item.group("newTimeFactorStr")
            item_content = '''
            %s: --%s--%s--%s
            ''' % (item_num,displaytime, title, url)
            list_all = list_all+item_content
    return list_all

def get_baidu_real_url(v_url):                                            # 定义一个函数，获取真实的地址
    r = requests.get(v_url,headers=baidu_headers,allow_redirects=False)   # 不允许重定向
    if r.status_code == 302:                                              # 如果返回302，就从响应头中获取真实的地址
        real_url = r.headers.get("location")
    else:                                                                 # 否则从返回内容中，用正则表达式提取
        real_url = re.findall("URL = '(.*?)'",r.text)[0]
    return real_url

# if __name__ == '__main__':
#     keyword = ['飞行汽车','科技']
#     search_result = ''
#     for i in range(len(keyword)):
#         search_result = search_result + google_search_info(keyword[i],2)
#
#     send_email(search_result,keyword[0],'unisearch','Charles')
