from HttpUtil import *
import re
import execjs
import csv

def get_js():
    f = open("email_decode.js", 'r', encoding='utf-8') # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr+line
        line = f.readline()
    return htmlstr

def get_des_email(data, key):
    jsstr = get_js()
    ctx = execjs.compile(jsstr) #加载JS文件
    return (ctx.call('n', data, key))  #调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数

reader = csv.reader(open('Firms with PSD Permissions (CSV).csv'))
reader1 = csv.reader(open('new.csv'))
data = []
for new_list in reader1:
    data.append(new_list[0])
for list in reader:
    print(list)
    if list[0] != 'FRN' and list[0] not in data:
        url = 'https://register.fca.org.uk/shpo_searchresultspage?search='+list[0]+'&TOKEN=3wq1nht7eg7tr'
        one_result = http_get_request(url,'')
        print(one_result)
        if one_result:
            patt = re.compile(r'window.location.href =\'(.+?)\';')
            two_result = patt.findall(one_result)
            print(two_result)
            if two_result:
                three_result = http_get_request(two_result[0],'')
                print(three_result)
                if three_result:
                    patt2 = re.compile(r'data-cfemail="(.+?)">')
                    four_result=patt2.findall(three_result)
                    print(four_result)
                    if four_result:
                        five_result = get_des_email(four_result[0],0)
                        print(five_result)
                        list[6]=five_result
                        with open('new.csv', 'a', newline='') as t_file:
                            csv_writer = csv.writer(t_file)
                            csv_writer.writerow(list)

