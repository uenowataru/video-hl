#!/bin/sh
echo "Trailerifying $1..."
rm -rf "$1_trailer" >> /dev/null
mkdir "$1_trailer"
echo "Putting result in $1_trailer.."
python trailer.py $1 "$1_trailer/" $2
cd "$1_trailer"
echo "Creating video TRAILER_$1"
ffmpeg -r 20 -i ./frame%08d.png -b 16777216 "TRAILER_$1.mp4"