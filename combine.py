import logging
from logger.logger import set_logger
import os
import numpy as np
import argparse
import re
import json

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
        logging.info("File: {}".format(os.path.basename(filename)))
    

    with open(output_path, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line_n, line in enumerate(infile):
                    outfile.write(line)
                linenumbers.append(line_n+1)

    basenames = [os.path.splitext(os.path.basename(filename))[0] for filename in filenames]
    cumulative_ln = [int(x) for x in np.cumsum(linenumbers)[:-1]]

    data = {"dataset": os.path.basename(files_path),"filenames": basenames, "linenumbers": cumulative_ln}

    with open('combine_data.json', 'w') as fp:
        json.dump(data, fp, indent=4)
        

if __name__ == "__main__":
    
    args = parser.parse_args()

    set_logger("combine.log")
    combine(
        args.filespath, args.outputpath
    )
   


