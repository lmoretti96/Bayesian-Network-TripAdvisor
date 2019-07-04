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
      great = row.great, good = row.good, old=row.old,
      bad = row.bad, comfortable = row.comfortable,
      small=row.small, Cleanliness= row.Cleanliness, 
      Location=row.Location,
      Service=row.Service, Rooms=row.Rooms, Value=row.Value, 
      Overall=row.Overall 
    ))
  return result


# nice = row.nice, 
# beautiful = row.beautiful, wonderful = row.wonderful, 
# friendly = row.friendly,
# Businessservice=row.Businessservice,
# Checkin=row.Checkin, 
# helpful = row.helpful, comfortable = row.comfortable,

#load all preprocessed training data
df = pd.read_csv('./features.csv', sep=',')
#format data to let them correctly processed by libpgm functions
node_data = format_data(df)

skel = GraphSkeleton()
#load structure of our net
#skel.load("./json_skel.txt")
#setting the topologic order
#skel.toporder()
#learner which will estimate parameters e if needed net structure
learner = PGMLearner()

#estismting parameters for our own model
#res = learner.discrete_mle_estimateparams(skel, node_data)



#estimating net structure given training data and paramenters this is an alternative to create a new model on our data
net = learner.discrete_estimatebn(node_data)
print(json.dumps(net.V, indent=2))
print(json.dumps(net.E, indent=2))
res = learner.discrete_mle_estimateparams(net, node_data)
print(str(res))