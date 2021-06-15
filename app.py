import glob
import re
import os
from concurrent import futures
from xml.etree.ElementTree import parse

regexp = re.compile(r'[A-z]+_{2}.*')


def process_file(filename):
    if regexp.match(os.path.basename(filename)):
        os.remove(filename)
        return (filename, True)
    else:
        return (filename, False)
    # with open(filename, 'r', encoding="utf-8") as content:


if __name__ == '__main__':
    list_of_files = list(glob.iglob('folder/**/*.xml', recursive=True))
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
