# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:39:05 2024

@author: nater
"""

import pandas as pd
import csv

# create a new pandas df
df = pd.DataFrame(columns=['N','roll','p'])


###########################################
N=1
prob = (1/6)**N

roll=[]
for d in range(1,7):
    roll.append(d)
    
    df.loc[len(df.index)] = [N, roll, prob] 
    roll = []
    
############################################
print("running twos")    
N=2
prob = (1/6)**N

rolls = [(i,j) for i in range (1,7) for j in range(1,7)]

roll = []
for roll in rolls:
    df.loc[len(df.index)] = [N,list(roll),prob]
    
############################################
print("running threes")    
N=3
prob = (1/6)**N

rolls = [(i,j,k) for i in range (1,7) for j in range(1,7) for k in range(1,7)]

roll = []
for roll in rolls:
    df.loc[len(df.index)] = [N,list(roll),prob]
    
############################################
print("running fours")  
N=4
prob = (1/6)**N

rolls = [(i,j,k,l) for i in range (1,7) for j in range(1,7) for k in range(1,7) for l in range(1,7)]

roll = []
for roll in rolls:
    df.loc[len(df.index)] = [N,list(roll),prob]
    
############################################
print("running fives")
N=5
prob = (1/6)**N

rolls = [(i,j,k,l,m) for i in range (1,7) for j in range(1,7) for k in range(1,7) for l in range(1,7) for m in range(1,7)]

roll = []
for roll in rolls:
    df.loc[len(df.index)] = [N,list(roll),prob]
    
############################################

print("running sixes")
N=6
prob = (1/6)**N

rolls = [(i,j,k,l,m,n) for i in range (1,7) for j in range(1,7) for k in range(1,7) for l in range(1,7) for m in range(1,7) for n in range(1,7)]

roll = []
for roll in rolls:
    df.loc[len(df.index)] = [N,list(roll),prob]
    
##############################################

df.to_parquet('dice_states.parquet', compression='snappy')
        
