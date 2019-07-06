#!/usr/bin/env python

import csv

reader = csv.reader(open(r"feature.csv"),delimiter=',')
filtered = filter(lambda p: '-1' != p[7] and  '-1' != p[8] and  '-1' != p[9] and '-1' != p[10] and  '-1' != p[11] , reader)
csv.writer(open(r"feature_filtrato.csv",'w'),delimiter=',').writerows(filtered)