#!/bin/bash 

#  Note: requires 		brew install imagemagick


# create output folder (if it doesn't exist)
mkdir -p ../PICS-webopt

# compress JPG and JPEG
for f in *.jpg *.jpeg *.JPG *.svg; do
  [ -e "$f" ] || continue
  magick "$f" -auto-orient \
  -resize 1400x1400\> -quality 85 -strip -interlace Plane \
  "../PICS-webopt/${f%.*}-webopt.jpg"
done

# convert PNG → JPG
for f in *.png; do
  [ -e "$f" ] || continue
  magick "$f" -auto-orient \
  -background white -alpha remove -alpha off \
  -resize 1400x1400\> -quality 85 -strip -interlace Plane \
  "../PICS-webopt/${f%.*}-webopt.jpg"
done