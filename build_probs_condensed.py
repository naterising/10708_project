# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:17:23 2024

@author: nater
"""

import pandas as pd
import csv

# create a new pandas df
df = pd.DataFrame(columns=['N','roll','p'])


###########################################
N=1
prob = (1/6)**N

for d in range(1,7):
    
    df.loc[len(df.index)] = [N, [d], prob] 
    roll = []
    
############################################
print("running twos")    
N=2
prob = (1/6)**N

roll_dict = dict()

rolls = [(i,j) for i in range (1,7) for j in range(1,7)]

for roll in rolls: 
    
    roll = tuple(sorted(roll))
    
    if roll in roll_dict:
        roll_dict[roll] += 1
        
    else:
        roll_dict[roll] = 1
    
for roll, count in roll_dict.items():
    
    df.loc[len(df.index)] = [N,list(roll),prob*count]
    
    
    
############################################

print("running threes")    
N=3
prob = (1/6)**N

roll_dict = dict()

rolls = [(i,j,k) for i in range (1,7) for j in range(1,7) for k in range(1,7)]

for roll in rolls:
    
    roll = tuple(sorted(roll))
    
    if roll in roll_dict:
        roll_dict[roll] += 1
        
    else:
        roll_dict[roll] = 1
    
for roll, count in roll_dict.items():
    df.loc[len(df.index)] = [N,list(roll),prob*count]
    
############################################

print("running fours")  
N=4
prob = (1/6)**N

roll_dict = dict()

rolls = [(i,j,k,l) for i in range (1,7) for j in range(1,7) for k in range(1,7) for l in range(1,7)]

for roll in rolls:
    roll = tuple(sorted(roll))
    
    if roll in roll_dict:
        roll_dict[roll] += 1
        
    else:
        roll_dict[roll] = 1    
        
for roll, count in roll_dict.items():
    df.loc[len(df.index)] = [N,list(roll),prob*count]        
        
############################################

print("running fives")
N=5
prob = (1/6)**N

roll_dict = dict()

rolls = [(i,j,k,l,m) for i in range (1,7) for j in range(1,7) for k in range(1,7) for l in range(1,7) for m in range(1,7)]

for roll in rolls:
    roll = tuple(sorted(roll))
    
    if roll in roll_dict:
        roll_dict[roll] += 1
        
    else:
        roll_dict[roll] = 1   
        
for roll, count in roll_dict.items():
    df.loc[len(df.index)] = [N,list(roll),prob*count]     
    
############################################

print("running sixes")
N=6
prob = (1/6)**N

roll_dict = dict()

rolls = [(i,j,k,l,m,n) for i in range (1,7) for j in range(1,7) for k in range(1,7) for l in range(1,7) for m in range(1,7) for n in range(1,7)]

for roll in rolls:
    roll = tuple(sorted(roll))
    
    if roll in roll_dict:
        roll_dict[roll] += 1
        
    else:
        roll_dict[roll] = 1   
        
for roll, count in roll_dict.items():
    df.loc[len(df.index)] = [N,list(roll),prob*count]    
    
##############################################

df.to_csv('dice_states_condensed.csv')
        
