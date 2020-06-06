#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 17:35:17 2020

@author: paddy IIT Mandi
"""

"""
For handling the COAP formats and stuff.
This code will:
1. Read the full shortlisted file and sort in the order required
2. This will be saved as new files (with _sorted filename suffix)
3. From _sorted files, pick up the relevant columns as per COAP
4. Modify the Gate number to remove category code
5. Form the final file with category wise data for a particular program.
"""
import pandas as pd

def processCoapFormat(df):
    # get info from df
    coapColumns = ['ApplicationNo','SubmissionDate','GATENo','RegistrationNo','EntranceScore','Name','CasteCategoryName']
    dfCoap = df[coapColumns].copy()
    # add additional fields as needed
    numRows = len(dfCoap.ApplicationNo)
    print('Num rows: ' + str(numRows))
    srAppStatus = pd.Series(['Pending']*numRows,index=df.index)
    srRemarks = pd.Series(['']*numRows,index=df.index)
    srOfferedProgram = pd.Series([strProgramName]*numRows,index=df.index)
    srRoundNum = pd.Series(['']*numRows,index=df.index)
    srInstiName = pd.Series(['']*numRows,index=df.index)
    srInstiId = pd.Series(['']*numRows,index=df.index)
    srInstiType = pd.Series(['']*numRows,index=df.index)
    dfCoap['AppStatus'] = srAppStatus
    dfCoap['Remarks'] = srRemarks
    dfCoap['OfferedPgm'] = srOfferedProgram
    dfCoap['RoundNum'] = srRoundNum
    dfCoap['InstiName'] = srInstiName
    dfCoap['InstiId'] = srInstiId
    dfCoap['InstiType'] = srInstiType
    return dfCoap



def processGateNumber(df):
    # Need to remove subject code from Gate number
    # Need to handle one by one
    for i in df.index:
        foo = (df['GATENo'][i]).strip()
        if foo[0:2].isalpha():
            df['GATENo'][i] = foo[2:]
    return df











# datafiles
dataDir = '/home/paddy/laptopLocal/localWork/msPhDAug2020/MTech_shortlisting/mtech_process/output/'
genDataFile = dataDir + 'power_genObccl.xls'
obcDataFile = dataDir + 'power_obcNcl.xls'
scDataFile = dataDir + 'power_sc.xls'
stDataFile = dataDir + 'power_st.xls'
ewsDataFile = dataDir + 'power_ews.xls'
pdDataFile = dataDir + 'power_pd.xls'

strProgramName = 'MTech'
# seat matrix
genCount = 17
obcCount = 10
scCount = 6
stCount = 3
ewsCount = 2
pdCount = 2
outDir = '/home/paddy/laptopLocal/localWork/msPhDAug2020/MTech_shortlisting/mtech_process/output/'
outfile = outDir + 'scee_power_coap_list.xls'

dfGen = pd.read_excel(genDataFile)
dfObc = pd.read_excel(obcDataFile)
dfSc = pd.read_excel(scDataFile)
dfSt = pd.read_excel(stDataFile)
dfEws = pd.read_excel(ewsDataFile)
dfPd = pd.read_excel(pdDataFile)
print('Loaded data files...')

dfGen.sort_values(by=['EntranceScore','NewCGPA'],ascending=False,inplace=True)
dfObc.sort_values(by=['EntranceScore','NewCGPA'],ascending=False,inplace=True)
dfSc.sort_values(by=['EntranceScore','NewCGPA'],ascending=False,inplace=True)
dfSt.sort_values(by=['EntranceScore','NewCGPA'],ascending=False,inplace=True)
dfEws.sort_values(by=['EntranceScore','NewCGPA'],ascending=False,inplace=True)
dfPd.sort_values(by=['EntranceScore','NewCGPA'],ascending=False,inplace=True)
print('Done sorting...')

dfCoapGen = processCoapFormat(dfGen)
dfCoapObc = processCoapFormat(dfObc)
dfCoapSc = processCoapFormat(dfSc)
dfCoapSt = processCoapFormat(dfSt)
dfCoapEws = processCoapFormat(dfEws)
dfCoapPd = processCoapFormat(dfPd)

print('Starting Gate code fixing')
dfCoapGen = processGateNumber(dfCoapGen)
dfCoapObc = processGateNumber(dfCoapObc)
dfCoapSc = processGateNumber(dfCoapSc)
dfCoapSt = processGateNumber(dfCoapSt)
dfCoapEws = processGateNumber(dfCoapEws)
dfCoapPd = processGateNumber(dfCoapPd)
print('Done Gate code fixing')

# Now prepare the final list
print('Preparing final list')
dfFinal = dfCoapGen.head(genCount)
dfFinal = dfFinal.append(dfCoapObc.head(obcCount))
dfFinal = dfFinal.append(dfCoapSc.head(scCount))
dfFinal = dfFinal.append(dfCoapSt.head(stCount))
dfFinal = dfFinal.append(dfCoapEws.head(ewsCount))
dfFinal = dfFinal.append(dfCoapPd.head(pdCount))
print('Done preparing final list')

# re-order columns in the way we want
dfFinal = dfFinal[['ApplicationNo','AppStatus','Remarks','SubmissionDate','GATENo','RegistrationNo','EntranceScore', 'Name','OfferedPgm','CasteCategoryName','RoundNum', 'InstiName', 'InstiId', 'InstiType']]

# write output to file
dfFinal.to_excel(outfile,index=False)
