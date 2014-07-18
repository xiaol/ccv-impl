__author__ = 'ding'
#coding=utf-8
#@author dingyaguang

from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element
 
ET._original_serialize_xml = ET._serialize_xml
 
 
def _serialize_xml(write, elem, encoding, qnames, namespaces):
    if elem.tag == '![CDATA[':
        write("<%s%s]]>%s" % (elem.tag, elem.text, elem.tail))
        return
    return ET._original_serialize_xml(
        write, elem, encoding, qnames, namespaces)
ET._serialize_xml = ET._serialize['xml'] = _serialize_xml

def xml2dict(element):
    if type(element) in [str, unicode]:
        element = ET.fromstring(element)
    assert isinstance(element, Element)
    ret = {}
    for child in list(element):
        #print child.tag, child.text
        if len(child) != 0:
            value = xml2dict(child)
        else:
            value = child.text
        if child.tag in ret:
            if type(ret[child.tag]) != list:
                ret[child.tag] = [ret[child.tag]]
            ret[child.tag].append(value)
        else:
            ret[child.tag] = value
    return ret


def dict2xml(root, content):
    if type(content) in [str, unicode, int, long, float]:
        e = Element(root)
        e.text = content
        return e

    e = Element(root)
    for key in content:
        if type(content[key]) == list:
            for one in content[key]:
                e.append(dict2xml(key, one))
        else:
            e.append(dict2xml(key, content[key]))
    return e


xml_tostring = ET.tostring


#=============================================================

def testXml2Json():
    s = '''
    <xml>
     <ToUserName><![CDATA[toUser]]></ToUserName>
     <FromUserName><![CDATA[fromUser]]></FromUserName>
     <CreateTime>1348831860</CreateTime>
     <MsgType><![CDATA[text]]></MsgType>
     <Content><![CDATA[this is a nothing]]></Content>
     <MsgId>1234567890123456</MsgId>
     </xml>
    '''

    s2 = '''
    <root>
         <person age="18">
            <name>hzj</name>
            <sex>man</sex>
         </person>
         <person age="19" des="hello">
            <name>kiki</name>
            <sex>female</sex>
         </person>
         <person2 age="19" des="hello">
            <name>kiki</name>
            <sex>female</sex>
         </person2>
        </root>
    '''

    print xml2dict(ET.fromstring(s2))

def testJson2xml():
    d = {'a':'4234','b':[{'a':'1'},{'b':'2'}]}
    print dict2xml('xml',d)
    print xml2dict(dict2xml('xml',d))



if __name__ == '__main__':
    testXml2Json()
 
