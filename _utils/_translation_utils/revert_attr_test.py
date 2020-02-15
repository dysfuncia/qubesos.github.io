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

def main(rootDir):
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
                if md.get('lang') != None:
                    del md['lang']
                if md.get('ref') != None:
                    del md['ref']
            bi = io.BytesIO()
            frontmatter.dump(md,bi)
            with io.open(filepath, 'wb') as replaced:
                replaced.write(bi.getbuffer())
            bi.close() 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()

    main(args.directory)


