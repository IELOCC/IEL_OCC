#!/bin/bash

TEXT=$1
LET=${TEXT:0:1}
CONN=0

if [ "$LET" = "P" ]; then
    CONN=1
fi

echo $CONN
