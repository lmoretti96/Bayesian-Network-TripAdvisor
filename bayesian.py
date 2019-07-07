import pandas as pd
import numpy as np
import csv
import json
from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.pgmlearner import PGMLearner
from libpgm.tablecpdfactorization import TableCPDFactorization
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork




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
skel.load("./skel-learned.txt")
#setting the topologic order
skel.toporder()
#learner which will estimate parameters e if needed net structure
learner = PGMLearner()


#estismting parameters for our own model
res = learner.discrete_mle_estimateparams(skel, node_data)


"""
#estimating net structure given training data and paramenters this is an alternative to create a new model on our data
net = learner.discrete_estimatebn(node_data)

with open("reteTestMeta.csv", "a") as gv:
  gv.write(json.dumps(net.V, indent=2))
  gv.write(json.dumps(net.E, indent=2))  
res = learner.discrete_mle_estimateparams(net, node_data)
with open("modelloMeta.csv", "a") as gv:
  gv.write(json.dumps(res.E, indent=2))
  gv.write(json.dumps(res.Vdata, indent=2))  
"""
#compute performances for each oveall score
for score in range(1,6):
    target = []
    pred = []
    #load testing dataset into a dataframe
    testdf = pd.read_csv("test.csv",  sep = ",")
    #selecting row with a certain overall value
    testdf = testdf[testdf["Overall"] == score]
    print(len(testdf))
    count = 0
    #for every test record
    for i in range (0, len(testdf)):
        #extract features
        great = int(testdf.iloc[i]["great"])
        good = int(testdf.iloc[i]["good"])
        comfortable = int(testdf.iloc[i]["comfortable"])
        clean = int(testdf.iloc[i]["clean"])
        # # small = int(testdf.iloc[i]["small"])
        bad = int(testdf.iloc[i]["bad"])
        old = int(testdf.iloc[i]["old"])
        Rooms = int(testdf.iloc[i]["Rooms"])
        Location = int(testdf.iloc[i]["Location"])
        Service = int(testdf.iloc[i]["Service"])
        Cleanliness = int(testdf.iloc[i]["Cleanliness"])
        #Checkin = int(testdf.iloc[i]["Checkin"])
        #Businessservice = int(testdf.iloc[i]["Businessservice"])
        Value = int(testdf.iloc[i]["Value"])
        Overall = int(testdf.iloc[i]["Overall"])
        #append the overall score to the target list
        target.append(Overall)
        #getting all cpt from our model
        a = TableCPDFactorization(res)
        #compute the query and evidences as dicts
        query = dict(Overall=Overall)
        evidence = dict(Service = Service, Location = Location, Cleanliness = Cleanliness, Value = Value,bad=bad,Rooms=Rooms,old=old,good=good,great=great,comfortable=comfortable)
        #Checkin=Checkin,Businessservice=Businessservice 
        #run the query given evidence
        result = a.condprobve(query, evidence)
        #result2 = a.specificquery(query, evidence)
        #print(result2)
        #print json.dumps(result.vals, indent=2)
        #choose the max probability ditribution as model prediction
        maxvalue = max(result.vals)

        pos = result.vals.index(maxvalue)
        pos= res.Vdata["Overall"]["vals"][pos]
        #append it to our prediction list
        pred.append(pos)
        print(count)
        count = count + 1
    #print performances on the performances.csv file
    with open("performancesLearned.csv", "a") as f:
        f.write("ACCURACY of the "+str(score)+"th score: "+str(accuracy_score(target, pred))+'\n')
        f.write("PRECISION of the "+str(score)+"th score: "+str(precision_score(target, pred, average = 'macro'))+'\n')
        f.write("RECALL of the "+str(score)+"th score: "+str(recall_score(target, pred, average = 'macro'))+'\n')
        f.write("F-MEASURE of the "+str(score)+"th score: "+str(f1_score(target, pred, average = 'macro'))+'\n')