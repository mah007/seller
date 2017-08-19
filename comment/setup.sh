#!/bin/bash

echo "Install chromedriver"
brew install chromedriver

echo "Install Pipreqs"
pip3 install pipreqs

echo "Generate dependency requirements.txt"
pipreqs --force .

echo "Install dependencies"
pip3 install -v -r requirements.txt
