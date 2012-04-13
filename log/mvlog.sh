#!/bin/bash
t=`date +%s`
for i in `ls | grep screenlog`
do
	mv $i /data/log/screenlog.$t
	t=$[$t+1]
done
