#!/usr/bin/env python

import re
import os
import csv

def readContent(file):
  with open('Dataset/Training/' + file) as dat_file:
    data = dat_file.read()
  
  regex = re.compile('(<Content>)(.*)')
  results = regex.findall(data)

  return results

with open('contents_only.csv', 'w') as f:
  writer = csv.writer(f)
  
  for file in os.listdir('Dataset/Training/'):
    print(file)
    
    content = readContent(file)
    for element in content:
      writer.writerow([element[1]])
