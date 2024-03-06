# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 18:25:45 2024

@author: nater
"""

import pandas as pd

df = pd.read_parquet('dice_states_condensed.parquet')

print("Orig DF len: "+str(len(df)))

# now, enumerate for value of accrued pts
orig_len = len(df)
accrued_states = list(range(0, 10001, 50))
accrued_pts_col  = [item for item in accrued_states for _ in range(orig_len)]

df_final = df.copy()
for _ in range(len(accrued_states)-1):
    df_final = pd.concat([df_final,df],ignore_index=True,axis=0)

print("Copied DF len: "+str(len(df_final)))
print("Accrued states len: "+str(len(accrued_pts_col)))

df_final['accrued'] = accrued_pts_col

df_final = df_final[['accrued','N','roll','p']]

df_final.to_parquet('dice_states_with_accrued.parquet', compression='snappy')
df_final.to_csv('dice_states_with_accrued.csv',index=False)