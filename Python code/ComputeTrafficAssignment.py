''' This code has been developed by Ashkan Fouladi (fooladiashkang@gmail.com) and
 Vahid Noroozi (vahidnoroozi1994@yahoo.com)'''
 
 
 
''' 1) This program calculates the flow of each link based on
UE.
2) A classical traffic assignment method, Frank-Wolfe, 
has been applied to this program.

3)To run this program, the user must input demand and network
CSV files.

4) In the setting section user could define
the precision of stop criteria and the maximum cycle number

5) This program provides two CSV files as an output;
first travel time and flow and second The total cost and 
relative gap for each iteration  '''





# Modules
import numpy as np
import csv 
import networkx as nx
import math
import matplotlib.pyplot as plt
import sympy
from sympy import S,ConditionSet
from sympy.solvers import solve
# Variables
previousTotalCost=0

# Setting
nCycle = 500
relativeGapAccuracy = 1E-4

# Functions

# This function gets data from demand and network files (CSV)
def import_network(network_file_path,demand_file_path):
    with open(network_file_path) as f:
        content=csv.reader(f)
        nodeList=[]
        for row in content:
            nodeList.append(row[0])
            nodeList.append(row[1])
    for i in range(0,len(nodeList)):
        nodeList[i]=int(nodeList[i])
    n=max(nodeList)
    x=np.zeros((n,n))
    y=np.zeros((n,n))
    z=np.zeros((n,n))
    w=np.zeros((n,n))
    with open(network_file_path) as f:
        content=csv.reader(f)
        for row in content:
            x[int(row[0])-1][int(row[1])-1]=1
            y[int(row[0])-1][int(row[1])-1]=float(row[2])
            z[int(row[0])-1][int(row[1])-1]=float(row[3])
    with open(demand_file_path) as f:
        content=csv.reader(f)
        for row in content:
            if row[2]!='':
                w[int(row[0])-1][int(row[1])-1]=float(row[2])      
    return n,x,y,z,w

# This function creates an n*n array of zero
def createArray(n):
    x=np.zeros((n,n))
    return x

# This function calculates the travel time of links based on the BPR function
# BPR function is defined as below:
    # t = a0[1+a1*(x^4)]
def linkTimeCalculator(x,t,a0,a1,n):
    for i in range(0,n):
        for j in range(0,n):
            t[i][j]=a0[i][j]*(1+a1[i][j]*(x[i][j])**4)
# This function creates the graph of link-time
def timeGraphGenerator(narr,t):
    b=narr*t
    tg=nx.DiGraph(b)
    return tg
# This function creates the auxiliary vector (y)
def auxiliaryVectorGenerator(tg,y,da,n):
    for w in range(0,n):
        for z in range(0,n):
            y[w][z]=0
    for i in range(0,n):
        for j in range(0,n):
            if da[i][j]!=0:
                a=list(nx.shortest_path(tg,source=i,target=j,weight='weight'))
                for k in range(1,len(a)):
                    y[a[k-1]][a[k]]+=da[i][j]
 # This function finds step-size                   
def findAlpha(x,y,a0,a1,n):
    z=sympy.symbols('z')
    expr=0
    for i in range(0,n):
        for j in range(0,n):
            expr+=(y[i][j]-x[i][j])*a0[i][j]*(1+a1[i][j]*(x[i][j]+z*(y[i][j]-x[i][j]))**4)
    sol=solve(expr,z,force=True)
    answer=0
    for i in range(0,len(sol)):
        if sol[i] in ConditionSet(z,(z>=0) & (z<1),S.Reals):
            answer=float(sol[i]) 
    return answer   
# This function calculates the flow of each link
def linkFlowCalculator(a,x,y,n):
    for i in range(0,n):
        for j in range(0,n):
            x[i][j]=x[i][j]+a*(y[i][j]-x[i][j]) 
# This function calculates the totalCost 
def totalCostCalculator(pre,x,t,n):
    tc=0
    for i in range(0,n):
        for j in range(0,n):
            tc+=x[i][j]*t[i][j] 
    rg=(pre-tc)/tc
    return tc,rg
# This function reports the travel time & the flow for each link
def reportFlow(file_path,n,narr,x,t):
    with open(file_path,'w',newline='') as f:
        myheader=['init_node','term_node','flow','travel time']
        content=csv.DictWriter(f,fieldnames=myheader)
        content.writeheader()
        for i in range(0,n):
            for j in range(0,n):
                if narr[i][j]==1:
                    content.writerow({'init_node':i+1,'term_node':j+1,'flow':x[i][j],'travel time':t[i][j]})
# This function reports the total cost & the relative gap for every iteration
def reportTotalCost(file_path,rg,tc,i):
    with open(file_path,'a',newline='') as f:
        myheader=['iteration','total cost','RG Gap']
        content=csv.DictWriter(f,fieldnames=myheader)
        if i==0:
            content.writeheader()
        content.writerow({'iteration':i,'total cost':tc,'RG Gap':abs(rg)})
def main():
    for i in range(0,nCycle):
        if i==0:
            (node_number,networkArray,a0Array,a1Array,demandArray)=import_network('C://Users/Asus/Desktop/personal/Networks/Anaheim/Network.csv','C://Users/Asus/Desktop/personal/Networks/Anaheim/Demand.csv')
            linkFlow=createArray(node_number)
            linkTime=createArray(node_number)
            auxiliaryVector=createArray(node_number)
            linkTimeCalculator(linkFlow, linkTime, a0Array, a1Array,node_number)
            timeGraph=timeGraphGenerator(networkArray,linkTime)
            auxiliaryVectorGenerator(timeGraph,linkFlow,demandArray,node_number)
            (totalCost,RG)=totalCostCalculator(previousTotalCost,linkFlow,linkTime,node_number)
            reportTotalCost('C://Users/Asus/Desktop/personal/Networks/Anaheim/TotalCost.csv',RG,totalCost,i)
        else:
            linkTimeCalculator(linkFlow, linkTime, a0Array, a1Array,node_number)
            timeGraph=timeGraphGenerator(networkArray,linkTime)
            auxiliaryVectorGenerator(timeGraph,auxiliaryVector,demandArray,node_number)
            alpha=findAlpha(linkFlow,auxiliaryVector,a0Array,a1Array,node_number)
            linkFlowCalculator(alpha,linkFlow,auxiliaryVector,node_number) 
            (totalCost,RG)=totalCostCalculator(totalCost,linkFlow,linkTime,node_number)
            reportTotalCost('C://Users/Asus/Desktop/personal/Networks/Anaheim/TotalCost.csv',RG,totalCost,i)
            print('\niteration number: ',i,'alpha= %.5f' %alpha,'The total cost is= %.5f' %totalCost)
            if RG>=0 and RG<relativeGapAccuracy:
                break
    reportFlow('C://Users/Asus/Desktop/personal/Networks/Anaheim/Flow.csv',node_number,networkArray,linkFlow,linkTime)   
main()



        
