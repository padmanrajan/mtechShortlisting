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
    foo = cgCol[i].strip()
    if 'CGPA' in foo:
        try:
            cgNew[i] = float(foo[0:4])
        except ValueError:
            print('CGPA ValueError in index ' + str(i) + ' ' + foo[0:4])
            cgNew[i] = float(foo[0:2])
    else:
        try:
            # convert i=per to cgpa
            cgNew[i] = float(foo[0:4])/10
        except ValueError:
            print('Per ValueError in index ' + str(i) + ' ' + foo[0:4])
            cgNew[i] = float(foo[0:2])/10
    


# now cgNew has all cgpas
# Append this to dataframe
data['NewCGPA'] = cgNew
   
# We also need to process the non-standard UG degrees.
# this is TODO in the OAS form.
# We will form a new column with standard values.
ugCol = data.UGStream
ugNew = pd.Series(np.zeros(len(ugCol)))
# iterate through this series
for i in range(len(ugCol)):
    if 'trical' in ugCol[i].lower():
        ugNew[i] = 'EEE'
    elif 'inst'in ugCol[i].lower():
        ugNew[i] = 'INS'
    elif 'ectronic'in ugCol[i].lower():
        ugNew[i] = 'ECE'
    elif 'power'in ugCol[i].lower():
        ugNew[i] = 'EEE'
    elif 'compu'in ugCol[i].lower():
        ugNew[i] = 'CSE'
    else:
        ugNew[i] = ugCol[i]

data['NewUG'] = ugNew




# choose the program of interest
pgmString = 'Power Electronics and Drive (PED)'

# get all applicants to pgm
x = data[(data.MainArea1==pgmString) | (data.MainArea2==pgmString) |
(data.MainArea3==pgmString)]

# make sure UG course is valid for program
# check the correct UG degree
string1 = 'EEE'
x_deg = x[x.NewUG==string1]


# check gate
gateString1 = 'EE - Electrical Engineering'
x_deg_gate = x_deg[(x_deg.EntranceSubjectName==gateString1)]


# Now apply category-wise selection criteria


# Divide into categories
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
x_deg_gate_cat = x_deg_gate[(x_deg_gate.CasteCategoryName==catGen) | (x_deg_gate.CasteCategoryName==catObcCl)]

# check gate_score
gateCutoff = 500
x_deg_gate_cat_gscore = x_deg_gate_cat[x_deg_gate_cat.EntranceScore >= gateCutoff]

# check UG marks
ugCutoff = 6
x_deg_gate_cat_gscore_ugscore = x_deg_gate_cat_gscore[x_deg_gate_cat_gscore.NewCGPA >= ugCutoff]
# copy to final variable for convenience
final_x_deg_gate_gen_gscore_ugscore = x_deg_gate_cat_gscore_ugscore

# write to output
outFile = outputDir +'power_genObccl.xls'
x_deg_gate_cat_gscore_ugscore.to_excel(outFile)

 
###################################################

##########################################

# for Obc NCL 

# get the list of general and CL catergory 
x_deg_gate_cat = x_deg_gate[(x_deg_gate.CasteCategoryName==catObcNcl)]

# check gate_score
gateCutoff = 500
x_deg_gate_cat_gscore = x_deg_gate_cat[x_deg_gate_cat.EntranceScore >= gateCutoff]

# check UG marks
ugCutoff = 6
x_deg_gate_cat_gscore_ugscore = x_deg_gate_cat_gscore[x_deg_gate_cat_gscore.NewCGPA >= ugCutoff]
# copy to final variable for convenience
final_x_deg_gate_obcncl_gscore_ugscore = x_deg_gate_cat_gscore_ugscore

# write to output
outFile = outputDir +'power_obcNcl.xls'
x_deg_gate_cat_gscore_ugscore.to_excel(outFile)

 
###################################################











# for SC
x_deg_gate_cat = x_deg_gate[x_deg_gate.CasteCategoryName==catSc]

# check gate_score
gateCutoff = 400
x_deg_gate_cat_gscore = x_deg_gate_cat[x_deg_gate_cat.EntranceScore >= gateCutoff]

# check UG marks
ugCutoff = 5.5
x_deg_gate_cat_gscore_ugscore = x_deg_gate_cat_gscore[x_deg_gate_cat_gscore.NewCGPA >= ugCutoff]
final_x_deg_gate_sc_gscore_ugscore = x_deg_gate_cat_gscore_ugscore

# write to output
outFile = outputDir +'power_sc.xls'
x_deg_gate_cat_gscore_ugscore.to_excel(outFile)


##########################################

# for EWS
x_deg_gate_cat = x_deg_gate[x_deg_gate.CasteCategoryName==catEws]

# check gate_score
gateCutoff = 500
x_deg_gate_cat_gscore = x_deg_gate_cat[x_deg_gate_cat.EntranceScore >= gateCutoff]

# check UG marks
ugCutoff = 6
x_deg_gate_cat_gscore_ugscore = x_deg_gate_cat_gscore[x_deg_gate_cat_gscore.NewCGPA >= ugCutoff]
# copy to final variable for convenience
final_x_deg_gate_ews_gscore_ugscore = x_deg_gate_cat_gscore_ugscore

# write to output
outFile = outputDir +'power_ews.xls'
x_deg_gate_cat_gscore_ugscore.to_excel(outFile)

 
###################################################

##########################################

# for ST

# get the list of general and CL catergory 
x_deg_gate_cat = x_deg_gate[x_deg_gate.CasteCategoryName==catSt]

# check gate_score
gateCutoff = 400
x_deg_gate_cat_gscore = x_deg_gate_cat[x_deg_gate_cat.EntranceScore >= gateCutoff]

# check UG marks
ugCutoff = 5.5
x_deg_gate_cat_gscore_ugscore = x_deg_gate_cat_gscore[x_deg_gate_cat_gscore.NewCGPA >= ugCutoff]
# copy to final variable for convenience
final_x_deg_gate_st_gscore_ugscore = x_deg_gate_cat_gscore_ugscore

# write to output
outFile = outputDir +'power_st.xls'
x_deg_gate_cat_gscore_ugscore.to_excel(outFile)

 
###################################################


##########################################

## for PD

# get the list of general and CL catergory 
x_deg_gate_cat = x_deg_gate[x_deg_gate.ISPhysicallyChallenged=='Yes']

# check gate_score
gateCutoff = 400
x_deg_gate_cat_gscore = x_deg_gate_cat[x_deg_gate_cat.EntranceScore >= gateCutoff]

# check UG marks
ugCutoff = 5.5
x_deg_gate_cat_gscore_ugscore = x_deg_gate_cat_gscore[x_deg_gate_cat_gscore.NewCGPA >= ugCutoff]
# copy to final variable for convenience
final_x_deg_gate_pd_gscore_ugscore = x_deg_gate_cat_gscore_ugscore

## write to output
outFile = outputDir +'power_pd.xls'
x_deg_gate_cat_gscore_ugscore.to_excel(outFile)
#
 
###################################################
