#!/bin/sh

git archive --output source.tar master

docker build . --file Dockerfile -o local --tag resummarized:$(date +%s)
