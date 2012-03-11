#!/bin/bash
while [ 1 ]
do
	date +%s >> cpu.txt
	top -b -n 1 |    awk '/mysql|python/{print $9, $12}' >> cpu.txt
	sleep 5
done
