#!/bin/bash

rm bundle.zip

zip -9 bundle.zip handler.py
zip -r9 bundle.zip worker.py
zip -r9 bundle.zip logger.py

zip -r9 bundle.zip /usr/lib64/libxml2.so
zip -r9 bundle.zip /usr/lib64/libxml2.so.2
zip -r9 bundle.zip /usr/lib64/libxml2.so.2.9.1

cd .env/lib64/python2.7/site-packages && zip -r9 ../../../../bundle.zip *

cd ../../../../

cd .env/lib/python2.7/site-packages && zip -r9 ../../../../bundle.zip *
