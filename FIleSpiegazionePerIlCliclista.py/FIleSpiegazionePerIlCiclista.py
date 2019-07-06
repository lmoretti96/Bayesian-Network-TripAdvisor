import pandas as pd
import numpy as np
import csv
import json
from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.pgmlearner import PGMLearner
from libpgm.tablecpdfactorization import TableCPDFactorization
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
#Defining formatting data method
def format_data(df):
    result = []
    for row in df.itertuples():
        #print(row.Pclass)
        result.append(dict(
          great = row.great, good = row.good, clean = row.clean,  comfortable = row.comfortable,
          bad = row.bad, old = row.old,
          Cleanliness= row.Cleanliness, Location=row.Location, Service=row.Service, Rooms=row.Rooms, 
          Value=row.Value, Overall=row.Overall 
        ))

            # beautiful = row.beautiful, wonderful = row.wonderful,     
            # Checkin=row.Checkin, Businessservice=row.Businessservice,
             #      result.append(dict(great = row.great, good = row.good, nice = row.nice, clean = row.clean, helpful = row.helpful, comfortable = row.comfortable,
       # beautiful = row.beautiful, wonderful = row.wonderful, friendly = row.friendly, fantastic = row.fantastic, bad = row.bad, 
      #   Cleanliness= row.Cleanliness, Location=row.Location ,Businessservice=row.Businessservice,
       #    Checkin=row.Checkin, Service=row.Service, Rooms=row.Rooms, Value=row.Value, Overall=row.Overall ))
    return result
#load all preprocessed training data
df = pd.read_csv('features.csv', sep=',')

#format data to let them correctly processed by libpgm functions
node_data = format_data(df)

skel = GraphSkeleton()
#load structure of our net
skel.load("./skel-learned2.txt")
#setting the topologic order
skel.toporder()
#learner which will estimate parameters e if needed net structure
learner = PGMLearner()

#estismting parameters for our own model
res = learner.discrete_mle_estimateparams(skel, node_data)

# get CPT
a = TableCPDFactorization(res)
#compute the query and evidences as dicts
query = dict(Overall=Overall)
# prepare dictionary of values (dopo gli uguali devi mettere i valori che leggi dalla GUI)
evidence = dict(Service = Service, Location = Location, Cleanliness = Cleanliness, Value = Value,bad=bad,Rooms=Rooms,old=old,good=good,great=great,comfortable=comfortable)

#run the query given evidence
result = a.condprobve(query, evidence)

# now you have all things you need. result.vals at index 0 rappresents the class 1, result.vals at index 1 rappresents the class 2 etc 
print json.dumps(result.vals, indent=2)