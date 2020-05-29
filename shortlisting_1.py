#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 16:40:21 2020

@author: paddy
"""

import pandas as pd
import numpy as np

# read the input
inputFile = '/home/paddy/laptopLocal/localWork/msPhDAug2020/MTech_shortlisting/PGApplciationReport_29May2020.xls'
data = pd.read_excel(inputFile)

outputDir = '/home/paddy/laptopLocal/localWork/msPhDAug2020/MTech_shortlisting/mtech_process/output/'

# convert UG score into CGPA
# This has to be automated in the form
# todo
cgCol = data.UGScore
cgpaIdx = cgCol.str.contains(r'.*CGPA.*')
perIdx = cgCol.str.contains(r'.*Per.*')
cgpaData = cgCol.loc[cgCol.str.contains(r'.*CGPA.*')]
perData = cgCol.loc[cgCol.str.contains(r'.*Per.*')]

# form a new series
cgNew = pd.Series(np.zeros(len(cgCol)))
# iterate through the cgCol series
for i in range(len(cgCol)):
    # check if its CGPA or per
    if 'CGPA' in cgCol[i]:
        try:
            cgNew[i] = float(cgCol[i][0:4])
        except ValueError:
            print('CGPA ValueError in index ' + str(i) + ' ' + cgCol[i][0:4])
            cgNew[i] = float(cgCol[i][0:2])
    else:
        try:
            # convert i=per to cgpa
            cgNew[i] = float(cgCol[i][0:4])/10
        except ValueError:
            print('Per ValueError in index ' + str(i) + ' ' + cgCol[i][0:4])
            cgNew[i] = float(cgCol[i][0:2])/10
    


# now cgNew has all cgpas
# Append this to dataframe
data['NewCGPA'] = cgNew
   


# choose the program of interest
pgmString = 'Signal Processing and Communications (SPCOM)'

# get all applicants to pgm
x = data[(data.MainArea1==pgmString) | (data.MainArea2==pgmString) |
(data.MainArea3==pgmString)]

# Now divide into categories
catGen = 'GEN'
catEws = 'GEN(EWS)'
catObcCl = 'OBC(CL)'
catObcNcl = 'OBC(NCL)'
catSc = 'SC'
catSt = 'ST'
#catPd

##########################################

# for general and Obc CL

# get the list of general and CL catergory 
x_gen = x[(x.CasteCategoryName==catGen) | (x.CasteCategoryName==catObcCl)]
# get the correct UG degree
#x_gen_deg
# currently this is not possible, because input is not standard
# this is TODO

# check gate
gateString = 'EC - Electronics and Communication Engineering'
x_gen_gate = x_gen[x_gen.EntranceSubjectName==gateString]

# check gate_score
gateCutoff = 700
x_gen_gate_gscore = x_gen_gate[x_gen_gate.EntranceScore > gateCutoff]

# check UG marks
ugCutoff = 7.5
x_gen_gate_gscore_ugscore = x_gen_gate_gscore[x_gen_gate_gscore.NewCGPA > ugCutoff]

# write to output
outFile = outputDir +'spcom_gen_obccl.xls'
x_gen_gate_gscore_ugscore.to_excel(outFile)

 
###################################################

# for SC

# get the list of general and CL catergory 
x_sc = x[x.CasteCategoryName==catSc]
# get the correct UG degree
#x_gen_deg
# currently this is not possible, because input is not standard
# this is TODO

# check gate
gateString = 'EC - Electronics and Communication Engineering'
x_sc_gate = x_sc[x_sc.EntranceSubjectName==gateString]

# check gate_score
gateCutoff = 200
x_sc_gate_gscore = x_sc_gate[x_sc_gate.EntranceScore > gateCutoff]

# check UG marks
ugCutoff = 5.0
x_sc_gate_gscore_ugscore = x_sc_gate_gscore[x_sc_gate_gscore.NewCGPA > ugCutoff]

# write to output
outFile = outputDir +'spcom_sc.xls'
x_sc_gate_gscore_ugscore.to_excel(outFile)


