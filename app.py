#!/usr/bin/python3

# Author : Xayon

import requests
import simple_colors as sc
import os
import sys
import argparse


def getPages(url='', path='', type=[], f=None, l_done=[]):
    r = requests.get(url)
    page = r.text.split('\n')
    pagename = url.split('/')[-1]
    l_done.append(pagename)
    for line in page:
        if 'link' not in line and 'href' in line:
            filename = line.split('"')[1]
            if filename not in l_done:
                if filename.split('.')[-1] in type:
                    getFile(url[:-len(pagename)] + filename,
                            pagename[:-4], path, f)
                elif 'php' in line:
                    getPages(url[:-len(pagename)] +
                             filename, path, type, f, l_done)
                else:
                    print(f"Nothing in {line.lstrip()}")
    print(f"Page {sc.red(pagename)} done")


def getFile(url, pagename, path, f):
    try:
        os.mkdir(f"{path}/{pagename}")
    except:
        pass

    filename = url.split('/')[-1]
    if not f and os.path.exists(f"{path}/{pagename}/{filename}"):
        print(f"{sc.cyan(filename)} already exists")
        return

    file = open(f"{path}/{pagename}/{filename}", 'wb')
    file.write(requests.get(url).content)
    file.close()
    print(f"Download of {sc.cyan(filename)} done")


def remove(f):
    if not f:
        ans = input(
            "Are you sure you want to remove all pdf and zip files? (y/n) ")
    else:
        ans = 'y'
    if ans.lower() == 'y':
        if sys.platform == 'linux':
            os.system('rm -v -r */*.pdf */*.zip')
            print(f"All pdf and zip files removed in {os.getcwd()}")
            ans2 = input("do you also want to remove the folders? (y/n) ")
            if ans2.lower() == 'y':
                os.system('rm -v -d */ 2>/dev/null')
                print(f"All folders removed in {os.getcwd()}")
            else:
                print("Nothing done")
        else:
            print("Unknown OS")
    else:
        print("Nothing done")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--url", help="url of the website", type=str,
                        default='https://nussbaumcpge.be/public_html/Sup/MP2I/index.php')
    parser.add_argument(
        "-o", "--output", help="output path and filename : path\filename", type=str, default=os.getcwd())
    parser.add_argument("-r", "--remove", help="remove all pdf and zip files",
                        action="store_true", default=False)
    parser.add_argument("-f", "--force", help="force download or removing of all files",
                        action="store_true", default=False)
    parser.add_argument(
        "-t", "--type", help="type(s) of file to download", nargs='+', default=['pdf', 'zip'])

    args = parser.parse_args()
    print(args)

    if args.remove:
        remove(args.force)
        sys.exit()
    else:
        getPages(args.url, args.output, args.type, args.force)


main()
