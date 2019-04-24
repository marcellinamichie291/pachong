# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup
import logging
from HttpUtil import *
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('./log/banks-new.log', encoding='utf-8')
# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
# 初始化日志
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(funcName)s() %(message)s',datefmt='%Y-%m-%d %H:%M:%S',handlers=[fh, ch])

url="http://bankswiftcode.info/SwiftCode/0"
s=http_get_request(url, '')
soup=BeautifulSoup(s,"html.parser")
patt = re.compile(r'<option.+?>(.+?)</option>')
# print(soup.select('#ctl00_ContentPlaceHolder1_ddlState'))
countrys = patt.findall(str(soup.select('#ctl00_ContentPlaceHolder1_ddlState')))
get_country=0
get_city=0
get_bank=0
for country in countrys:
    if country=='France':
        get_country=1
    if country != 'Select State' and country != 'Select City' and country != 'Select Bank' and get_country==1:
        country = country.replace(',','').replace('.','').replace('(','').replace(')','').replace('\'','').replace(' ','-').lower()
        url_city = "http://bankswiftcode.info/SwiftCode/"+country
        s_city = http_get_request(url_city, '')
        soup_city = BeautifulSoup(s_city, "html.parser")
        citys = patt.findall(str(soup_city.select('#ctl00_ContentPlaceHolder1_ddlCity')))
        for city in citys:
            if city=='LONGJUMEAU':
                get_city=1
            if city != 'Select State' and city != 'Select City' and city != 'Select Bank' and get_city==1:
                city = city.replace(',', '').replace('.', '').replace('(','').replace(')','').replace('\'','').replace(' ', '-').lower()
                url_bank = "http://bankswiftcode.info/SwiftCode/" + country+'/'+city
                s_bank =http_get_request(url_bank, '')
                soup_bank = BeautifulSoup(s_bank, "html.parser")
                banks = patt.findall(str(soup_bank.select('#ctl00_ContentPlaceHolder1_ddlBank')))
                for bank in banks:
                    if bank != 'Select State' and bank != 'Select City' and bank != 'Select Bank':
                        bank = bank.replace(' (','-').replace(' - ','-').replace(' ','-').replace(',','-').replace('.','').replace(')','').replace('-/-','-').replace('/','-').replace('----','-').replace('---','-').replace('--','-').replace('(','').lower()
                        if bank=='societe-generale':
                            get_bank=1
                        if get_bank==1:
                            url_content = "http://bankswiftcode.info/SwiftCode/" + country + '/' + city + '/' + bank
                            s_content = http_get_request(url_content, '')
                            if s_content is None:
                                print(url_content)
                            else:
                                s_content = s_content.replace('Bank :','<a>Bank :')
                                soup_content = BeautifulSoup(s_content, "html.parser")
                                contents = soup_content.find(id='ctl00_ContentPlaceHolder1_Result')
                                if contents is None:
                                    print(url_content)
                                else:
                                    for div in contents.findAll('div'):
                                        div = str(div)
                                        div = re.sub(re.compile(r"<a.*?>", re.S), "", str(div))
                                        div = re.sub(re.compile(r"<div.*?>", re.S), "", str(div))
                                        div = div.replace('<b>','').replace('</b>','').replace('</a>','').replace('</div>','')
                                        div = div.replace('\r','').replace('\n','').replace('                                                ','')
                                        infos = div.split('<br/>')
                                        logging.info(infos[0].split(':')[1].strip()+'\t'+infos[1].split(':')[1].strip()+'\t'+infos[2].split(':')[1].strip()+'\t'+infos[3].split(':')[1].strip()+'\t'+infos[4].split(':')[1].strip())





