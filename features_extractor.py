#!/usr/bin/env python


import re
import csv
import json
import os

def extract_features(file):
    #apro il file delle recensioni di un hotel
    with open('Dataset/Training/' + file, errors='ignore') as dat_file:
            data = dat_file.read()

    metadatas = ["Overall", "Value", "Rooms", "Location", "Cleanliness", "Check in / front desk", "Service", "Business service"]

    feature_words = good_keyworks + bad_keyworks

    #divido il file delle recensioni per ogni recensione eliminando il preambolo generale sull'hotel
    reviews = data.split('<Author>')
    reviews.pop(0)
    
    #creo il vettore feature per ogni recensione
    for review in reviews:
        listRev=[]
        current_features = {}

        #trovo il content della recensione
        content = re.compile('<Content>(.*)').findall(review)[0]

        #cerco se le keyword sono presenti nel content
        for keyword in feature_words:
            if re.search(keyword, content, re.IGNORECASE):
                current_features[keyword] = 1
            else:
                current_features[keyword] = 0

        #estraggo il valore dei metadati
        for metadata in metadatas:
            current_features[metadata] = re.compile('<' + metadata + '>(.*)').findall(review)[0]
        listRev.append(current_features)
        #print(str(current_features))
        #scrivo sull'output il vettore features
        output_file.write(json.dumps(current_features) + "\n")
        with open("output.csv","a+",newline="") as f:  # python 2: open("output.csv","wb")
            title = "great,good,nice,clean,excellent,helpful,comfortable,beautiful,wonderful,friendly,fantastic,bad,Overall,Value,Rooms,Location,Cleanliness,Check in / front desk,Service,Business service".split(",") # quick hack
            cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #cw.writeheader()
            cw.writerows(listRev)

#creo il file di output
output_file = open("reviews_output.csv", 'w')

#apro il file delle parole più frequenti buone e cattive
with open("keywords_prova.csv") as csv_file:
    keywords = csv.reader(csv_file,delimiter=",")
    good_keyworks = next(keywords)
    bad_keyworks = next(keywords)

#apro ad uno ad uno i file della cartella training
for file in os.listdir('Dataset/Training/'):
    print(file)
    extract_features(file)

output_file.close()