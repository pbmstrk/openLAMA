#!/bin/bash

echo "Downloading LAMA data"

LAMApath=https://dl.fbaipublicfiles.com/LAMA/data.zip
LAMAprefix=./data/LAMA/
LAMAdata=./data/LAMA/data.zip
SQUADpath=https://raw.githubusercontent.com/rajpurkar/SQuAD-explorer/master/dataset/dev-v1.1.json
SQUADprefix=./data/SQUAD/

# make directories to store original data
mkdir -p ./data 
mkdir -p ./data/LAMA/
mkdir -p ./data/SQUAD/ 

wget -c --directory-prefix=$LAMAprefix $LAMApath
unzip $LAMAdata -d $LAMAprefix && rm $LAMAdata
mv ./data/LAMA/data/* ./data/LAMA/ && rmdir ./data/LAMA/data/

wget -c --directory-prefix=$SQUADprefix $SQUADpath

# make directories to store openLAMA
mkdir -p ./openLAMA
mkdir -p ./openLAMA/SQUAD
mkdir -p ./openLAMA/Google_RE
mkdir -p ./openLAMA/trex
