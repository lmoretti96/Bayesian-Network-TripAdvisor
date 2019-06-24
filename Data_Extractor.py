import re
import os
import csv

def readContent(file):
  with open('Dataset/Training/' + file, errors='ignore') as dat_file:
    data = dat_file.read()
  
  regex = re.compile('(<Content>)(.*)')
  results = regex.findall(data)

  return results

with open('tmp-returns.csv', 'w') as f:
  writer = csv.writer(f)
  
  for file in os.listdir('Dataset/Training/'):
    print(file)
    
    content = readContent(file)[0][1]
    writer.writerow([content])
