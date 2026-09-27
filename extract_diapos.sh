#!/bin/sh

set -e

mkdir -p "$2"
# ffmpeg -i "$1" -vf "crop=1672:1248:284:6,fps=0.2" "$2"/slides_%04d.png
ffmpeg -i "$1" -vf "fps=0.2" "$2"/slides_%04d.png
