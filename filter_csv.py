#!/usr/bin/env python

import csv

reader = csv.reader(open(r"output.csv"),delimiter=',')
filtered = filter(lambda p: '-1' != p[12] and  '-1' != p[13] and  '-1' != p[14] and '-1' != p[15] and  '-1' != p[16] and  '-1' != p[17] and  '-1' != p[18] and  '-1' != p[19]  , reader)
csv.writer(open(r"output_filtrato.csv",'w'),delimiter=',').writerows(filtered)