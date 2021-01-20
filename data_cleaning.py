
"""
Created on Wed Jan  6 09:27:27 2021

@author: lenovo"""

import numpy as np 
import pandas as pd
from pandas import Series,DataFrame
from datetime import datetime
import re
import math
import json

def getNum(x):
    """
    科学计数法和字符转浮点数
    """
    if re.findall(r'\d+\.\d+E\+',x):
        return "%.f" % float(x)
    elif x=="C":
        return 1
    else:
        return x 

def turn_dtype(x,y):
    x[y] = x[y].astype("str")
    x[y] = x[y].apply(getNum)
    x[y] = pd.to_numeric(x[y])
    x[y] = x[y].astype("float64")
    return x

def turn_dtype_int(x,y):
    x[y] = x[y].astype("str")
    x[y] = x[y].apply(getNum)
    x[y] = pd.to_numeric(x[y])
    x[y] = x[y].astype("int32")
    return x





Public_Company =pd.read_csv("public_company.csv",encoding = 'gbk')
turn_dtype(Public_Company, 'Symbol')
col_n = ['Symbol']
Public_Company = pd.DataFrame(Public_Company,columns = col_n)
    
#-----------------------------------------------------------------


df = pd.read_csv("research_invest.csv",encoding = 'gbk')
col_n = ['Symbol','RDSpendSumRatio']
df = pd.DataFrame(df,columns = col_n)
df = df.drop(labels = 0)
df = df.drop(labels = 1)
df = df.dropna(axis=0, how='any', inplace=False)

turn_dtype(df, 'RDSpendSumRatio')
turn_dtype(df, 'Symbol')
df = pd.merge(df,Public_Company,on = 'Symbol')


RD_Spend_Ratio = df['RDSpendSumRatio'].groupby(df['Symbol']).mean()
RD_Spend_Ratio.to_csv('1.1.1 RD_Spend_Proportion.csv')


#-----------------------------------------------------------------



df = pd.read_csv("research_invest.csv",encoding = 'gbk')
col_n = ['Symbol','EndDate','RDSpendSum']
df = pd.DataFrame(df,columns = col_n)
df = df.drop(labels = 0)
df = df.drop(labels = 1)
df = df.dropna(axis=0, how='any', inplace=False)
df = df.dropna(axis=0, how='any', inplace=False)
df['EndDate'] = df['EndDate'].astype('datetime64[ns]')
RD_Spend_Sum = df [df.EndDate == '2019-12-31' ]
turn_dtype(RD_Spend_Sum, 'Symbol')
turn_dtype(RD_Spend_Sum, 'RDSpendSum')
col_n = ['Symbol','RDSpendSum']
RD_Spend_Sum = pd.DataFrame(RD_Spend_Sum,columns = col_n)
RD_Spend_Sum = pd.merge(RD_Spend_Sum,Public_Company, on = 'Symbol')

per = pd.read_csv('person.csv',encoding = 'gbk')
per = pd.DataFrame(per)
per.columns=['Symbol','EndDate','Person']
per = per.drop(labels = 0)
per = per.drop(labels = 1)
per = per.dropna(axis=0, how='any', inplace=False)
per['EndDate'] = per['EndDate'].astype('datetime64[ns]')
per = per [per.EndDate == '2019-12-31']
turn_dtype(per, 'Symbol')
turn_dtype(per, 'Person')
col_n = ['Symbol','Person']
Person = pd.DataFrame(per,columns = col_n)
Person = pd.merge(Person,Public_Company, on = 'Symbol')

merge = pd.merge(RD_Spend_Sum,Person,on = 'Symbol',how = 'outer')
merge['Per_RD_Spend'] = merge.apply(lambda x: x['RDSpendSum']/x['Person'], axis=1)
col_n = ['Symbol','Per_RD_Spend']
merge = pd.DataFrame(merge,columns = col_n)


Spend_person = pd.merge(merge,Public_Company,on = 'Symbol')

Spend_person.to_csv('1.1.2 Per_RD_Spend.csv')



#-----------------------------------------------------------------

df = pd.read_csv("research_invest.csv",encoding = 'gbk')
col_n1 = ['Symbol','RDPersonRatio']
    
df = pd.DataFrame(df,columns = col_n1)
df = df.drop(labels = 0)
df = df.drop(labels = 1)
df = df.fillna({'RDPersonRatio':0})

turn_dtype(df, 'Symbol')
turn_dtype(df, 'RDPersonRatio')
df = pd.merge(df,Public_Company,on = 'Symbol')

RD_Person_Proportion = df['RDPersonRatio'].groupby(df['Symbol']).mean()
RD_Person_Proportion.to_csv('1.2.1 RD_Person_Proportion.csv')

#-----------------------------------------------------------------


df = pd.read_csv("RD_person_equity.csv",encoding = 'gbk')
df.columns=['code','EventID','Symbol','Date','RD_person_equity']
col_n1 = ['Symbol','RD_person_equity']
df = pd.DataFrame(df,columns = col_n1)
df = df.drop(labels = 0)
df = df.drop(labels = 1)
df = df.fillna({'RD_person_equity':0})

turn_dtype(df, 'Symbol')
turn_dtype(df, 'RD_person_equity')

grouped1 = df['RD_person_equity'].groupby(df['Symbol']).mean()
grouped2 = df['RD_person_equity'].groupby(df['Symbol']).count()

df = grouped1*grouped2

df.reset_index()

RD_person_equity = pd.merge(df,Public_Company,on = 'Symbol')

RD_person_equity.to_csv('1.3.1 RD_person_equity.csv')

#-----------------------------------------------------------------

df = pd.read_csv("patents.csv",engine = 'python',encoding = 'gb18030')
col_n = ['股票代码','专利分类号']
df = pd.DataFrame(df,columns = col_n)
df.rename(columns = {'股票代码':'Symbol','专利分类号':'patents'},inplace = True)

df = df['patents'].groupby(df['Symbol']).count()


df = df.reset_index()
df = pd.merge(df,Public_Company, on = 'Symbol')


Sum_patents = np.sum(df.patents[1:])
df['Patents_ratio'] = df.apply(lambda x : x['patents']/Sum_patents,axis =1 )

col_n = ['Symbol','Patents_ratio']
Patents_ratio = pd.DataFrame(df,columns = col_n)

Patents_ratio.to_csv('2.1.1 Patents_ratio.csv')


#-----------------------------------------------------------------


df = pd.read_csv("patents.csv",engine = 'python',encoding = 'gb18030')
col_n = ['股票代码','专利分类']
df = pd.DataFrame(df,columns = col_n)
df.rename(columns = {'股票代码':'Symbol','专利分类':'patents_type'},inplace = True)
df = df.loc[df['patents_type'] == 1 ]

grouped = df['patents_type'].groupby(df['Symbol']).count()
df = grouped
df = df.reset_index()
df = pd.merge(df,Public_Company, on = 'Symbol')


Sum_inventions = np.sum(df.patents_type[1:])
df['inventions_ratio'] = df.apply(lambda x : x['patents_type']/Sum_inventions,axis =1 )

col_n = ['Symbol','inventions_ratio']
Inventions_ratio = pd.DataFrame(df,columns = col_n)

Inventions_ratio.to_csv('2.1.2 inventions_ratio.csv')

#-----------------------------------------------------------------



df = pd.read_csv("patents.csv",engine = 'python',encoding = 'gb18030')
col_n = ['股票代码','专利分类号']
df = pd.DataFrame(df,columns = col_n)
df.rename(columns = {'股票代码':'Symbol','专利分类号':'patents'},inplace = True)

df = df['patents'].groupby(df['Symbol']).count()

df = df.reset_index()

Sum_patents = pd.merge(df,Public_Company, on = 'Symbol')
Person = pd.merge (Person,Public_Company , on = "Symbol")

merge = pd.merge(Sum_patents,Person,on = 'Symbol')
merge['Patents_person'] = merge.apply(lambda x: x['patents']/x['Person'], axis=1)
col_n = ['Symbol','Patents_person']
Patents_person = pd.DataFrame(merge,columns = col_n)

Patents_person.to_csv('2.1.3 Per_Patents.csv')



#-------------------------------------------------------------------


df = pd.read_csv('innovation_output.csv',engine = 'python',encoding = 'gbk')
col_n = ['股票代码','年份','创新产出-软件著作权(个)']
df = pd.DataFrame(df,columns = col_n)
df = df.rename(columns = {'股票代码':'Symbol','年份':'Date','创新产出-软件著作权(个)':'Software_Copyrights'},inplace = False)
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
df =  df[df.Date == 2019]

df = df['Software_Copyrights'].groupby(df['Symbol']).mean()
df = df.reset_index()
df = pd.merge(df,Public_Company, on = 'Symbol')

Sum_Software_Copyrights = np.sum(df.Software_Copyrights[1:])
df['Software_Copyright_ratio'] = df.apply(lambda x : x['Software_Copyrights']/Sum_Software_Copyrights,axis =1 )

col_n = ['Symbol','Software_Copyright_ratio']
Software_Copyright_ratio = pd.DataFrame(df,columns = col_n)

Software_Copyright_ratio.to_csv('3.1.1 Software_Copyright_ratio.csv')

#-----------------------------------------------------------------


df = pd.read_csv('innovation_output.csv',engine = 'python',encoding = 'gbk')
col_n1 = ['股票代码','年份','创新产出-获奖-国家(个)','创新产出-获奖-省级(个)']
df = pd.DataFrame(df,columns = col_n1)
df = df.rename(columns = {'股票代码':'Symbol','年份':'Date','创新产出-获奖-国家(个)':'awards1','创新产出-获奖-省级(个)':'awards2'},inplace = False)
df = df [df.Date == 2019]

df['awards'] = df.apply(lambda x: x['awards1'] + x['awards2'], axis=1)
col_n = ['Symbol','awards']
df = pd.DataFrame(df,columns = col_n )


turn_dtype(df,'awards')
turn_dtype(df,'Symbol')
RD_Awards = pd.merge (df, Public_Company, on = 'Symbol')
RD_Awards.to_csv('3.2.1 RD_Awards.csv')

#-----------------------------------------------------------------

df1 = pd.read_csv('balance_sheet.csv',engine = 'python',encoding = 'gbk')
df2 = pd.read_csv('profit_statement.csv',engine = 'python',encoding = 'gbk')
df1 = df1.rename(columns = {'证券代码':'Symbol'})
df2 = df2.rename(columns = {'证券代码':'Symbol'})
df = pd.merge(df1,df2,on = 'Symbol')
df = df.fillna(0)

df['Qi'] = df.apply(lambda x: np.log(x['固定资产清理(元)']+x['应付职工薪酬(元)']+ x['应交税费(元)']
       +x['其中：应付利息(元)']+x['资产减值损失(元)']+x['公允价值变动收益(元)']+x['投资收益(元)']
       +x['汇兑收益(元)']+x['营业利润(元)']), axis=1)
df['Ki'] = df.apply(lambda x: np.log(x['固定资产(元)']),axis =1)
df['Li'] = Person.apply(lambda x: np.log(x['Person']),axis =1)
col_n = ['Symbol','Qi','Ki','Li']
df = pd.DataFrame(df,columns = col_n )
df.fillna(0,inplace = True)

turn_dtype(df, 'Qi')
turn_dtype(df, 'Ki')
turn_dtype(df, 'Li')
turn_dtype(df, 'Symbol')

merge = pd.merge(df,Public_Company, on = 'Symbol')
merge['Output_diviation_value'] = merge.apply(lambda x : x['Qi'] - 23.44 + 0.5591*x['Ki'] +
                                        0.3224*x['Li'] - 0.02152*x['Ki']**2 - 0.04662*x['Li']**2
               + 0.01134*x['Ki']*x['Li'],axis =1)

col_n = ['Symbol','Output_diviation_value']
Output_diviation_value = pd.DataFrame(merge,columns = col_n )
Output_diviation_value.to_csv('3.3.1 Output_diviation_value.csv')

#--------------------------------------------------------------------------



with open("会议.json",'r',encoding = 'utf_8_sig') as f:
    p1 = json.load(f)
with open("学术期刊.json",'r',encoding = 'utf_8_sig') as f:
    p2 = json.load(f)

df1 = pd.DataFrame(p1)
df2 = pd.DataFrame(p2)
df = df1.append(df2)


def parse_author_school(author_list):
    num = 0
    for author in author_list:
        department = author.get("机构","")
        department = str(department)
        if u"大学" in department:
            num = num + 1
    return num    


df = pd.DataFrame(df, columns = ['作者','篇名','公司名'])
df = df.rename(columns = {'作者':'author','篇名':'paper','公司名':'Company'},inplace = False)
df['cooperations'] = df["author"].map(parse_author_school)

col_n = ['Company','cooperations']
df = pd.DataFrame(df,columns = col_n)

df = df.loc[df["cooperations"] != 0 ]
df = df['cooperations'].groupby(df['Company']).count()


Public_Company1 =pd.read_csv("public_company.csv",encoding = 'gbk')
df = pd.merge(df,Public_Company1,on = 'Company')


Sum_Cooperate_Papers = np.sum(df.cooperations[1:])
df['Cooperate_Paper_ratio'] = df.apply(lambda x : x['cooperations']/Sum_Cooperate_Papers,axis =1 )
col_n = ['Symbol','Cooperate_Paper_ratio']
Cooperate_Paper_ratio = pd.DataFrame(df,columns = col_n)

Cooperate_Paper_ratio.to_csv('4.3.1 Cooperate_Paper_ratio.csv',encoding = 'utf_8_sig')

#--------------------------------------------------------------------------


df = pd.read_csv('financial_funds.csv',engine = 'python',encoding = 'gbk')

col_n1 = ['股票代码','年份','科技创新补助金额(元)']
df = pd.DataFrame(df,columns = col_n1)
df = df.rename(columns = {'股票代码':'Symbol','年份':'Date','科技创新补助金额(元)':'Financial_Funds'},inplace = False)


df = df [df.Date == 2019]
col_n = ['Symbol','Financial_Funds']
df = pd.DataFrame(df,columns = col_n )
turn_dtype(df,'Financial_Funds')
turn_dtype(df,'Symbol')
Financial_Funds = pd.merge (df, Public_Company, on = 'Symbol')


df = pd.merge(Financial_Funds,RD_Spend_Sum,on = 'Symbol')
df['Financial_Fund_Proportion'] = df.apply(lambda x : x['Financial_Funds']/x['RDSpendSum'],axis =1 )

col_n1 = ['Symbol','Financial_Fund_Proportion']
df = pd.DataFrame(df,columns = col_n1)

df.to_csv('4.4.1 Financial_Fund_Proportion.csv')


#-----------------------------------------------------------------




df = pd.read_csv("OFDI_earning_proportion.csv",encoding = 'gbk')

col_n1 = ['Symbol','EarningsProportion']
df = pd.DataFrame(df,columns = col_n1)
df = df.fillna({'EarningsProportion':0})

turn_dtype(df, 'Symbol')
turn_dtype(df, 'EarningsProportion')

grouped = df['EarningsProportion'].groupby(df['Symbol']).mean()

df = grouped

df.reset_index()

EarningsProportion = pd.merge(df,Public_Company,on = 'Symbol')

EarningsProportion.to_csv('5.1.1 OFDI_Earnings_Proportion.csv')


#-----------------------------------------------------------------

df = pd.read_csv("OFDI_ralatedparty.csv",encoding = 'gbk')
col_n1 = ['Symbol','RelationshipID']
df = pd.DataFrame(df,columns = col_n1)
df.rename(columns = {'RelationshipID':'RalatedParty_count'},inplace = True)


turn_dtype(df, 'Symbol')
turn_dtype(df, 'RalatedParty_count')

df = df['RalatedParty_count'].groupby(df['Symbol']).count()

df.reset_index()
df = pd.merge(df,Public_Company,on = 'Symbol')

Sum_RelatedParty = np.sum(df.RalatedParty_count[1:])
df['RelatedParty_ratio'] = df.apply(lambda x : x['RalatedParty_count']/Sum_RelatedParty,axis =1 )
col_n = ['Symbol','RelatedParty_ratio']
RelatedParty_ratio = pd.DataFrame(df,columns = col_n)

RelatedParty_ratio.to_csv('5.1.2 OFDI_RelatedParty_ratio.csv')



#-----------------------------------------------------------------

df = pd.read_csv('cooperate_project.csv',engine = 'python',encoding = 'gbk')
df = df['project'].groupby(df['Company']).count()

Public_Company1 =pd.read_csv("public_company.csv",encoding = 'gbk')
df = pd.merge(df,Public_Company1,on = 'Company')

Sum_project = np.sum(df.project[1:])
df['ODFI_Cooperate_project_ratio'] = df.apply(lambda x : x['project']/Sum_project,axis =1 )


col_n = ['Symbol','ODFI_Cooperate_project_ratio']
df = pd.DataFrame(df,columns = col_n)

df.to_csv('5.1.3 ODFI_Cooperate_project_ratio.csv')





#-----------------------------------------------------------------

df = pd.read_csv("patents.csv",engine = 'python',encoding = 'gbk')
col_n1 = ['股票代码','国际申请']
df = pd.DataFrame(df,columns = col_n1)
df.rename(columns = {'股票代码':'Symbol','国际申请':'PCTs'},inplace = True)
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)


df= df['PCTs'].groupby(df['Symbol']).count()
df = pd.merge(df,Public_Company,on = 'Symbol')

Sum_PCTs = np.sum(df.PCTs[1:])
df['PCTs_ratio'] = df.apply(lambda x : x['PCTs']/Sum_PCTs,axis =1 )


col_n = ['Symbol','PCTs_ratio']
df = pd.DataFrame(df,columns = col_n)


df.to_csv('5.2.1 PCT_ratio.csv')


#-------------------------------------------------------------------




















