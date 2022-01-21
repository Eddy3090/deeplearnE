#!/usr/bin/env bash
dist_dir=$1
rm_jpg=$2
if [ -z "$1" ]; then
    echo "must input some dir"
else
    echo "img convert in dir:" $dist_dir
    cd $dist_dir
    ls -1 *.jpg | xargs -n 1 bash -c 'convert "$0" "${0%.jpg}.png"'
    if [ $rm_jpg == 'r' ]; then
        echo $rm_jpg
        echo "replace ori imgs"
        rm -rf *.jpg
    fi
fi



