#! usr/bin/env python
#-*-coding=utf-8-*-
# Author = wfy

import os
import sys
import json


from html.parser import HTMLParser
import urllib.request

class MyparseText(HTMLParser):
    text = False
    contents = []
    Title = False
    title = []


    def handle_starttag(self, tag, attr):
        if tag == 'div':
            if len(attr) == 0:
                pass
            else:
                for(variable, value) in attr:
                    if variable == "style" and value == "LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;":
                        self.text = True
        if tag == 'title':
            self.Title = True

    def handle_endtag(self, tag):
        if tag == "div":
            self.text = False
        if tag == 'title':
            self.Title = False

    def handle_data(self, data):
        if self.text:
            self.contents.append(data)
        if self.Title:
            self.title.append(data)

def main(htmlpath):
    num = 0
    data= {}
    lParser = MyparseText()
    filenamelist = os.listdir(htmlpath)
    for filename in filenamelist:
        lParser.contents = []
        lParser.title = []
        f1 = open(htmlpath+filename, 'rb')
        lParser.feed(f1.read().decode("utf8"))
        lParser.close()
        f1.close()

        title = "".join(lParser.title)
        contents = "".join(lParser.contents)
        data[title] = {}
        data[title]["文书正文"] = contents

        f2 = open(htmlpath+filename, 'r', encoding = 'utf-8')
        totalstring = f2.read()
        if "var jsonHtmlData = " in totalstring and "var caseinfo=JSON.stringify" in totalstring and "{" in totalstring and "}" in totalstring:
            elseinfo = totalstring.split("var jsonHtmlData = ")[0].split("var caseinfo=JSON.stringify")[1].split("{")[1].split("}")[0]
            try:
                elseinfo_dict = json.loads("{" + elseinfo + "}")
                #print((elseinfo_dict["案号"]))
            except:
                #print("this file has jsondecodeerror: " + filename)
                num += 1
                pass
            else:
                data[title]["案号"] = elseinfo_dict["案号"]
                data[title]["审判程序"] = elseinfo_dict["审判程序"]
                data[title]["案件类型"] = elseinfo_dict["案件类型"]
                data[title]["法院名称"] = elseinfo_dict["法院名称"]
                data[title]["法院省份"] = elseinfo_dict["法院省份"]
                data[title]["诉讼记录段原文"] = elseinfo_dict["诉讼记录段原文"]
                data[title]["案件基本情况段原文"] = elseinfo_dict["案件基本情况段原文"]
                data[title]["诉讼参与人信息部分原文"] = elseinfo_dict["诉讼参与人信息部分原文"]
                data[title]["案件基本情况段原文"] = elseinfo_dict["案件基本情况段原文"]
                data[title]["裁判要旨段原文"] = elseinfo_dict["裁判要旨段原文"]
                data[title]["判决结果段原文"] = elseinfo_dict["判决结果段原文"]
                data[title]["文本尾部原文"] = elseinfo_dict["文本尾部原文"]
                data[title]["附加原文"] = elseinfo_dict["附加原文"]
        else:
            data[title]["案号"] = ""
            data[title]["审判程序"] = ""
            data[title]["案件类型"] = ""
            data[title]["法院名称"] = ""
            data[title]["法院省份"] = ""
            data[title]["诉讼记录段原文"] = "" 
            data[title]["案件基本情况段原文"] = ""
            data[title]["诉讼参与人信息部分原文"] = ""
            data[title]["案件基本情况段原文"] = ""
            data[title]["裁判要旨段原文"] = ""
            data[title]["判决结果段原文"] = ""
            data[title]["文本尾部原文"] = ""
            data[title]["附加原文"] = ""

        
        #f = open(os.path.join(outpath, os.path.splitext(filename)[0] + '.txt'), 'w', encoding='utf-8')
        #print(lParser.contents)
        #f.write(data)
        #f.close()
       
        f1.close()
        f2.close()
    print(num)
    return data

if __name__ == '__main__':
    data = main(sys.argv[1])
    with open("11.json", 'w+', encoding='utf-8') as fp:
        json.dump(data, fp=fp, ensure_ascii=False, indent= 15)