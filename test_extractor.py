#!/usr/bin/env python

import re
import csv
import json
import os

def extract_features(file):
    with open('test.csv', 'a', newline='') as output_file:
        #apro il file delle recensioni di un hotel
        with open('Dataset/Testing/' + file, errors='ignore') as dat_file:
                data = dat_file.read()

        #divido il file delle recensioni per ogni recensione eliminando il preambolo generale sull'hotel
        reviews = data.split('<Author>')
        reviews.pop(0)
        
        #creo il vettore feature per ogni recensione
        for review in reviews:
            current_features = {}

            #trovo il content della recensione
            content = re.compile('<Content>(.*)').findall(review)[0]
            valido=True
            #estraggo il valore dei metadati
            for metadata in metadatas:
                #print(metadata)
                current_features[metadata] = re.compile('<' + metadata + '>(.*)').findall(review)[0]
                if(str(current_features[metadata])=="-1"):
                    valido=False

            #cerco se le keyword sono presenti nel content
            for keyword in feature_words:
                if re.search(keyword, content, re.IGNORECASE):
                    current_features[keyword] = 1
                else:
                    current_features[keyword] = 0

            #scrivo i valori per ogni recensione
            if(valido==True):
                writer = csv.writer(output_file)
                writer.writerow(current_features.values())
        
#---------------------------------------------------------------------------------------------#
#main#

#lista dei metadati che voglio estrarre
metadatas = ["Overall", "Value", "Rooms", "Location", "Cleanliness", "Service"]
#,"Business service","Check in / front desk"]


#apro il file delle parole più frequenti buone e cattive
with open("keywords_prova.csv") as csv_file:
    keywords = csv.reader(csv_file,delimiter=",")
    good_keyworks = next(keywords)
    bad_keyworks = next(keywords)
feature_words = good_keyworks + bad_keyworks

#creo il file di output e stampo l'header
with open('test.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(feature_words + metadatas)
    #writer.writerow(metadatas)

#apro ad uno ad uno i file della cartella training
for file in os.listdir('Dataset/Testing/'):
    print(file)
    extract_features(file)
