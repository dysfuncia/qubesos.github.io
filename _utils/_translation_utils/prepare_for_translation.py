#!/usr/bin/python3
#python prepare_for_translation.py bg bg/ counter_file
#adds lang and ref attribute (starting from counter) to existing files after permalink line recursively from a given root dir
#param1 is the language in short form
#param2 is the root dir
# expects a file containing the value of the current reference counter as a third argument with exactly onle line in the form of
# current counter: x
from io import open as iopen
from os.path import isfile
from sys import exit
from argparse import ArgumentParser
from frontmatter import Post, load, dump
from logging import basicConfig, getLogger, DEBUG, Formatter, FileHandler


def read_counter(counterfile):
    if not isfile(counterfile):
        print('check your files')
        exit()
    with iopen(counterfile,'r') as c:
        counter_line=c.readline()
        counter_a=counter_line.split('current counter: ')
    return int(counter_a[1])

def write_counter_to_file(counter, counterfile):
    if not isfile(counterfile):
        print('check your files')
        exit()
    with iopen(counterfile,'w') as c:
        counter_line ='current counter: ' + str(counter)
        c.writelines(counter_line)
        c.truncate()


def main(rootDir, lang, counter):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('current directory: %s' % dirName)
        if dirName[0] == '.':
            continue
        for fileName in fileList:
            print('\t%s' % fileName)
            if fileName[0] == '.':
                continue
            filepath=dirName+"/"+fileName
            with iopen(filepath) as fp:
                md = load(fp)
                if not md.metadata:
                    continue
                if md.get('lang') == None:
                    md['lang'] = "en"

                if md.get('ref') == None:
                    md['ref'] = counter
                    counter+=1

            with iopen(filepath, 'wb') as replaced:
                dump(md,replaced)
                replaced.write(b'\n')

    return counter


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("language")
    parser.add_argument("directory")
    parser.add_argument("counterfile")
    args = parser.parse_args()

    counter=read_counter(args.counterfile)
    print('\n CURRENT COUNTER IS %s' % counter)
    cc = main(args.directory, args.language, counter)
    print('\n NEW CURRENT COUNTER IS %s' % cc)
    write_counter_to_file(cc,args.counterfile)
