#!/bin/bash

URL="http://localhost:5000/api/timeline_post"
RANDOM_NUM=$RANDOM

curl -s -X POST "$URL" -d "name=TestUSER${RANDOM_NUM}&email=Test${RANDOM_NUM}.@example.com&content=Timeline post ${RANDOM_NUM}"

response=$(curl -S "$URL")

if echo "$response" | grep ${RANDOM_NUM}; then
	echo 'Test Passed: Timeline post found.'
else
	echo 'Test Failed: Timeline post not found.'
	exit 1
fi
