# coding = utf-8
# @Author = wfy

import os
'''
解析XML文件，获取文书文件标题及文件路径名
'''
                        
                        
# SAX解析
import sys
import xml.sax
get_record = []
class Sax_Parser(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.wsmc = ""
        self.wspath = ""

    def startElement(self, label, attrs):
        self.CurrentData = label
        if label == "T_WSFW_WS":
            return label

    def characters(self, content):
        if self.CurrentData == "C_WSMC":
            self.wsmc = content
        if self.CurrentData == "C_DOC_PROTOCOL":
            self.wspath = content

    def endElement(self, label):
        global get_record
        if self.CurrentData == "C_WSMC":
            get_record.append(self.wsmc)
        if self.CurrentData == "C_DOC_PROTOCOL":
            get_record.append(self.wspath)
    
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = Sax_Parser()
parser.setContentHandler(Handler)
parser.parse("ws20180831220044949.xml")
print(get_record)



# DOM解析
import xml.dom.minidom
document_tree = xml.dom.minidom.parse("ws20180831220044949.xml")
collection = document_tree.documentElement
if collection.hasAttribute("data"):
    print("root element：%s" % collection.getAttribute("data"))
WSFW = collection.getElementsByTagName('T_WSFW_WS')
wenshu_list = []
for wenshu_object in WSFW:
    wsmc = wenshu_object.getElementsByTagName("C_WSMC")[0]
    wspath = wenshu_object.getElementsByTagName("C_DOC_PROTOCOL")[0]
    wenshu_list.append(wsmc.childNodes[0].data +'\t' + wspath.childNodes[0].data)
    print(type(wspath.childNodes[0].data))
    #f = open(wspath.childNodes[0].data, 'r')
print((wenshu_list[0]))



# ElementTree 解析
import xml.etree.cElementTree as ce
a = ce.parse("ws20180831220044949.xml")
b = a.findall('T_WSFW_WS')
list1=[]
class etree_parser:
    def __init__(self, wsmc = 0, wspath = 0):
        self.wsmc = wsmc
        self.wspath = wspath
 
    def __repr__(self):
        return self.wsmc+"\t"+self.wspath+"\t"
for i in b:
    lei1=etree_parser()
    #b1=i.getchildren()#得到每一次项子节点——列表
    b1 = list(i)
    lei1.wsmc=b1[0].text#得到列表元素
    lei1.wspath=b1[1].text
    #print(type(lei1.wspath))
    #f = open(lei1.wspath, 'r')
    #print(len(f.readlines()))
    list1.append(lei1)


