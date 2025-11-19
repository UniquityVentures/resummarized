#!/bin/sh

git archive --output source.tar master

docker build . --file Dockerfile --tag resummarized:$(date +%s)
