#!/usr/bin/python3

# Author : Xayon

import requests
import simple_colors as sc
import os
import sys
import argparse

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


# gestion arguments à revoir
def main():
    if len(sys.argv) == 3:
        if sys.argv[1] == '-h' or sys.argv[2] == '-h':
            print(f"Usage: getfile [website_url] [output_path]")
            sys.exit()
        elif sys.argv[1] == '-rm':
            remove()
            sys.exit()
        elif sys.argv[1] == 'n' or sys.argv[1] == 'nussbaum':
            getPages('https://nussbaumcpge.be/public_html/Sup/MP2I/index.php',sys.argv[2])
        else:
            raise Exception("Unknown website")
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print(f"Usage: getfile [website_url] [output_path]")
            sys.exit()
        elif sys.argv[1] == '-rm':
            remove()
            sys.exit()
        elif sys.argv[1] == 'n' or sys.argv[1] == 'nussbaum':
            getPages('https://nussbaumcpge.be/public_html/Sup/MP2I/index.php')
        else:
            getPages(sys.argv[1])
    elif len(sys.argv) > 3:
        raise Exception("Too many arguments")
    else:
        getPages()


def getPages(url = 'https://nussbaumcpge.be/public_html/Sup/MP2I/index.php', path = os.getcwd(), l_done = []):
    r = requests.get(url)
    page = r.text.split('\n')
    pagename = url.split('/')[-1]
    l_done.append(pagename)   
    for line in page: 
        if 'link' not in line and 'href' in line:
            filename = line.split('"')[1]
            if filename not in l_done:
                if 'pdf' in line or 'zip' in line:
                    getFile(url[:-len(pagename)] + filename, pagename[:-4], path)
                elif 'php' in line:                    
                    getPages(url[:-len(pagename)] + filename, path, l_done)
                else:
                    print(f"Nothing in {line.lstrip()}")
    print(f"Page {sc.red(pagename)} done")


def getFile(url, pagename, path):
    print(url, pagename, path)
    try: 
        os.mkdir(f"{path}/{pagename}")
    except:
        pass

    filename = url.split('/')[-1]
    if  os.url.exists(f"{path}/{pagename}/{filename}"):
        print(f"{sc.cyan(filename)} already exists")
        return
    
    file = open(f"{path}/{pagename}/{filename}", 'wb')
    file.write(requests.get(url).content)
    file.close()
    print(f"Download of {sc.cyan(filename)} done")



def remove():
    ans = input("Are you sure you want to remove all pdf and zip files? (y/n) ")
    if ans.lower() == 'y' :
        os.system('rm -v -r */*.pdf */*.zip')
        print(f"All pdf and zip files removed in {os.getcwd()}")
        ans2 = input("do you also want to remove the folders? (y/n) ")
        if ans2.lower() == 'y':
            os.system('rm -v -d */ 2>/dev/null')
            print(f"All folders removed in {os.getcwd()}")
        else:
            print("Nothing done")
    else:
        print("Nothing done")
    

# def getMetadata(url):
#     fp = open('/home/xayon/Documents/Cours/Info/1-Cours/arbres/arbresbinaires.pdf', 'rb')
#     parser = PDFParser(fp)
#     doc = PDFDocument(parser)
#     print(doc.info[0]['ModDate'].decode())
#     dt_object = datetime.fromtimestamp(int(doc.info[0]['ModDate']))
#     print(doc.info)



# getMetadata('https://nussbaumcpge.be/public_html/Sup/MP2I/flottants.pdf')




# parser = argparse.ArgumentParser()
# parser.add_argument("-w", "--website", help="website to scrap", type=str, default="nussbaum")
# parser.add_argument("-o", "--output", help="output url and filename", type=str, default=os.getcwd())





main()