#!/usr/bin/env bash
OUTFILE=/tmp/$(date +%m%d%Y).dat

./manage.py modelcount 2> $OUTFILE

echo -e "\n Stderr saved to $OUTFILE"