#!/bin/bash
while [ 1 ]
do
	mv screenlog.0 s.0 -f
	mv screenlog.1 s.1 -f
	#cat s.0 | grep debug > res1.txt
	#cat s.1 | grep debug > res2.txt
	#python sendToMe.py
	let time=`date +%s`
	mv s.0 /data/s0.$time
	mv s.1 /data/s1.$time
	echo '' > screenlog.0
	echo '' > screenlog.1
	sleep 7200
done
