#!/bin/sh

git archive --output source.tar master

doas docker build -t resummarized-docker .
