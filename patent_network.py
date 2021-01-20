# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 09:11:13 2021

@author: lenovo
"""


import json
import pandas as pd
import numpy as np
import networkx as nx



all_patents = []
with open('专利数据样例.json','r',encoding = 'utf_8_sig') as f:
    for line in f:
        all_patents.append(json.loads(line))



def cite_table(cite_patents,current_patent):

    cite_companylist = []
    dict_cite_companylist = {}
    for i in cite_patents:
        cite_company = i.get('申请人')
        for x in cite_company.split(';'):           
            cite_companylist.append(x)
            dict_cite_companylist = dict.fromkeys(cite_companylist, 1)    
                
    current_companylist = [] 
    try:
        current_company = current_patent['当前权利人']
        current_company = current_company.split(';')[0]            
        current_companylist.append(current_company)
    except:
        current_companylist = []
        

    df = pd.DataFrame([dict_cite_companylist],index = current_companylist)
    return df


i = 0
df = pd.DataFrame()
while i in range(len(all_patents)):
    x = all_patents[i].get('引证信息').get('引证专利')
    y = all_patents[i].get('基本信息')
    df1 = cite_table(x, y)
    i = i+1
    df = pd.concat([df,df1],join = 'outer')
    
    if i not in  range(len(all_patents)):
        break

df.fillna(0,inplace = True) 
df.index.names = ['company']
#df =  df.groupby('company').sum()



G = nx.Graph()
col_list1 = df.index.values.tolist()
col_list2 = df.columns.values.tolist()

j = 0
while (j in range(len(df.columns))):
    i = 0
    while (i in range(len(df))) :
        if df.iloc[i].iat[j] != 0:
            G.add_edge(col_list1[i],col_list2[j])
            i = i + 1
        else :
            if df.iloc[i].iat[j] == 0:
                pass
        if i not in range(len(df)):
            break
    j = j+1
    if j not in range(len(df.coloumns)):
        break

structurehole1  = nx.effective_size(G)

print (structurehole1 )       
        
    



                










