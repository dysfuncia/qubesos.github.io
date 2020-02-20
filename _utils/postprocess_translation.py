#!/usr/bin/python3
#python posprocess_translation.py bg bg/ --yml
#adds language pattern in permalink line and all found relative links in the current open file recursively from a given root dir
#param1 is the language in short form
#param2 is the root dir
#param3 is optional indicating .yml files to be processed as in _data directory with no frontmatter whatsoever
import os
import sys
import frontmatter
import argparse 
import io
import yaml

patterns = (
    "](/",
    "]: /",
    "url: /",
    "href=\"/",
    "href=\'/",
)
news="/news/"
qubes_issues="/qubes-issues/"
url_key="url"

def process_markdown(filepath, lang):
    md = frontmatter.Post
    with io.open(filepath) as fp:
        md = frontmatter.load(fp)
        if md.get('permalink') != None and not md.get('permalink').startswith("/"+lang +"/"):
            md['permalink'] = "/" + lang + md.get('permalink')
        
        if md.get('redirect_from') != None:
            redirects = md.get('redirect_from')
            if isinstance(redirects, str):
                redirects = [redirects]
            if any('..' in elem for elem in redirects):
                print('ERRROR: \'..\' found in redirect_from')
                sys.exit(1)
            md['redirect_from'] = [("/" + lang + elem.replace('/en/', '/') if not elem.startswith("/" + lang + "/") else elem)
                                   for elem in redirects]
            if md['permalink'] in md['redirect_from']:
                md['redirect_from'].remove(md['permalink'])

        if md.get('lang') != None:
            md['lang'] = lang
        md['translated'] = 'yes'
        ## for testing only
        #if md.get('title') != None:
        #    md['title'] = lang + md.get('title')

            # replace links
    lines=[]
    for line in md.content.splitlines():
        for pattern in patterns:
            if pattern in line:
                tmp = line.split(pattern)
                line = tmp[0]
                for part in range(1, len(tmp)):
                    if not tmp[part].startswith(lang + "/") and \
                            not tmp[part].startswith('news') and \
                            not tmp[part].startswith('attachment') and \
                            not tmp[part].startswith('qubes-issues'):
                        line += pattern + lang + "/" + tmp[part]
                    else:
                        line += pattern + tmp[part]
        lines.append(line)

    md.content=os.linesep.join(lines) + '\n'

    with io.open(filepath, 'wb') as replaced:
        frontmatter.dump(md, replaced)

def replace_val(yml,key,val,lang):
    yml[key]= "/" + lang + val if ("/"+lang not in val and val.startswith("/")) else val
    return yml

def process_yml(filepath,lang):
    docs = []
    with io.open(filepath) as fp:
        docs = yaml.full_load(fp)
        for a in docs:
            if url_key in a:
                val = a[url_key]
                #print(val)
                #a[url_key] = "/" + lang + val if (lang not in val and val.startswith("/")) else val
                a=replace_val(a,url_key,a[url_key],lang)
                for b in a['sub-pages']:
                    #v = b[url_key]
                    b=replace_val(b,url_key,b[url_key],lang)
                    #b[url_key] = "/" + lang + v if (lang not in v and v.startswith("/")) else v
            else:
                return

    with io.open(filepath, 'w') as replaced:
        yaml.dump(docs, replaced, sort_keys=True)

def main(rootDir, lang, yml):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('current directory: %s' % dirName)
        if dirName[0] == '.':
            continue
        for fileName in fileList:
            print('\t%s' % fileName)
            if fileName[0] == '.':
                continue
            filepath=dirName+"/"+fileName
            if yml:
                process_yml(filepath,lang)
            else:
                process_markdown(filepath,lang)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("language")
    parser.add_argument("directory")
    parser.add_argument("--yml", action='store_true')
    args = parser.parse_args()

    main(args.directory, args.language, args.yml)
