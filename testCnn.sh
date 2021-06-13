#!/bin/bash

file=$(ls BiometricsIdealTest/ | shuf -n 1) 
cp "BiometricsIdealTest/${file}" "test.bmp"
./cnn.py
xdg-open test.bmp
xdg-open output.jpg
