import pandas as pd
import numpy as np
import csv
import json
from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.pgmlearner import PGMLearner
from libpgm.tablecpdfactorization import TableCPDFactorization

def fun(inputData):

    #Defining formatting data method
    def format_data(df):
        result = []
        for row in df.itertuples():
            #print(row.Pclass)
            result.append(dict(
            great = row.great, 
            good = row.good, 
            clean = row.clean,
            comfortable = row.comfortable,
            bad = row.bad, 
            old = row.old,
            Cleanliness= row.Cleanliness, Location=row.Location, Service=row.Service, 
            Rooms=row.Rooms, 
            Value=row.Value, 
            Overall=row.Overall))
        return result

    #load all preprocessed training data
    df = pd.read_csv('features.csv', sep=',')

    #format data to let them correctly processed by libpgm functions
    node_data = format_data(df)

    skel = GraphSkeleton()
    #load structure of our net
    skel.load("./our-skel.txt")
    #setting the topologic order
    skel.toporder()
    #learner which will estimate parameters e if needed net structure
    learner = PGMLearner()

    #estismting parameters for our own model
    res = learner.discrete_mle_estimateparams(skel, node_data)

    # get CPT
    a = TableCPDFactorization(res)
    #compute the query and evidences as dicts
    query = dict(Overall=1)
    # prepare dictionary of values (dopo gli uguali devi mettere i valori che leggi dalla GUI)
    
    evidence = dict(Value = inputData[0],
                    Location = inputData[1],
                    Cleanliness = inputData[2],
                    Service = inputData[3],
                    Rooms = inputData[4],
                    bad = inputData[5],
                    old = inputData[6],
                    good = inputData[7],
                    great = inputData[8],
                    comfortable = inputData[9],
                    clean = inputData[10]
                    )

    print(query)
    print(evidence)

    #run the query given evidence
    result = a.condprobve(query, evidence)

    print json.dumps(result.vals, indent=2)
    #res.Vdata["Overall"]["vals"][pos]
    #arr=[]
    dizionario={}
    for i in range(1,6):
        dizionario[res.Vdata["Overall"]["vals"][i-1]] = result.vals[i-1]
    #    arr.append(dizionario)
    #print(str(arr))
    return dizionario