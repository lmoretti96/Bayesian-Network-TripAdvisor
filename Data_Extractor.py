import re
import os

def readContent(file):
    with open('Dataset/Training/' + file, errors='ignore') as dat_file:
        data = dat_file.read()
    regex = re.compile('(<Content>)(.*)')
    results = regex.findall(data)
    for result in results:
        file_out.write(result[1] + "\n")

file_out = open("contents_only.txt", 'w')

for file in os.listdir('Dataset/Training/'):
    print(file)
    readContent(file)

file_out.close()



