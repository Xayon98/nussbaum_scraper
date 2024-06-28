# Nussbaum scraper

This was created to scrap all the files from our computer science teacher.

## Modules needed

- argparse
- request
- simple_colors

## Usage

For Help :
``` python3 app.py -h ```

```
usage: app.py [-h] [-u URL] [-o OUTPUT] [-r] [-f] [-t TYPE [TYPE ...]]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     url of the website
  -o OUTPUT, --output OUTPUT
                        output path and filename : path ilename
  -r, --remove          remove all pdf and zip files
  -f, --force           force download or removing of all files
  -t TYPE [TYPE ...], --type TYPE [TYPE ...]
                        type(s) of file to download
```
