import logging
from logger.logger import set_logger
import os
import numpy as np
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('filespath',
                    help="path to files that should be combined")
parser.add_argument('outputpath',
                    help="path to outputfile, path/to/output.txt")



def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):

    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def combine(files_path, output_path):

    (_, _, filenames) = next(os.walk(files_path))

    linenumbers = []

    filenames = sorted([os.path.join(files_path, filename) for filename in filenames], key=natural_keys)
    logging.info("Combining files:")
    for filename in filenames:
        logging.info("File: {}".format(filename))
    

    with open(output_path, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line_n, line in enumerate(infile):
                    outfile.write(line)
                linenumbers.append(line_n+1)
    
    logging.info("Cumulative line numbers: {}".format(np.cumsum(linenumbers)[:-1]))

if __name__ == "__main__":
    
    args = parser.parse_args()

    set_logger("combine.log")
    logging.info("Combining files")
    combine(
        args.filespath, args.outputpath
    )
   


