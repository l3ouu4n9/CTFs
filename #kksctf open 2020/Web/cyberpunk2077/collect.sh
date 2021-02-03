#!/bin/bash

for i in $(seq 1 1300)
do
	curl -s http://tasks.kksctf.ru:30030/reports/$i | xmllint --html --xpath "//body//pre/text()" - | sed 's/ -/-/g' | gpg -d -q >> answer.txt;
	printf "\n" >> answer.txt;
	printf "$i\n";
done