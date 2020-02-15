#!/usr/bin/python3
#python posprocess_translation.py bg bg/
#adds language pattern in permalink line and all found relative links in the current open file recursively from a given root dir
#param1 is the language in short form
#param2 is the root dir
import os
import sys
import frontmatter
import argparse 
import io

patterns = (
    "](/",
    "]: /",
    "url: /",
    "href=\"/",
)
news="/news/"
qubes_issues="/qubes-issues/"

def main(rootDir, lang):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('current directory: %s' % dirName)
        if dirName[0] == '.':
            continue
        for fileName in fileList:
            print('\t%s' % fileName)
            if fileName[0] == '.':
                continue
            filepath=dirName+"/"+fileName
            md = frontmatter.Post
            with io.open(filepath) as fp:
                md = frontmatter.load(fp)
                if md.get('redirect_from') != None:
                    redirects = md.get('redirect_from')
                    if isinstance(redirects, str):
                        redirects = [redirects]
                    if any('..' in elem for elem in redirects):
                        print('ERRROR: \'..\' found in redirect_from')
                        sys.exit(1)
                    md['redirect_from'] = [("/" + lang + elem.replace('/en/', '/') if not elem.startswith("/" + lang + "/") else elem)
                                           for elem in redirects]
                if md.get('permalink') != None and not md.get('permalink').startswith("/"+lang +"/"):
                    md['permalink'] = "/" + lang + md.get('permalink')
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



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("language")
    parser.add_argument("directory")
    args = parser.parse_args()

    main(args.directory, args.language)
