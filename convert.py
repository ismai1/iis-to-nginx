# coding: utf-8
from xml.etree import ElementTree
from xml.etree.ElementTree import XMLParser
from xml.sax.saxutils import unescape
import os


def convert_match (str):
    out = ""+str.replace('?$','')
    out = "/"+out.replace('^','')
    return out

def find_regex (str):
    regex = {'(.*)', '[0-9]', '*'}
    if any(x in regex for x in str):
        return True
    else:
        return False

os.popen("cat web.config | sed '/<!--.*-->/d' | sed '/<!--/,/-->/d' > webconfig.xml")     #remove comments from configuration file
tree = ElementTree.parse("webconfig.xml")
root = tree.getroot()

children = root.getchildren()


for child in root.iter('rule'):

    for ch in child.getchildren():

        if ch.tag == "match":
            if child.getchildren()[child.getchildren().index(ch)+1].attrib.get('type') == "Rewrite":
                match = convert_match(ch.attrib.get('url')).encode("utf-8")
                action = child.getchildren()[child.getchildren().index(ch)+1].attrib.get('url').encode("utf-8")
                print("#"+child.attrib.get("name").encode("utf-8"))
                if find_regex(match):
                    print("location ~ ^"+match+"$ {")
                    print("   proxy_pass \"http://localhost/"+action+"$1\";")
                else:
                    print("location "+match+" {")
                    print("   proxy_pass \"http://localhost/"+action+"\";")

                print("   proxy_set_header Host $http_host;")
                print("}\n")
               
