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
        result.append(dict(great = row.great, good = row.good, clean = row.clean,  comfortable = row.comfortable,
        beautiful = row.beautiful, wonderful = row.wonderful,  fantastic = row.fantastic, bad = row.bad, 
         Cleanliness= row.Cleanliness, Location=row.Location ,Businessservice=row.Businessservice,
           Checkin=row.Checkin, Service=row.Service, Rooms=row.Rooms, Value=row.Value, Overall=row.Overall ))
             #      result.append(dict(great = row.great, good = row.good, nice = row.nice, clean = row.clean, helpful = row.helpful, comfortable = row.comfortable,
       # beautiful = row.beautiful, wonderful = row.wonderful, friendly = row.friendly, fantastic = row.fantastic, bad = row.bad, 
      #   Cleanliness= row.Cleanliness, Location=row.Location ,Businessservice=row.Businessservice,
       #    Checkin=row.Checkin, Service=row.Service, Rooms=row.Rooms, Value=row.Value, Overall=row.Overall ))
    return result
#load all preprocessed training data
df = pd.read_csv('./features_filtrato.csv', sep=',')
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
print(str(res))


#estimating net structure given training data and paramenters this is an alternative to create a new model on our data
#net = learner.discrete_estimatebn(node_data)
#print json.dumps(net.V, indent=2)
#print json.dumps(net.E, indent=2)
#res = learner.discrete_mle_estimateparams(net, node_data)
#print(str(res))




#compute performances for each oveall score
for score in range(1,6):
    target = []
    pred = []
    #load testing dataset into a dataframe
    testdf = pd.read_csv("test-filtrato.csv",  sep = ",")
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
        small = int(testdf.iloc[i]["small"])
        bad = int(testdf.iloc[i]["bad"])
        old = int(testdf.iloc[i]["old"])
        Rooms = int(testdf.iloc[i]["Rooms"])
        Location = int(testdf.iloc[i]["Location"])
        Service = int(testdf.iloc[i]["Service"])
        Cleanliness = int(testdf.iloc[i]["Cleanliness"])
        CheckIn = int(testdf.iloc[i]["CheckIn"])
        Businessservice = int(testdf.iloc[i]["Businessservice"])
        Value = int(testdf.iloc[i]["Value"])
        Overall = int(testdf.iloc[i]["Overall"])
        #append the overall score to the target list
        target.append(Overall)
        #getting all cpt from our model
        a = TableCPDFactorization(res)
        #compute the query and evidences as dicts
        query = dict(Overall=Overall)
        evidence = dict(CheckIn=CheckIn,Businessservice=Businessservice,Service = Service, Location = Location, Cleanliness = Cleanliness, Value = Value, bad = bad, good = good, Rooms = Rooms, great =great, comfortable = comfortable, small = small, old = old)
        #run the query given evidence
        result = a.condprobve(query, evidence)
        #choose the max probability ditribution as model prediction
        maxvalue = max(result.vals)
        pos = result.vals.index(maxvalue)
        #append it to our prediction list
        pred.append(pos + 1)
        print(count)
        count = count + 1
    #print performances on the performances.csv file
    with open("performances.csv", "a") as f:
        f.write("ACCURACY of the "+str(score)+"th score: "+str(accuracy_score(target, pred))+'\n')
        f.write("PRECISION of the "+str(score)+"th score: "+str(precision_score(target, pred, average = 'macro'))+'\n')
        f.write("RECALL of the "+str(score)+"th score: "+str(recall_score(target, pred, average = 'macro'))+'\n')
        f.write("F-MEASURE of the "+str(score)+"th score: "+str(f1_score(target, pred, average = 'macro'))+'\n')