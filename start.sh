#!/bin/bash
screen -d -m node myserver.js
python updatePort.py

screen -d -m paster serve --reload development.ini 
screen -d -m paster serve --reload development0.ini 
screen -d -m paster serve --reload development1.ini 
