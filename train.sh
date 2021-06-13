#!/bin/bash

./cnn.py > stdout.txt
cp headerCont.py header.py	
cp -r Model/ Epoch1

for i in {2..5}
do
	./cnn.py >> stdout.txt
	cp -r Model/ Epoch$i
done
