#!/usr/bin/env bash

sudo bash hamachi_reset.sh 2>&1 HAMACHI_ERROR.txt
sudo python lescan.py 2>&1 LESCAN_ERROR.txt
