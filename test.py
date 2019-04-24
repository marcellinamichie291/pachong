# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup
import threading
import logging
import asyncio
from aiohttp import ClientSession

async def print_content(country,city,bank):
    url_content = "http://bankswiftcode.info/SwiftCode/" + country + '/' + city + '/' + bank
    async with ClientSession() as session:
        async with session.get(url_content) as response:
            s_content = str(await response.read())
            # print(s_content)
            # r_content.encoding = r_content.apparent_encoding
            # s_content = r_content.text
            s_content = s_content.replace('Bank :', '<a>Bank :')
            soup_content = BeautifulSoup(s_content, "html.parser")
            contents = soup_content.find(id='ctl00_ContentPlaceHolder1_Result')
            if contents is None:
                logging.info(url_content)
            else:
                for div in contents.findAll('div'):
                    div = str(div)
                    div = re.sub(re.compile(r"<a.*?>", re.S), "", str(div))
                    div = re.sub(re.compile(r"<div.*?>", re.S), "", str(div))
                    div = div.replace('<b>', '').replace('</b>', '').replace('</a>', '').replace('</div>', '')
                    div = div.replace('\r\n', '').replace('\r', '').replace('\n', '').replace('                                                ', '')
                    infos = div.split('<br/>')
                    # logging.info(infos)
                    result=infos[0].split(':')[1].strip() + '\t' + infos[1].split(':')[1].strip() + '\t' + infos[2].split(':')[
                                     1].strip() + '\t' + infos[3].split(':')[1].strip() + '\t' + infos[4].split(':')[
                                     1].strip()
                    result=result.replace('\r\n', '').replace('\r', '').replace('\n', '').replace('\\r\\n', '').replace('\\r', '').replace('\\n', '').replace('	                            ', '\t')
                    logging.info(result)
                    # print(result)
    # r_content = requests.get(url_content)


# 初始化日志
def logInit():
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('./log/banks.log', encoding='utf-8')
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    # 初始化日志
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(funcName)s() %(message)s',datefmt='%Y-%m-%d %H:%M:%S',handlers=[fh, ch])

def get_contents():
    url="http://bankswiftcode.info/SwiftCode/0"
    r=requests.get(url)
    r.encoding=r.apparent_encoding
    s=r.text
    soup=BeautifulSoup(s,"html.parser")
    patt = re.compile(r'<option.+?>(.+?)</option>')
    # print(soup.select('#ctl00_ContentPlaceHolder1_ddlState'))
    countrys = patt.findall(str(soup.select('#ctl00_ContentPlaceHolder1_ddlState')))
    i=0
    start_record = 0
    for country in countrys:
        if country == 'Austria':
            start_record = 1
        if country != 'Select State' and country != 'Select City' and country != 'Select Bank' and start_record==1:
            # print(country)
            url_city = "http://bankswiftcode.info/SwiftCode/"+country
            r_city = requests.get(url_city)
            r_city.encoding = r_city.apparent_encoding
            s_city = r_city.text
            soup_city = BeautifulSoup(s_city, "html.parser")
            citys = patt.findall(str(soup_city.select('#ctl00_ContentPlaceHolder1_ddlCity')))
            for city in citys:
                # print(city)
                if city != 'Select State' and city != 'Select City' and city != 'Select Bank':
                    url_bank = "http://bankswiftcode.info/SwiftCode/" + country+'/'+city
                    r_bank = requests.get(url_bank)
                    r_bank.encoding = r_bank.apparent_encoding
                    s_bank = r_bank.text
                    soup_bank = BeautifulSoup(s_bank, "html.parser")
                    banks = patt.findall(str(soup_bank.select('#ctl00_ContentPlaceHolder1_ddlBank')))
                    for bank in banks:
                        if bank != 'Select State' and bank != 'Select City' and bank != 'Select Bank':
                            bank = bank.replace(' (','-').replace(' - ','-').replace(' ','-').replace(',','-').replace('.','').replace(')','').replace('-/-','-').replace('/','-').replace('----','-').replace('---','-').replace('--','-').replace('(','').lower()
                            loop = asyncio.get_event_loop()
                            loop.run_until_complete(print_content(country, city, bank))
                            # t = threading.Thread(target=print_content(country,city,bank), args=(i,))
                            # t.start()




if __name__ == '__main__':
    logInit()
    get_contents()