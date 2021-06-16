#!/usr/bin/env python3
import glob
import argparse
import re
import os
from concurrent import futures
from xml.etree.ElementTree import parse
from PathType import PathType

regexp = re.compile(r'[A-z]+_{2}.*')


def process_file(filename):
    if regexp.match(os.path.basename(filename)):
        os.remove(filename)
        return (filename, True)
    else:
        return (filename, False)
    # with open(filename, 'r', encoding="utf-8") as content:


def run(list_of_files):
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_file = dict((executor.submit(process_file, filename), filename)
                              for filename in list_of_files)

    for future in futures.as_completed(future_to_file):
        file = future_to_file[future]
        if future.exception() is not None:
            print('%r generated an exception: %s' % (file,
                                                     future.exception()))
        else:
            filename, is_deleted = future.result()
            if is_deleted:
                print('%s deleted' % filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Delete managed package metadata files and references')
    parser.add_argument('directory', type=PathType(exists=True, type='dir'),
                        help='directory to process')

    args = parser.parse_args()

    list_of_files = list(glob.iglob('%s/**/*.xml' %
                                    args.directory, recursive=True))
    run(list_of_files)
