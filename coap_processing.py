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

# datafiles
dataDir = '/home/paddy/laptopLocal/localWork/msPhDAug2020/MTech_shortlisting/mtech_process/output/'
genDataFile = dataDir + 'spcom_genObccl.xls'
obcDataFile = dataDir + 'spcom_obcNcl.xls'
scDataFile = dataDir + 'spcom_sc.xls'
stDataFile = dataDir + 'spcom_st.xls'
ewsDataFile = dataDir + 'spcom_ews.xls'
pdDataFile = dataDir + 'spcom_pd.xls'

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

coapColumns = ['RegistrationNo','Name','COAPNo', 'GATENo', 'EntranceScore','AppliedDate']
dfCoapGen = dfGen[coapColumns].copy()


