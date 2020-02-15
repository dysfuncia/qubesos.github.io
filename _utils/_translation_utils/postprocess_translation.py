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

pattern="](/"
pattern2="]: /"
pattern3="url: /"
news="/news/"
qubes_issues="/qubes-issues/"

def is_pattern_in_line(pattern, line, lang):
    return pattern in line and "/"+lang+"/" not in line and news not in line and qubes_issues not in line

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
                    # FIXME: (marmarek) make it more defensive!
                    if isinstance(redirects,str) and "/" + lang + "/" not in md.get('redirect_from') :
                        md['redirect_from'] = "/" + lang + md.get('redirect_from')
                    else:
                        # FIXME: (marmarek) make it more defensive!
                        md['redirect_from'] = ["/" + lang + elem for elem in redirects if "/en/" not in elem]
                # FIXME: (marmarek) make it more defensive!
                if md.get('permalink') != None and "/"+lang +"/" not in md.get('permalink') :
                    md['permalink'] = "/" + lang + md.get('permalink')
                if md.get('lang') != None:
                    md['lang'] = lang
                md['translated'] = 'yes'
                ## for testing only
                #if md.get('title') != None:
                #    md['title'] = lang + md.get('title')
            lines=[]
            for line in md.content.splitlines():
                tmp=line.split(pattern)
                tmp2=line.split(pattern2)
                tmp3=line.split(pattern3)
                if tmp and is_pattern_in_line(pattern,line, lang):
                    replace=tmp[0]+pattern+lang+"/"+tmp[1]
                    lines.append(replace)
                elif tmp2 and is_pattern_in_line(pattern2,line, lang):
                    replace=tmp2[0]+pattern2+lang+"/"+tmp2[1]
                    lines.append(replace)
                elif tmp3 and is_pattern_in_line(pattern3,line, lang):
                    replace=tmp3[0]+pattern3+lang+"/"+tmp3[1]
                    lines.append(replace)
                else:
                    lines.append(line)
            md.content=os.linesep.join(lines)

            bi = io.BytesIO()
            frontmatter.dump(md,bi)
            with io.open(filepath, 'wb') as replaced:
                replaced.write(bi.getbuffer())
            bi.close() 



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("language")
    parser.add_argument("directory")
    args = parser.parse_args()

    main(args.directory, args.language)
