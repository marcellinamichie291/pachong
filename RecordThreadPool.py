import concurrent
from concurrent.futures import ProcessPoolExecutor
import re
from bs4 import BeautifulSoup
import logging
from HttpUtil import *

class RecordThreadPool:

    def __init__(self):
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler('./log/banks-thread.log', encoding='utf-8')
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        # 初始化日志
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(funcName)s() %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', handlers=[fh, ch])
        self.executor = ProcessPoolExecutor(max_workers=10)
        self.patt = re.compile(r'<option.+?>(.+?)</option>')

    def set_record(self,country,city,bank):
        url_content = "http://bankswiftcode.info/SwiftCode/" + country + '/' + city + '/' + bank
        s_content = http_get_request(url_content, '')
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
                div = div.replace('\r', '').replace('\n', '').replace(
                    '                                                ', '')
                infos = div.split('<br/>')
                logging.info(
                    infos[0].split(':')[1].strip() + '\t' + infos[1].split(':')[1].strip() + '\t' + infos[2].split(':')[
                        1].strip() + '\t' + infos[3].split(':')[1].strip() + '\t' + infos[4].split(':')[1].strip())

    def get_bank(self, country, city):
        url_bank = "http://bankswiftcode.info/SwiftCode/" + country + '/' + city
        s_bank = http_get_request(url_bank, '')
        soup_bank = BeautifulSoup(s_bank, "html.parser")
        banks = self.patt.findall(str(soup_bank.select('#ctl00_ContentPlaceHolder1_ddlBank')))
        for bank in banks:
            if bank != 'Select State' and bank != 'Select City' and bank != 'Select Bank':
                bank = bank.replace(' (', '-').replace(' - ', '-').replace(' ', '-').replace(',',
                                                                                             '-').replace(
                    '.', '').replace(')', '').replace('-/-', '-').replace('/', '-').replace('----',
                                                                                            '-').replace(
                    '---', '-').replace('--', '-').replace('(', '').lower()
                self.executor.submit(self, self.set_record(country, city, bank))

    def get_contents(self):

        url = "http://bankswiftcode.info/SwiftCode/0"
        s = http_get_request(url, '')
        soup = BeautifulSoup(s, "html.parser")

        # print(soup.select('#ctl00_ContentPlaceHolder1_ddlState'))
        countrys = self.patt.findall(str(soup.select('#ctl00_ContentPlaceHolder1_ddlState')))
        country = ''
        for country in countrys:
            if country != 'Select State' and country != 'Select City' and country != 'Select Bank':
                country = country.replace(',', '').replace('.', '').replace('(', '').replace(')', '').replace('\'',
                                                                                                              '').replace(
                    ' ', '-').lower()
                url_city = "http://bankswiftcode.info/SwiftCode/" + country
                s_city = http_get_request(url_city, '')
                soup_city = BeautifulSoup(s_city, "html.parser")
                citys = self.patt.findall(str(soup_city.select('#ctl00_ContentPlaceHolder1_ddlCity')))
                for city in citys:
                    if city != 'Select State' and city != 'Select City' and city != 'Select Bank':
                        city = city.replace(',', '').replace('.', '').replace('(', '').replace(')', '').replace(
                            '\'', '').replace(' ', '-').lower()
                        self.executor.submit(self, self.get_bank(country, city))



if __name__ == '__main__':
        rtp = RecordThreadPool()
        rtp.get_contents()