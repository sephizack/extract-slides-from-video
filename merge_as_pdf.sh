#!/bin/sh

FOLDER="$1"
img2pdf "$FOLDER"/*.png -o "$FOLDER".pdf