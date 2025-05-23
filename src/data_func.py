
#-----------------------------------------------------------------------
# Copyright (C) 2020, All rights reserved
#
# Peng Wang
#
#-----------------------------------------------------------------------
#=======================================================================

# DESCRIPTION:
# This software is a python library for Many-Particle Simulation of Complex Social Interaction
# The individual-level model is extended based on the well-known social force model, and it mainly describes how agents/particles interact with each other, and also with surrounding facilities including obstructions and passageways. Most importantly, we introduce a set of arrays to define social relationship of agents/particles in a quantitative manner. Opinion dynamics is integrated with force-based interaction to study complex social phenonmena including path-selection activities, social group and herding effect.  Verying interestingly, the interaction of such agent/particles are not only at physics-level, but at consciousness and unconsciousness level by integratings advance social-psychological studies.  

# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@gmail.com

import pygame
import pygame.draw
import numpy as np
#from agent_model_obst3 import *
from agent import *
from obst import *
#from passage import *
from math_func import *
from math import *
#from config import *
import re
import random
import csv
#from ctypes import *
import struct
import time
import sys, os
try:
    import matplotlib.pyplot as plt
except:
    print("Warning: matplotlib cannot be imported.  Unable to plot figures!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")

# Sequentially search for Title1, Title2 and Title3 through FileName
def findTitle(FileName, Title1=None, Title2=None, Title3=None):
    findTitle=False
    if Title1:
        for line in open(FileName):
            if re.match(Title1, line):
                findTitle=True
                return line
    if Title2:
        for line in open(FileName):
            if re.match(Title2, line):
                findTitle=True
                return line
    if Title3:
        for line in open(FileName):
            if re.match(Title3, line):
                findTitle=True
                return line
    return None


def findKey(FileName, Title1=None, Title2=None, Title3=None, TitleStr=''):
    
    FindTitle1=int(0)
    FindTitle2=int(0)
    FindTitle3=int(0)
    
    for line in open(FileName, "r"):
        if Title1:
            if re.match(Title1, line):
                FindTitle1=int(1)
                temp =  line.split('=')
                result = str(temp[1].rstrip('\n').rstrip(',').strip())
                return result
        if Title2:
            if re.match(Title2, line):
                FindTitle2=int(1)
                temp =  line.split('=')
                result = str(temp[1].rstrip('\n').rstrip(',').strip())
                return result
        if Title3:
            if re.match(Title3, line):
                FindTitle3=int(1)
                temp =  line.split('=')
                result = str(temp[1].rstrip('\n').rstrip(',').strip())
                return result
    if FindTitle1+FindTitle2+FindTitle3>1.0:
        print("Warning: Multiple input line for Title of "+str(TitleStr)+"\n")
        print("Use the last key value found for the title!")
        if sys.version_info[0] == 2: 
            raw_input("Please check!")
        else:
            input("please check!")
    return result


def readStepTxt(FileName, showdata=True):
    findStep=False

    T= []
    XYZ=[]
    TAG=[]
    FEATRUE=[]
    
    for line in open(FileName):
        if re.match('&SimulationTime:', line):
            findStep=True
            dataTemp=line.split(':')
            Time = float(dataTemp[1].strip())
            T.append(Time)
            
            x=[]
            y=[]
            z=[]
            tag=[]
            
            Q_actualVx=[]
            Q_actualVy=[]
            Q_desiredVx=[]
            Q_desiredVy=[]
            
            Q_motiveFx=[]
            Q_motiveFy=[]
            
            Q_socialFx=[]
            Q_socialFy=[]
            Q_selfrepFx=[]
            Q_selfrepFy=[]
            
        if  findStep:
            if re.search('Agent:', line):
                dataTemp=line.split(':')
                tag.append(float(dataTemp[1].strip()))

            if re.search('Position:', line):
                dataTemp=line.split(':')
                xy=dataTemp[1]
                temp =  re.split(r'[\s\,]+', xy)
                x.append(float(temp[1].strip().lstrip('[')))
                y.append(float(temp[2].strip().rstrip(']')))
                z.append(1.6)

            if re.search('Velocity:', line):
                dataTemp=line.split(':')
                vel=dataTemp[2]
                temp =  re.split(r'[\s\,]+', vel)
                Q_actualVx.append(float(temp[1].lstrip('[').strip()))
                Q_actualVy.append(float(temp[2].strip().rstrip(']')))
                
            if re.search('&EndofStep', line):
                findStep = False

                NPLIM=np.size(tag)
                xyz=x+y+z #+ap1+ap2+ap3+ap4
                Q = Q_actualVx+Q_actualVy +Q_desiredVx+Q_desiredVy + Q_motiveFx+Q_motiveFy +Q_socialFx+Q_socialFy + +Q_selfrepFx+Q_selfrepFy

                # process timestep data
                XYZ.append(xyz)
                TAG.append(tag)
                FEATRUE.append(Q)
                
            '''
            xyz  = np.array(readFRec(fin,'f'))
            tag  = np.array(readFRec(fin,'I'))
            q    = np.array(readFRec(fin,'f'))

            #print >> outfile, "g", q, "\n"
            if mode=='evac':
                xyz.shape = (7,nplim) # evac data: please check dump_evac() in evac.f90
            else: 
                xyz.shape = (3,nplim) # particle data: please check dump_part() in dump.f90
            
            q.shape   = (n_quant, nplim)
            
            if wrtxt:
                outfile.write("Time:" + str(Time) + "\n")
                outfile.write("xyz:" + str(xyz) + "\n") 
                outfile.write("tag:" + str(tag) + "\n")           
                outfile.write( "q:" + str(q) + "\n")
            '''
    
    #np.savez( outfn + ".npz", T, XYZ, TAG)
    #return (np.array(T), np.hstack(Q), q_labels, q_units)
    return T, XYZ, TAG, FEATRUE  #, n_part, version, n_quant


def readDoorProb(FileName, doorIndex, showdata=True):
    findMESH=False
    doorProb=[]
    timeIndex= []
    for line in open(FileName):
        if re.match('&DoorProb', line):
            findMESH=True
            row=[]
        if  findMESH:
            if re.search('prob=', line):
                dataTemp=line.split('prob=')
                #print('dataTemp:', dataTemp[1:])

                #for index in range(len(dataTemp[1:])):
                #    probDist=dataTemp[index+1].lstrip('[').strip('=').rstrip(']')
                probDist=dataTemp[1].lstrip('[').strip('=').rstrip(']')
                temp2 =  re.split(r'[\s\,]+', probDist)
                print(temp2)
                prob = float(temp2[doorIndex+1].lstrip('[').strip('=').rstrip(']'))
                row.append(prob)
                #print(row)
            if re.search('SimulationTime=', line):
                dataTemp=line.split('=')
                timeIndex.append(float(dataTemp[1].lstrip().rstrip()))
                    #xpoints = temp2[0]
                    #ypoints = temp2[1]
            '''
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xmax = temp2[1]-temp2[0]
                ymax = temp2[3]-temp2[2]
            '''
            if re.search('WellDone!', line):
                findMESH = False
                #doorProb.append(dataTemp[1:])
                doorProb.append(row)
                # return xpoints, ypoints, xmax, ymax
                # Only find the first &MESH line
                # The second or other MESH lines are ignored

    print('doorProb', doorProb)
    (NRow, NColomn) = np.shape(doorProb)  
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(doorProb[i][j])
    print('matrix', matrix)
    print('sizeOfMatrix:', np.shape(matrix))
    print('sizeOfTimeIndex:', np.shape(timeIndex))
    #print(timeIndex)
    if showdata:
        for j in range(NColomn):
            plt.plot(timeIndex, matrix[:,j], linewidth=3.0, label=str(j))
            plt.text(0,matrix[0,j], str(j), fontsize=18)
        plt.title("exit index:"+str(doorIndex))
        plt.grid()
        plt.legend(loc='best')
        temp=FileName.split('.')
        fnamePNG = temp[0]+'_exitprob.png'
        plt.savefig(fnamePNG)
        plt.show()

    return matrix


def readCSV_base(fileName):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    print(reader)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print(strData[1:,1:])
    #print('np.shape(strData)=', np.shape(strData), '\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    #dataNP = np.array(strData)
    #print(dataNP)
    #print('np.shape(dataNP)', np.shape(dataNP),'\n')

    csvFile.close()
    return strData #dataNP


def getData(fileName, strNote, flag='npArray'):
    dataFeatures = readCSV_base(fileName)

    Num_Data = len(dataFeatures)
    
    IPedStart=0
    Find = False
    #print(dataFeatures)
    for i in range(Num_Data):
        if len(dataFeatures[i]):
            if dataFeatures[i][0]==strNote:
                IPedStart=i
                Find = True
    
    if Find is False:
        return [], 0, 0
        #IPedStart = None
        #IPedEnd = None
        #dataOK = None
        #return dataOK, IPedStart, IPedEnd
        #return [], 0, 0
    else:
        IPedEnd=IPedStart
        for j in range(IPedStart, Num_Data):
            if len(dataFeatures[j]):
                if dataFeatures[j][0]=='' or dataFeatures[j][0]==' ':
                    IPedEnd=j
                    break
            else: #len(dataFeatures[j])==0: Namely dataFeatures[j]==[]
                IPedEnd=j
                break
            if j==Num_Data-1:
                IPedEnd=Num_Data
                
        if flag=='npArray':
            dataOK = dataFeatures[IPedStart : IPedEnd]
        else:
            dataOK = list(dataFeatures[IPedStart : IPedEnd])
        return dataOK, IPedStart, IPedEnd

    #data_result = np.array(dataOK)
    #return data_result[1:, 1:]
    

# This function is not used in this program
def readCSV(fileName, mode='float'):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    dataNP = np.array(strData)
    print (dataNP)
    print('np.shape(dataNP)', np.shape(dataNP))
    print('\n')

    #print(strData[1:,1:])
    csvFile.close()	
    
    if mode=='string':
        print (dataNP[1:, 1:])
        return dataNP[1:, 1:]
    
    if mode=='float':
        
        #print dataNP[1:, 1:]
        (I, J) = np.shape(dataNP)
        #print "The size of tha above matrix:", [I, J]
        #print "The effective data size:", [I-1, J-1]
        matrix = np.zeros((I, J))
        #print matrix

        for i in range(1,I):
            for j in range(1,J):
                matrix[i,j] = float(dataNP[i,j])

    print (matrix[1:, 1:])
    return matrix[1:, 1:]
    

def arr1D_2D(data, debug=True):
    #data is in type of 1D array, but it is actually a 2D data format.  
    
    NRow = len(data)
    NColomn = len(data[1])
    matrix = np.zeros((NRow, NColomn), dtype='|S20')
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = data[i][j]
    if debug:
        print('Data in 2D array:\n', matrix)
        
    return matrix


def readFloatArray(tableFeatures, NRow, NColomn, debug=True):

    #tableFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Ped2Exit')
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                try:
                    matrix[i,j] = float(tableFeatures[i+1][j+1])
                except:
                    matrix[i,j] = float(0.0)
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrix)
    return matrix

def readAgent2Exit(tableFeatures, NRow, NColomn, debug=True):

    #tableFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Ped2Exit')
    matrixA2E = np.zeros((NRow, NColomn))
    matrixKW = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                if tableFeatures[i+1][j+1] and tableFeatures[i+1][j+1] != '0':
                    
                    temp=re.split(r'\s*[;\|\s]\s*', tableFeatures[i+1][j+1])
                    try:
                        matrixA2E[i,j] = float(temp[0])
                    except:
                        matrixA2E[i,j] = float(0.0)
                        
                    try:
                        matrixKW[i,j] = bool(temp[1])
                    except:
                        matrixKW[i,j] = False
                else:
                    matrixA2E[i,j] = 0.0
                    matrixKW[i,j] = False
                    
                # Coordinate consistency of matrixA2E and matrixKW
                if matrixA2E[i,j] > 0.0:
                    matrixKW[i,j] = True

    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrixA2E, matrixKW)
    return matrixA2E #, matrixKW


def readGroupSABD(tableFeatures, NRow, NColomn, debug=True):

    # NRow and NColomn are the size of data to be extracted from tableFeatures
    matrixS = np.zeros((NRow, NColomn))
    matrixA = np.zeros((NRow, NColomn))
    matrixB = np.zeros((NRow, NColomn))
    matrixD = np.zeros((NRow, NColomn))
    
    for i in range(NRow):
        for j in range(NColomn):
            
            if tableFeatures[i+1][j+1] and tableFeatures[i+1][j+1] != '0':
                try:
                    #temp=re.split(r'[\s\/]+', tableFeatures[i+1][j+1])
                    temp=re.split(r'\s*[;\|\s]\s*', tableFeatures[i+1][j+1])
                    matrixS[i,j] = float(temp[0])
                    matrixA[i,j] = float(temp[1])
                    matrixB[i,j] = float(temp[2])
                    matrixD[i,j] = float(temp[3])
                except:
                    print("Error in reading group data!")
                    input("Please check!")
                    matrixS[i,j] = 0.0
                    matrixA[i,j] = 0.0
                    matrixB[i,j] = 0.0
                    matrixD[i,j] = 0.0
            else:
                matrixS[i,j] = 0.0
                matrixA[i,j] = 0.0
                matrixB[i,j] = 0.0
                matrixD[i,j] = 0.0
                
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrixS, matrixA, matrixB, matrixD)
    return matrixS, matrixA, matrixB, matrixD


def readGroupABD(tableFeatures, NRow, NColomn, debug=True):

    # NRow and NColomn are the size of data to be extracted from tableFeatures
    matrixA = np.zeros((NRow, NColomn))
    matrixB = np.zeros((NRow, NColomn))
    matrixD = np.zeros((NRow, NColomn))
    
    for i in range(NRow):
        for j in range(NColomn):
            
            if tableFeatures[i+1][j+1] and tableFeatures[i+1][j+1] != '0':
                try:
                    #temp=re.split(r'[\s\/]+', tableFeatures[i+1][j+1])
                    temp=re.split(r'\s*[;\|\s]\s*', tableFeatures[i+1][j+1])
                    matrixA[i,j] = float(temp[0])
                    matrixB[i,j] = float(temp[1])
                    matrixD[i,j] = float(temp[2])
                except:
                    print("Error in reading group data!")
                    input("Please check!")
                    matrixA[i,j] = 0.0
                    matrixB[i,j] = 0.0
                    matrixD[i,j] = 0.0
            else:
                matrixA[i,j] = 0.0
                matrixB[i,j] = 0.0
                matrixD[i,j] = 0.0
                
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrixA, matrixB, matrixD)
    return matrixA, matrixB, matrixD
    

def readGroupS(tableFeatures, NRow, NColomn, debug=True):
    # NRow and NColomn are the size of data to be extracted from tableFeatures
    matrixS = np.zeros((NRow, NColomn))
    if tableFeatures[i+1][j+1] and tableFeatures[i+1][j+1] != '0':
        try:    
            matrixS[i,j] = float(tableFeatures[i+1][j+1])        
        except:
            print("Error in reading group data!")
            input("Please check!")
            matrixS[i,j] = 0.0
    else:
        matrixS[i,j] = 0.0
                
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrixS)
    return matrixS


def readArrayIndex(tableFeatures, NRow, NColomn, index=0, iniX=1, iniY=1, debug=True):

    #tableFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Ped2Exit')

    #(dataX, dataY) = np.shape(tableFeatures)
    #NRow = dataX - iniX
    #NColomn = dataY - iniY

    # NRow and NColomn are the size of data to be extracted from tableFeatures
    matrixC = np.zeros((NRow, NColomn))
    #matrixB = np.zeros((NRow, NColomn))
    #matrixD = np.zeros((NRow, NColomn))
    
    for i in range(NRow):
        for j in range(NColomn):
            try:
                if tableFeatures[i+iniX][j+iniY] and tableFeatures[i+iniX][j+iniY] != '0':
                    #temp=re.split(r'[\s\/]+', tableFeatures[i+1][j+1])
                    temp=re.split(r'\s*[;\|\s]\s*', tableFeatures[i+iniX][j+iniY])
                    matrixC[i,j] = float(temp[index])
                    #matrixB[i,j] = float(temp[1])
                    #matrixD[i,j] = float(temp[2])
                else:
                    matrixC[i,j] = 0.0
                    #matrixB[i,j] = 1.0
                    #matrixD[i,j] = 1.0
            except:
                print("Error in reading data!")
                input("Please check!")
                matrixC[i,j] = 0.0
                #matrixB[i,j] = 1.0
                #matrixD[i,j] = 1.0
                
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', 'Index Number:', index, '\n', matrixC, '\n\n') #, matrixB, matrixD)
    return matrixC #, matrixB, matrixD



def readSocialArrayCSV(FileName, debug=True, marginTitle=1):

    #dataFeatures = readCSV_base(FileName)
    #[Num_Data, Num_Features] = np.shape(dataFeatures)   

    agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Ped')
    Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&agent')
        Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Agent')
        Num_Agents=len(agentFeatures)-marginTitle

    if debug: 
        print ('Number of Agents:', Num_Agents, '\n')
        print ("Features of Agents\n", agentFeatures, "\n")

    agent2exitFeatures, lowerIndex, upperIndex = getData(FileName, '&agent2exit')
    Num_Agent2Exit=len(agent2exitFeatures)-marginTitle
    if Num_Agent2Exit <= 0:
        agent2exitFeatures, lowerIndex, upperIndex = getData(FileName, '&ped2exit')
        Num_Agent2Exit=len(agent2exitFeatures)-marginTitle
    if Num_Agent2Exit <= 0:
        agent2exitFeatures, lowerIndex, upperIndex = getData(FileName, '&Ped2Exit')
        Num_Agent2Exit=len(agent2exitFeatures)-marginTitle
    if debug:
        print ('Number of Agent2Exit:', Num_Agent2Exit, '\n')
        print ('Features of Agent2Exit\n', agent2exitFeatures, "\n")

    agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupC')
    Num_AgentGroup=len(agentgroupFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupCABD')
        Num_AgentGroup=len(agent2exitFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupABD')
        Num_AgentGroup=len(agent2exitFeatures)-marginTitle
    if debug:
        print ('Number of AgentGroup:', Num_AgentGroup, '\n')
        print ('Features of AgentGroup\n', agentgroupFeatures, "\n")

    obstFeatures, lowerIndex, upperIndex = getData(FileName, '&Wall')
    Num_Obsts=len(obstFeatures)-marginTitle
    if Num_Obsts <= 0:
        obstFeatures, lowerIndex, upperIndex = getData(FileName, '&wall')
        Num_Obsts=len(obstFeatures)-marginTitle

    if debug:
        print ('Number of Walls:', Num_Obsts, '\n')
        print ("Features of Walls\n", obstFeatures, "\n")

    exitFeatures, lowerIndex, upperIndex = getData(FileName, '&Exit')
    Num_Exits=len(exitFeatures)-marginTitle
    if Num_Exits <= 0:
        exitFeatures, lowerIndex, upperIndex = getData(FileName, '&exit')
        Num_Exits=len(exitFeatures)-marginTitle
        
    if debug: 
        print ('Number of Exits:', Num_Exits, '\n')
        print ("Features of Exits\n", exitFeatures, "\n")

    doorFeatures, lowerIndex, upperIndex = getData(FileName, '&Door')
    Num_Doors=len(doorFeatures)-marginTitle
    if Num_Doors <= 0:
        doorFeatures, lowerIndex, upperIndex = getData(FileName, '&door')
        Num_Doors=len(doorFeatures)-marginTitle
        
    if debug:
        print ('Number of Doors:', Num_Doors, '\n')
        print ('Features of Doors\n', doorFeatures, "\n")
        
    exit2doorFeatures, lowerIndex, upperIndex = getData(FileName, '&Exit2Door')
    Num_Exit2Door=len(exit2doorFeatures)-marginTitle
    if Num_Exit2Door <= 0:
        exit2doorFeatures, lowerIndex, upperIndex = getData(FileName, '&exit2door')
        Num_Exit2Door=len(doorFeatures)-marginTitle

    if debug:
        print ('Number of Exit2Door:', Num_Exit2Door, '\n')
        print ('Features of Exit2Door\n', exit2doorFeatures, "\n")

    simuObjFeatures = []
    if solverFeature:
        simuObjFeatures.append(solverFeature)
    if dtFeature:
        simuObjFeatures.append(dtFeature)
    if dt1Feature:
        simuObjFeatures.append(dt1Feature)
    if dt2Feature:
        simuObjFeatures.append(dt2Feature)
    if dt3Feature:
        simuObjFeatures.append(dt3Feature)
    if tendFeature:
        simuObjFeatures.append(tendFeature)

    return agentFeatures, agent2exitFeatures, agentgroupFeatures, obstFeatures, exitFeatures, \
    doorFeatures, exit2doorFeatures, simuObjFeatures


# The file to record the some output data of the simulation
# f = open("outData.txt", "w+")

def readAgents(FileName, debug=True, marginTitle=1, ini=1):

    #dataFeatures = readCSV_base(FileName)
    #[Num_Data, Num_Features] = np.shape(dataFeatures)   

    agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Agent')
    Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&agent')
        Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Ped')
        Num_Agents=len(agentFeatures)-marginTitle

    if debug: 
        print ('Number of Agents:', Num_Agents, '\n')
        print ("Features of Agents\n", agentFeatures, "\n")

    agents = []
    index = 0 
    for agentFeature in agentFeatures[marginTitle:]:
        agent = person()
        agent.ID = index
        index = index+1
        agent.name = str(agentFeature[ini-1])
        agent.pos = np.array([float(agentFeature[ini+0]), float(agentFeature[ini+1])])
        try:
            agent.actualV = np.array([float(agentFeature[ini+2]), float(agentFeature[ini+3])])
        except:
            agent.actualV = np.array([0.0, 0.0])
            
        try:
            agent.tau = float(agentFeature[ini+4])
            agent.tpre = float(agentFeature[ini+5])
        except:
            agent.tau = 0.6
            agent.tpre = 10.0
        
        # Opinion Dynamic Parameters
        try:
            agent.p = float(agentFeature[ini+6])
            agent.pMode = agentFeature[ini+7]
            agent.pp2 = float(agentFeature[ini+8])
        except:
            agent.p = 0.5
            agent.pMode = 'fixed'
            agent.pp2 = 0.5
        
        try:
            agent.tpreMode = int(agentFeature[ini+9]) #arousalLevel = float(agentFeature[ini+9])
            agent.aType = str(agentFeature[ini+10])
            agent.inComp = int(agentFeature[ini+11]) 
        except:
            agent.tpreMode = int(1) #arousalLevel = 0 #0.2
            agent.aType = 'active'
            agent.inComp = int(1)
        
        try:
            #agent.moving_tau = float(agentFeature[ini+12])
            agent.talk_range = float(agentFeature[ini+12])
            agent.talk_tau = float(agentFeature[ini+13])
            agent.talk_prob = float(agentFeature[ini+14])
            #agent.pp2 = float(agentFeature[ini+15])
            agent.radius = float(agentFeature[ini+16])
            agent.mass = float(agentFeature[ini+17])
        except:     
            #agent.moving_tau = agent.tau
            agent.talk_range = 2.0
            agent.talk_tau = agent.tau
            agent.talk_prob = 0.6
            #agent.pp2 = 0.1
            agent.radius = 0.35
            agent.mass = 65 
        
        agents.append(agent)
        
    return agents


# This function addAgent() is actually not that meaningful.  We just leave it here for future optional development.  
# Because many agent features cannot be added by using the graphic user interface.
# Such as group features and door selection features.
def addAgent(agents, x_pos, y_pos):
    num = len(agents)
    agent = person()
    agent.pos = np.array([float(x_pos), float(y_pos)])
    agent.ID = int(num)
    agent.inComp = int(1)

    # add agent into the list of agents
    agents.append(agent)
    

def readWalls(FileName, debug=True, marginTitle=1, ini=0):
    #obstFeatures = readCSV(FileName, "string")
    #[Num_Obsts, Num_Features] = np.shape(obstFeatures)

    obstFeatures, lowerIndex, upperIndex = getData(FileName, '&Wall')
    Num_Obsts=len(obstFeatures)-marginTitle
    if Num_Obsts <= 0:
        obstFeatures, lowerIndex, upperIndex = getData(FileName, '&wall')
        Num_Obsts=len(obstFeatures)-marginTitle
    if Num_Obsts <= 0:
        obstFeatures, lowerIndex, upperIndex = getData(FileName, '&obst')
        Num_Obsts=len(obstFeatures)-marginTitle

    if debug:
        print ('Number of Walls:', Num_Obsts, '\n')
        print ("Features of Walls\n", obstFeatures, "\n")
    
    walls = []
    index = 0
    for obstFeature in obstFeatures[marginTitle:]:
        wall = obst()
        wall.name = str(obstFeature[ini])
        
        try:
            wall.mode = str(obstFeature[ini+6])
        except:
            wall.mode = 'rect'
        
        if wall.mode == 'line':
            wall.params[0]= float(obstFeature[ini+1])
            wall.params[1]= float(obstFeature[ini+2])
            wall.params[2]= float(obstFeature[ini+3])
            wall.params[3]= float(obstFeature[ini+4])
        
        elif wall.mode == 'rect':
            wall.params[0]= min(float(obstFeature[ini+1]),float(obstFeature[ini+3]))
            wall.params[1]= min(float(obstFeature[ini+2]),float(obstFeature[ini+4]))
            wall.params[2]= max(float(obstFeature[ini+1]),float(obstFeature[ini+3]))
            wall.params[3]= max(float(obstFeature[ini+2]),float(obstFeature[ini+4]))
        
        wall.oid = index
        index = index+1
        
        try:
            wall.arrow = int(obstFeature[ini+5])
        except:
            wall.arrow = int(0)
        
        try:
            wall.mode = str(obstFeature[ini+6])
        except:
            wall.mode = 'rect'
            
        try:
            wall.inComp = int(obstFeature[ini+7])
        except:
            wall.inComp = int(1)

        try:
            wall.pointer1 = np.array([float(obstFeature[ini+8]), float(obstFeature[ini+9])])
            wall.pointer2 = np.array([float(obstFeature[ini+10]), float(obstFeature[ini+11])])
        except:
            wall.pointer1 = np.array([np.nan, np.nan])
            wall.pointer2 = np.array([np.nan, np.nan]) #np.array([float('NaN'), float('NaN')])
        
        # Walls have no exit signs if arrow is 0
        wall.exitSign = bool(wall.arrow)
        walls.append(wall)
        
    return walls


#This function addWall() is created for users to add wall in testGeom()
def addWall(walls, startPt, endPt, mode='line'):
    num = len(walls)
    wall = obst()
    
    if mode == 'line':
        wall.params[0]= float(startPt[0])
        wall.params[1]= float(startPt[1])
        wall.params[2]= float(endPt[0])
        wall.params[3]= float(endPt[1])
    if mode == 'rect':
        #wall.params[0]= float(startPt[0])
        #wall.params[1]= float(startPt[1])
        #wall.params[2]= float(endPt[0])
        #wall.params[3]= float(endPt[1])

        wall.params[0]= min(float(startPt[0]),float(endPt[0]))
        wall.params[1]= min(float(startPt[1]),float(endPt[1]))
        wall.params[2]= max(float(startPt[0]),float(endPt[0]))
        wall.params[3]= max(float(startPt[1]),float(endPt[1]))

    wall.name = '-G-'
    # The wall arrow is to be tested in simulation.  
    # The default value is no direction assigned, i.e., zero.  
    wall.arrow = 0 #normalize(endPt - startPt)
    
    wall.mode = mode
    wall.oid = int(num)
    wall.inComp = int(1)

    # Add wall into the list of walls
    walls.append(wall)


def readDoors(FileName, debug=True, marginTitle=1, ini=0):
    #doorFeatures = readCSV(FileName, "string")
    #[Num_Doors, Num_Features] = np.shape(doorFeatures)

    doorFeatures, lowerIndex, upperIndex = getData(FileName, '&Door')
    Num_Doors=len(doorFeatures)-marginTitle
    if Num_Doors <= 0:
        doorFeatures, lowerIndex, upperIndex = getData(FileName, '&door')
        Num_Doors=len(doorFeatures)-marginTitle
    if Num_Doors <= 0:
        doorFeatures, lowerIndex, upperIndex = getData(FileName, '&Path')
        Num_Doors=len(doorFeatures)-marginTitle
    if Num_Doors <= 0:
        doorFeatures, lowerIndex, upperIndex = getData(FileName, '&path')
        Num_Doors=len(doorFeatures)-marginTitle
        
    if debug:
        print ('Number of Doors:', Num_Doors, '\n')
        print ('Features of Doors\n', doorFeatures, "\n")
    
    doors = []
    index = 0
    for doorFeature in doorFeatures[marginTitle:]:
        door = passage()
        door.name = str(doorFeature[ini])
        #door.params[0]= float(doorFeature[ini+1])
        #door.params[1]= float(doorFeature[ini+2])
        #door.params[2]= float(doorFeature[ini+3])
        #door.params[3]= float(doorFeature[ini+4])
        
        door.params[0]= min(float(doorFeature[ini+1]),float(doorFeature[ini+3]))
        door.params[1]= min(float(doorFeature[ini+2]),float(doorFeature[ini+4]))
        door.params[2]= max(float(doorFeature[ini+1]),float(doorFeature[ini+3]))
        door.params[3]= max(float(doorFeature[ini+2]),float(doorFeature[ini+4]))
        door.arrow = int(doorFeature[ini+5])
        try:
            door.mode = str(doorFeature[ini+6])
            door.inComp = int(doorFeature[ini+7])
            #door.exitSign = int(doorFeature[ini+8])
        except:
            door.mode = 'rect'
            door.inComp = int(1)
            #door.exitSign = int(1)
        
        # Doors have no exit signs if arrow is 0
        door.exitSign = bool(door.arrow)
        #if door.arrow == 0:
        #    door.exitSign = 0
        #else:
        #    door.exitSign = 1
        # Doors are all in rectangular shape in current progame
        if door.mode != 'rect':
            door.mode = 'rect'
        door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
        door.oid = index
        index = index+1
        doors.append(door)
        
    return doors


#This function addDoor() is created for users to add door in testGeom()
def addDoor(doors, startPt, endPt, mode='rect'):
    num = len(doors)
    door = passage()
    
    if mode == 'rect':
        door.params[0]= min(float(startPt[0]),float(endPt[0]))
        door.params[1]= min(float(startPt[1]),float(endPt[1]))
        door.params[2]= max(float(startPt[0]),float(endPt[0]))
        door.params[3]= max(float(startPt[1]),float(endPt[1]))

    # The arrow is to be tested in simulation.  
    # The default value is no direction assigned, i.e., zero.  
    door.arrow = 0 #normalize(endPt - startPt)
    door.mode = mode   # Currently door has no attribute of "mode"
    door.name = '-G-'

    door.oid = int(num)
    door.inComp = int(1)
    door.exitSign = int(0) # Default: there is no exit sign 
    door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
    
    # Add door into the list of doors
    doors.append(door)
    

#[Num_Doors, Num_DoorFeatures] = np.shape(doorFeatures)
#if np.shape(agent2doors)[0]!= Num_Agents or np.shape(agent2doors)[1]!= Num_Doors:
#    print '\nError on input data: doors or agent2doors \n'
#    print >>f, '\nError on input data: doors or agent2doors \n'


def readExits(FileName, debug=True, marginTitle=1, ini=0):
    #exitFeatures = readCSV(FileName, "string")
    #[Num_Exits, Num_Features] = np.shape(exitFeatures)

    exitFeatures, lowerIndex, upperIndex = getData(FileName, '&Exit')
    Num_Exits=len(exitFeatures)-marginTitle
    if Num_Exits <= 0:
        exitFeatures, lowerIndex, upperIndex = getData(FileName, '&exit')
        Num_Exits=len(exitFeatures)-marginTitle
        
    if debug: 
        print ('Number of Exits:', Num_Exits, '\n')
        print ("Features of Exits\n", exitFeatures, "\n")
    
    exits = []
    index = 0
    for exitFeature in exitFeatures[marginTitle:]:
        exit = passage()
        exit.name = str(exitFeature[ini])
        exit.params[0]= min(float(exitFeature[ini+1]),float(exitFeature[ini+3]))
        exit.params[1]= min(float(exitFeature[ini+2]),float(exitFeature[ini+4]))
        exit.params[2]= max(float(exitFeature[ini+1]),float(exitFeature[ini+3]))
        exit.params[3]= max(float(exitFeature[ini+2]),float(exitFeature[ini+4]))
        exit.arrow = int(exitFeature[ini+5])
        try:
            exit.mode = str(exitFeature[ini+6])
            exit.inComp = int(exitFeature[ini+7])
            #exit.exitSign = int(exitFeature[ini+8])
        except:
            exit.mode = 'rect'
            exit.inComp = int(1)
            #exit.exitSign = int(1)

        # Exits have  exit signs
        exit.exitSign = 1
        # Exits are all in rectangular shape in current progame
        if exit.mode != 'rect':
            exit.mode = 'rect'
        exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
        exit.oid = index
        index = index+1
        exits.append(exit)
        
    return exits


#This function addDoor() is created for users to add door in testGeom()
def addExit(exits, startPt, endPt, mode='rect'):
    num = len(exits)
    exit = passage()
    
    if mode == 'rect':
        #exit.params[0]= float(startPt[0])
        #exit.params[1]= float(startPt[1])
        #exit.params[2]= float(endPt[0])
        #exit.params[3]= float(endPt[1])

        exit.params[0]= min(float(startPt[0]),float(endPt[0]))
        exit.params[1]= min(float(startPt[1]),float(endPt[1]))
        exit.params[2]= max(float(startPt[0]),float(endPt[0]))
        exit.params[3]= max(float(startPt[1]),float(endPt[1]))

    # The arrow is to be tested in simulation.  
    # The default value is no direction assigned, i.e., zero.  
    exit.arrow = 0 #normalize(endPt - startPt)
    exit.mode = mode   # Currently passage class has no attribute of "mode"
    exit.name = '-G-'

    exit.oid = int(num)
    exit.inComp = int(1)
    exit.exitSign = int(0) # Default there is an exit sign
    exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
    
    # Add exit into the list of exits
    exits.append(exit)

    

##############################################
# This function will be used to read CHID from FDS input file
def readCHID(FileName):

    findHEAD=False
    for line in open(FileName):
        if re.match('&HEAD', line):
            findHEAD=True
        if  findHEAD:
            if re.search('CHID', line):
                temp1=line.split('CHID')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                return keyInfo
            if re.search('/', line):
                findHEAD = False
    return None

# Find the first &MESH line in FDS input file and return the value
def readMesh(FileName):
    findMESH=False
    for line in open(FileName):
        if re.match('&MESH', line):
            findMESH=True
        if  findMESH:
            if re.search('IJK', line):
                temp1=line.split('IJK')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xpoints = temp2[0]
                ypoints = temp2[1]
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xmax = temp2[1]-temp2[0]
                ymax = temp2[3]-temp2[2]
            if re.search('/', line):
                findMESH = False
                return xpoints, ypoints, xmax, ymax
                # Only find the first &MESH line
                # The second or other MESH lines are ignored
    return None



def readTEnd(FileName):
    
    findTIME=False
    for line in open(FileName):
        if re.match('&TIME', line):
            findTIME=True
        if  findTIME:
            if re.search('T_END', line):
                temp1=line.split('T_END')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                return keyInfo   # Return a string
            if re.search('/', line):
                findTIME = False
            
    keyInfo=0.0    #If T_END is not found, then return 0.0
    return keyInfo
    #return None
    

# To be added
def readKeyOnce(FileName, Title, Key):
    findTitle=False
    for line in open(FileName):
        if re.match(Title, line):
            findTitle=True
        if  findTitle:
            if re.search(Key, line):
                temp1=line.split(Key)
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                findTitle=False
                return keyInfo
            #if re.match(Title, line)==False and re.match('&', line):
            if re.search('/', line):
                findTitle = False
    return None



### A illustration of OBST PATH and EXIT in RECTANGULAR SHAPE
##############################
### p1-----------------p4  ###
###  |                  |  ###
###  |                  |  ###
###  |                  |  ###
### p2-----------------p3  ###
##############################
            
##############################################
# This function will be used to read OBST from FDS input file
def readOBST(FileName, Keyword='&OBST', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("OBSTout.txt", "w+")
    obstFeatures = []
    findOBST=False
    for line in open(FileName):
        if re.match(Keyword, line):
            findOBST=True
        if  findOBST:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip().strip('=').strip()
                #line1=temp1[1].strip('= ')
                #temp =  line1.split('=')
                #dataXYZ = temp[1].strip()
                coords = re.split(r'[\s\,]+', dataXYZ)
                print(coords)
                obstFeature = []
                obstFeature.append(float(coords[0]))
                obstFeature.append(float(coords[2]))
                obstFeature.append(float(coords[1]))
                obstFeature.append(float(coords[3]))
                obstFeature.append(float(coords[4]))
                obstFeature.append(float(coords[5].rstrip('/')))
                obstFeatures.append(obstFeature)
                findOBST=False

            if debug:
                print (line, '\n', obstFeature)
                #print >>fo, line
                #print >>fo, obstFeature

            #print >>fo, 'test\n'
            #print >>fo, 'OBST Features\n'
            #print >>fo, obstFeatures
    
    walls = []
    index = 0
    for obstFeature in obstFeatures:
        if obstFeature[4]<Zmin and obstFeature[5]<Zmin:
            continue
        if obstFeature[4]>Zmax and obstFeature[5]>Zmax:
            continue
        wall = obst()
        wall.params[0]= float(obstFeature[0])
        wall.params[1]= float(obstFeature[1])
        wall.params[2]= float(obstFeature[2])
        wall.params[3]= float(obstFeature[3])
        wall.arrow = 0
        wall.inComp = 1
        wall.mode = 'rect'
        wall.oid = index
        index = index+1
        walls.append(wall)

    if outputFile is not None:
        updateWallData(walls, outputFile)
        
        '''
        with open(outputFile, mode='w+') as obst_test_file:
            csv_writer = csv.writer(obst_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp', '8/exitSign'])
            index_temp=0
            for obstFeature in obstFeatures:
                if obstFeature[4]<Zmin and obstFeature[5]<Zmin:
                    continue
                if obstFeature[4]>Zmax and obstFeature[5]>Zmax:
                    continue
                csv_writer.writerow(['--', str(obstFeature[0]), str(obstFeature[1]), str(obstFeature[2]), str(obstFeature[3]), '0', 'rect', '1', '0'])
                index_temp=index_temp+1        
        '''
    return walls


#######################################################
# This function will be used to read HOLE or DOOR from FDS input file
def readPATH(FileName, Keyword='&HOLE', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("HOLEout.txt", "w+")
    holeFeatures = []
    
    findPATH=False
    findPATH_XB=False
    findPATH_IOR=False
    for line in open(FileName):
        if re.match(Keyword, line):
            findPATH=True
            findPATH_XB=True
            findPATH_IOR=True
            
        if findPATH:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip().strip('=').strip()
                #line1=temp1[1]
                #temp =  line1.split('=')
                #dataXYZ = temp[1].strip()    
                coords = re.split(r'[\s\,]+', dataXYZ)
                
        #if findPATH and findPATH_IOR:
        #    if re.search('IOR', line):
        #        temp1=line.split('IOR')
        #        dataXYZ=temp1[1].strip().strip('=').strip()
        #        result_IOR = re.split(r'[\s\,]+', dataXYZ)              
        #if findPATH and not findPATH_XB and not findPATH_IOR:            
                holeFeature = []
                holeFeature.append(float(coords[0]))
                holeFeature.append(float(coords[2]))
                holeFeature.append(float(coords[1]))
                holeFeature.append(float(coords[3]))
                holeFeature.append(float(coords[4]))
                holeFeature.append(float(coords[5].rstrip('/')))
                holeFeatures.append(holeFeature)
                findPATH=False

                if debug:
                    print (line, '\n', holeFeature)
                    #print >>fo, line
                    #print >>fo, holeFeature

                #print >>fo, 'test\n'
                #print >>fo, 'HOLE Features\n'
                #print >>fo, holeFeatures

    doors = []
    index = 0
    for holeFeature in holeFeatures:
        if holeFeature[4]<Zmin and holeFeature[5]<Zmin:
            continue
        if holeFeature[4]>Zmax and holeFeature[5]>Zmax:
            continue
        door = passage()
        door.params[0]= float(holeFeature[0])
        door.params[1]= float(holeFeature[1])
        door.params[2]= float(holeFeature[2])
        door.params[3]= float(holeFeature[3])
        door.arrow = 0
        door.oid = index
        index = index+1
        door.inComp = 1
        door.exitSign = 0
        door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
        doors.append(door)
        
    if outputFile: 
        updateDoorData(doors, outputFile)
        
        '''
        with open(outputFile, mode='w+') as door_test_file:
            csv_writer = csv.writer(door_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp', '8/exitSign'])
            index_temp=0
            for holeFeature in holeFeatures:
                if holeFeature[4]<Zmin and holeFeature[5]<Zmin:
                    continue
                if holeFeature[4]>Zmax and holeFeature[5]>Zmax:
                    continue
                csv_writer.writerow(['--', str(holeFeature[0]), str(holeFeature[1]), str(holeFeature[2]), str(holeFeature[3]), '0', 'rect', '1', '0'])
                index_temp=index_temp+1
        '''

    return doors


##############################################
# This function will be used to read EXIT from FDS input file
def readEXIT(FileName, Keyword='&EXIT', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("EXITout.txt", "w+")
    exitFeatures = []
    findEXIT=False
    findEXIT_XB=False
    findEXIT_IOR=False
    
    for line in open(FileName):
        if re.match(Keyword, line):
            findEXIT=True
            findEXIT_XB=True
            findEXIT_IOR=True
            
        if findEXIT:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip().strip('=').strip()
                #line1=temp1[1]
                #temp =  line1.split('=')
                #dataXYZ = temp[1]
                #coords = dataXYZ.split(',')
                coords = re.split(r'[\s\,]+', dataXYZ)
                
        #if findEXIT and findEXIT_IOR:
        #    if re.search('IOR', line):
        #        temp1=line.split('IOR')
        #        dataXYZ=temp1[1].strip().strip('=').strip()
        #        result_IOR = re.split(r'[\s\,]+', dataXYZ)              
        #if findEXIT and not findEXIT_XB and not findEXIT_IOR:
                exitFeature = []
                exitFeature.append(float(coords[0]))
                exitFeature.append(float(coords[2]))
                exitFeature.append(float(coords[1]))
                exitFeature.append(float(coords[3]))
                exitFeature.append(float(coords[4]))
                exitFeature.append(float(coords[5].rstrip('/')))
                exitFeatures.append(exitFeature)
                findEXIT=False

                if debug:
                    print (line, '\n', exitFeature)
                    #print >>fo, line
                    #print >>fo, exitFeature

            
                #print >>fo, 'test\n'
                #print >>fo, 'EXIT Features\n'
                #print >>fo, exitFeatures

        #if re.search('/', line): ???  Not used
        #    findEXIT=False
        #    findEXIT_XB=False
        #    findEXIT_IOR=False

    exits = []
    index = 0
    for exitFeature in exitFeatures:
        if exitFeature[4]<Zmin and exitFeature[5]<Zmin:
            continue
        if exitFeature[4]>Zmax and exitFeature[5]>Zmax:
            continue
        exit = passage()
        exit.params[0]= float(exitFeature[0])
        exit.params[1]= float(exitFeature[1])
        exit.params[2]= float(exitFeature[2])
        exit.params[3]= float(exitFeature[3])
        exit.arrow = 0   #  This need to be improved
        exit.oid = index
        exit.inComp = 1
        exit.exitSign = 0
        exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5

        # In FDS input file exit is a planary surface and agents go into the surface
        # In our simulaiton exit is a rectangular area and agent reach the area
        if exit.params[0]==exit.params[2]:
            exit.params[0]=exit.params[0]-0.3
            exit.params[2]=exit.params[2]+0.3
            exitFeature[0]=exitFeature[0]-0.3
            exitFeature[2]=exitFeature[2]+0.3
            
            
        if exit.params[1]==exit.params[3]:
            exit.params[1]=exit.params[1]-0.3
            exit.params[3]=exit.params[3]+0.3
            exitFeature[1]=exitFeature[1]-0.3
            exitFeature[3]=exitFeature[3]+0.3
            
        exits.append(exit)
        index = index+1

    if outputFile:
        updateExitData(exits, outputFile)
        
        '''
        with open(outputFile, mode='w+') as exit_test_file:
            csv_writer = csv.writer(exit_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp', '8/exitSign'])
            index_temp=0
            for exitFeature in exitFeatures:
                if exitFeature[4]<Zmin and exitFeature[5]<Zmin:
                    continue
                if exitFeature[4]>Zmax and exitFeature[5]>Zmax:
                    continue                
                csv_writer.writerow(['--', str(exitFeature[0]), str(exitFeature[1]), str(exitFeature[2]), str(exitFeature[3]), '0', 'rect', '1', '0'])
                index_temp=index_temp+1
        '''
                
    return exits


def updateAgentData(agents, outputFile, inputFile=None):
    try:
        with open(outputFile, mode='a+', newline='') as agent_test_file:
            csv_writer = csv.writer(agent_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['Agent data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            csv_writer.writerow(['&Agent', '1/iniX', '2/iniY', '3/iniVx', '4/iniVy', '5/tau', '6/tpre', '7/p, 8/pMode, 9/pp2, 10/tpreMode, 11/aType, 12/inComp, 13/talkRange'])
            index_temp=0
            for agent in agents:
                csv_writer.writerow([str(agent.name), str(agent.pos[0]), str(agent.pos[1]), str(agent.actualV[0]), str(agent.actualV[1]), str(agent.tau), str(agent.tpre), str(agent.p), str(agent.pMode), str(agent.pp2), str(agent.tpreMode), str(agent.aType), str(agent.inComp), str(agent.talk_range), str(agent.talk_prob)])
                index_temp=index_temp+1
    except:
        with open(outputFile, mode='wb+') as agent_test_file:
            csv_writer = csv.writer(agent_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['Agent data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            csv_writer.writerow(['&Agent', '1/iniX', '2/iniY', '3/iniVx', '4/iniVy', '5/tau', '6/tpre', '7/p, 8/pMode, 9/pp2, 10/tpreMode, 11/aType, 12/inComp, 13/talkRange'])
            index_temp=0
            for agent in agents:
                csv_writer.writerow([str(agent.name), str(agent.pos[0]), str(agent.pos[1]), str(agent.actualV[0]), str(agent.actualV[1]), str(agent.tau), str(agent.tpre), str(agent.p), str(agent.pMode), str(agent.pp2), str(agent.tpreMode), str(agent.aType), str(agent.inComp), str(agent.talk_range), str(agent.talk_prob)])
                index_temp=index_temp+1
                

def updateDoorData(doors, outputFile, inputFile=None):
    try:
        with open(outputFile, mode='a+', newline='') as door_test_file:
            csv_writer = csv.writer(door_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['DOOR/PATH data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            csv_writer.writerow(['&Door', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp'])
            index_temp=0
            for door in doors:
                csv_writer.writerow(['--', str(door.params[0]), str(door.params[1]), str(door.params[2]), str(door.params[3]), str(door.arrow), str(door.mode), str(door.inComp)])
                index_temp=index_temp+1
    except:
        with open(outputFile, mode='wb+') as door_test_file:
            csv_writer = csv.writer(door_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['DOOR/PATH data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            csv_writer.writerow(['&Door', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp'])
            index_temp=0
            for door in doors:
                csv_writer.writerow(['--', str(door.params[0]), str(door.params[1]), str(door.params[2]), str(door.params[3]), str(door.arrow), str(door.mode), str(door.inComp)])
                index_temp=index_temp+1
                

def updateExitData(doors, outputFile, inputFile=None):
    try:
        with open(outputFile, mode='a+', newline='') as exit_test_file:
            csv_writer = csv.writer(exit_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['EXIT data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            csv_writer.writerow(['&Exit', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp'])
            index_temp=0
            for door in doors:
                csv_writer.writerow(['--', str(door.params[0]), str(door.params[1]), str(door.params[2]), str(door.params[3]), str(door.arrow), str(door.mode), str(door.inComp)])
                index_temp=index_temp+1
    except:
        with open(outputFile, mode='wb+') as exit_test_file:
            csv_writer = csv.writer(exit_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['EXIT data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            csv_writer.writerow(['&Exit', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp'])
            index_temp=0
            for door in doors:
                csv_writer.writerow(['--', str(door.params[0]), str(door.params[1]), str(door.params[2]), str(door.params[3]), str(door.arrow), str(door.mode), str(door.inComp)])
                index_temp=index_temp+1
            

def updateWallData(walls, outputFile, inputFile=None):
    try:
        with open(outputFile, mode='a+', newline='') as wall_test_file:
            csv_writer = csv.writer(wall_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['WALL/OBST data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            csv_writer.writerow(['&Wall', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp'])
            index_temp=0
            for wall in walls:
                csv_writer.writerow(['--', str(wall.params[0]), str(wall.params[1]), str(wall.params[2]), str(wall.params[3]), str(wall.arrow), str(wall.mode), str(wall.inComp)])
                index_temp=index_temp+1
    except:
        with open(outputFile, mode='wb+') as wall_test_file:
            csv_writer = csv.writer(wall_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['WALL/OBST data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            csv_writer.writerow(['&Wall', '1/startX', '2/startY', '3/endX', '4/endY', '5/arrow', '6/shape', '7/inComp'])
            index_temp=0
            for wall in walls:
                csv_writer.writerow(['--', str(wall.params[0]), str(wall.params[1]), str(wall.params[2]), str(wall.params[3]), str(wall.arrow), str(wall.mode), str(wall.inComp)])
                index_temp=index_temp+1
            

# Not used after the flow solver is integrated into our program
# This function was originally developed to dump exit2door data in TestGeom
def updateExit2Doors(exit2doors, outputFile, inputFile=None):
    (I, J) = np.shape(exit2doors)
    #print "The size of exit2door:", [I, J]
    #dataNP = np.zeros((I+1, J+1))

    dataNP=[]
    for i in range(I+1):
        row=[]
        if i==0:
            row.append('&Exit2Door')
            for j in range(1, J+1):
                row.append('DoorID'+str(j-1))
        else:
            row.append('ExitID'+str(i-1))
            for j in range(1, J+1):
                row.append(str(int(exit2doors[i-1, j-1])))
            
        dataNP.append(row)

    #dataNP[1:, 1:] = exit2doors
    #np.savetxt(fileName, dataNP, delimiter=',', fmt='%s')   #'2darray.csv'
    try:
        with open(outputFile, mode='a+', newline='') as exit2door_file:
            csv_writer = csv.writer(exit2door_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['exit2door data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            for i in range(I+1):
                #print(dataNP[i])
                csv_writer.writerow(dataNP[i])
    
    except:
        with open(outputFile, mode='wb+') as exit2door_file:
            csv_writer = csv.writer(exit2door_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([])
            if inputFile is not None:
                csv_writer.writerow([inputFile])
            csv_writer.writerow(['exit2door data in TestGeom: '])
            csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
            #csv_writer.writerow(['&Wall', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/shape', '6/inComp'])
            #index_temp=0
            for i in range(I+1):
                csv_writer.writerow(dataNP[i])
            #for wall in walls:
            #    csv_writer.writerow(['--', str(wall.params[0]), str(wall.params[1]), str(wall.params[2]), str(wall.params[3]), str(wall.arrow), str(wall.mode), str(wall.inComp)])
            #    index_temp=index_temp+1
    
    


##############################################################
# The function writeFRec is modified from Topi's work
# python script: readFRec (by Topi on Google Forum)
# readFRec: Read fortran record, return payload as bytestring
##############################################################
#
def writeFRec(infile, fmt, data):
    len1 = np.size(data)
    if len1==0 or data is None:
        #len2=infile.read(4)
        #infile.write(0x00)
        temp = struct.pack('@I', 0)
        infile.write(temp)
    
        return None
    
    #if fmt=='s':
        #result  = struct.pack('@I', data.encode())
    #    infile.write(data.encode())
    # Not try data.encode().  Use standard format to write data
        
    fmt2 = str(len1)+fmt
    num  = len1 * struct.calcsize(fmt)
    
    # length of the data
    num2   = struct.pack('@I', num)
    infile.write(num2)
    
    # Modified on 2022 Apr2: Handle string type differently from int and float type
    if fmt=='s':
        result = struct.pack(fmt, data.encode())
        infile.write(result)
    
        # End symbol
        temp = struct.pack('@I', 0)
        infile.write(temp)
        return "write a string"

    # Write data
    for i in range(len1):
        result = struct.pack(fmt, data[i])
        infile.write(result)
    
    # End symbol
    temp = struct.pack('@I', 0)
    infile.write(temp)
    

    
#Read fortran record, return payload as bytestring
def readFRec(infile,fmt):
    len1   = infile.read(4)
    if not len1:
        return None
    len1   = struct.unpack('@I', len1)[0]

    if len1==0:
        len2=infile.read(4)
        return None
    num    = int(len1/struct.calcsize(fmt))
    fmt2   = str(num)+fmt
    if num>1:
        result = struct.unpack(fmt2,infile.read(len1))
    else:
        result = struct.unpack(fmt2,infile.read(len1))[0]
    len2   = struct.unpack('@I', infile.read(4))[0]
    if fmt == 's':
        result=result[0] #.rstrip()
    return result


#################################
# The function readPRTfile
def readPRTfile(fname, max_time=float('inf'), mode='evac'):

    fin = open(fname,'rb')
    #if wrtxt:
    #    temp = fname.split('.prt5')
    #    outfile = open(temp[0] + ".txt", "w")
    
    one_integer=readFRec(fin,'I')  #! Integer 1 to check Endian-ness
    version=readFRec(fin,'I')       # FDS version number
    n_part=readFRec(fin,'I')        # Number of PARTicle classes
    #print(n_part)
    q_labels = []
    q_units  = []
    for npc in range(0,n_part):
        n_quant,zero_int=readFRec(fin,'I')  # EVAC_N_QUANTITIES, ZERO_INTEGER
        for nq in range(0,n_quant):
            smv_label=readFRec(fin,'s')
            #print(smv_label)
            units    =readFRec(fin,'s')
            q_units.append(units)  
            q_labels.append(smv_label)
    #if wrtxt:
    #    outfile.write("one_integer:" + str(one_integer) + "\n")    
    #    outfile.write("n_part:" + str(n_part) + "\n") 
    #    outfile.write("n_quant:" + str(n_quant) + "\n")
        
    Q=[]
    T  = []
    #diam =[] ??? Not used in this program
    XYZ = []
    TAG = []
    while True:

        Time  = readFRec(fin,'f')  # Time index
        if Time == None or Time>max_time:
            break
        nplim = readFRec(fin,'I')  # Number of particles in the PART class
        if nplim>0:
            xyz  = np.array(readFRec(fin,'f'))
            tag  = np.array(readFRec(fin,'I'))
            q    = np.array(readFRec(fin,'f'))

            #print >> outfile, "g", q, "\n"
            if mode=='evac':
                xyz.shape = (7,nplim) # evac data: please check dump_evac() in evac.f90
            else: 
                xyz.shape = (3,nplim) # particle data: please check dump_part() in dump.f90
            
            q.shape   = (n_quant, nplim)
            
            #if wrtxt:
            #    outfile.write("Time:" + str(Time) + "\n")
            #    outfile.write("xyz:" + str(xyz) + "\n") 
            #    outfile.write("tag:" + str(tag) + "\n")           
            #    outfile.write( "q:" + str(q) + "\n")

            # process timestep data
            T.append(Time)
            XYZ.append(xyz)
            TAG.append(tag)
            Q.append(q)
        else:
            tmp = fin.read(24)
    
    fin.close()
    #if wrtxt:
    #    outfile.close()
    #np.savez( outfn + ".npz", T, XYZ, TAG, Q)
    #return (np.array(T),np.hstack(Q),q_labels,q_units)
    return T, XYZ, TAG, Q, n_part, version, n_quant


def intiPrt(fileName, num_agents, debug=True):
    
    n_part=1  # Number of PARTicle classes
    [n_quant,zero_int]=[20,0]  # Number of particle features
    
    #filename=open('test.bin', 'wb+')
    writeFRec(fileName, 'I', [1])      #! Integer 1 to check Endian-ness
    writeFRec(fileName, 'I', [num_agents])    # FDS version number
    writeFRec(fileName, 'I', [n_part]) # Number of PARTicle classes
    for npc in range(n_part):
        writeFRec(fileName, 'I', [n_quant, zero_int])
        for nq in range(n_quant):
            if nq == 0:
                writeFRec(fileName,'s', "actual Vx") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
                #q_units.append(units)  
                #q_labels.append(smv_label)
            if nq ==1:
                writeFRec(fileName,'s', "actual Vy") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
                #q_units.append(units)  
                #q_labels.append(smv_label)
            if nq ==2:
                writeFRec(fileName,'s', "desired Vx") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
            if nq ==3:
                writeFRec(fileName,'s', "desired Vy") # smv_label
                writeFRec(fileName,'s', "m/s") 
            if nq ==4:
                writeFRec(fileName,'s', "motive Fx") # smv_label
                writeFRec(fileName,'s', "N")        # units
            if nq ==5:
                writeFRec(fileName,'s', "motive Fy") # smv_label
                writeFRec(fileName,'s', "N")        # units
            if nq ==6:
                writeFRec(fileName,'s', "group Fx") # smv_label
                writeFRec(fileName,'s', "N")        # units
            if nq ==7:
                writeFRec(fileName,'s', "group Fy") # smv_label
                writeFRec(fileName,'s', "N")        # units            
            if nq ==8:
                writeFRec(fileName,'s', "self-repulsion Fx") # smv_label
                writeFRec(fileName,'s', "N")        # units
            if nq ==9:
                writeFRec(fileName,'s', "self-repulsion Fy") # smv_label
                writeFRec(fileName,'s', "N")        # units     

            if nq ==10:
                writeFRec(fileName,'s', "subjective Fx") # smv_label
                writeFRec(fileName,'s', "N")        # units
            if nq ==11:
                writeFRec(fileName,'s', "subjective Fy") # smv_label
                writeFRec(fileName,'s', "N")        # units     
                
            if nq ==12:
                writeFRec(fileName,'s', "objective Fx") # smv_label
                writeFRec(fileName,'s', "N")        # units
            if nq ==13:
                writeFRec(fileName,'s', "objectiven Fy") # smv_label
                writeFRec(fileName,'s', "N")        # units     

            if nq ==14:
                writeFRec(fileName,'s', "t premovement") # smv_label
                writeFRec(fileName,'s', "s")        # units
            if nq ==15:
                writeFRec(fileName,'s', "exit selected") # smv_label
                writeFRec(fileName,'s', "Null")        # units     

            if nq ==16:
                writeFRec(fileName,'s', "num_see_others") # smv_label
                writeFRec(fileName,'s', "Null")        # units
            if nq ==17:
                writeFRec(fileName,'s', "num_others") # smv_label
                writeFRec(fileName,'s', "Null")        # units   
                
            if nq ==18:
                writeFRec(fileName,'s', "ratioV") # smv_label
                writeFRec(fileName,'s', "Null")        # units
            if nq ==19:
                writeFRec(fileName,'s', "stressLevel") # smv_label
                writeFRec(fileName,'s', "Null")        # units   

#################################################
# This function is used to dump evac prt5 data file
# so that the simulation result can be visualized by smokeview
#################################################
def dump_evac(agents, fileName, T, debug=True):
    
    num = len(agents)
    
    x=[]
    y=[]
    z=[]
    ap1=[]
    ap2=[]
    ap3=[]
    ap4=[]
    
    tag=[]
    # n_quant = ?  Please revise in intiPrt()
    Q_actualVx=[]
    Q_actualVy=[]
    
    Q_desiredVx=[]
    Q_desiredVy=[]

    Q_motiveFx=[]
    Q_motiveFy=[]
    Q_socialFx=[]
    Q_socialFy=[]

    Q_selfrepFx=[]
    Q_selfrepFy=[]
    
    Q_subFx=[]
    Q_subFy=[]
    Q_objFx=[]
    Q_objFy=[]
    
    Q_tpre=[]
    Q_exit=[]
    
    Q_numOtherSee=[]
    Q_numOther=[]
    
    Q_arousal=[]
    Q_stressLevel=[]
    
    Q_doorFx=[]
    Q_doorFy=[]
    
    Q_wallFx=[]
    Q_wallFy=[]
    
    for agent in agents:
        if agent.inComp == 0:
            continue
        
        x.append(agent.pos[0])
        y.append(agent.pos[1])
        z.append(1.5)

        # 180* np.arctan2(agent.actualV[1], agent.actualV[0]) /pi
        #angle = vectorAng(agent.actualV)
        ap1.append(vectorAng(agent.actualV))        # velocity direction  Agent HR angle is [0,2PI)
        ap2.append(0.1)     # diameter
        ap3.append(0.05)    #torso diameter
        ap4.append(1.0)     # height
        
        tag.append(agent.ID)

        Q_actualVx.append(agent.actualV[0])
        Q_actualVy.append(agent.actualV[1])

        Q_desiredVx.append(agent.desiredV[0])
        Q_desiredVy.append(agent.desiredV[1])

        Q_motiveFx.append(agent.motiveF[0])
        Q_motiveFy.append(agent.motiveF[1])
        Q_socialFx.append(agent.socialF[0])
        Q_socialFy.append(agent.socialF[1])
        
        Q_selfrepFx.append(agent.selfrepF[0])
        Q_selfrepFy.append(agent.selfrepF[1])
        
        Q_subFx.append(agent.subF[0])
        Q_subFy.append(agent.subF[1])
        
        Q_objFx.append(agent.objF[0])
        Q_objFy.append(agent.objF[1])
        
        Q_tpre.append(agent.tpre)
        try:
            Q_exit.append(agent.exitInMind.oid)
        except:
            Q_exit.append(int(0))
        
        Q_numOtherSee.append(len(agent.seeothers))
        Q_numOther.append(len(agent.others))
        
        Q_arousal.append(agent.arousalLevel)
        Q_stressLevel.append(agent.stressLevel)

        Q_doorFx.append(agent.doorF[0])
        Q_doorFy.append(agent.doorF[1])
        
        Q_wallFx.append(agent.wallrepF[0])
        Q_wallFy.append(agent.wallrepF[1])
        
    NPLIM=np.size(tag)
    # ??? what happens if tag is an empty list
    # if tag is empty, do not write agent data to the binary file
    xyz=x+y+z+ap1+ap2+ap3+ap4
    # tag=tag  tag is already OK
    Q=Q_actualVx +Q_actualVy +Q_desiredVx +Q_desiredVy +Q_motiveFx +Q_motiveFy\
    +Q_socialFx +Q_socialFy +Q_selfrepFx +Q_selfrepFy\
    +Q_subFx +Q_subFy +Q_objFx+ Q_objFy+ Q_tpre+ Q_exit+ Q_numOtherSee +Q_numOther\
    +Q_arousal +Q_stressLevel
    
    writeFRec(fileName, 'f', [T])
    writeFRec(fileName, 'I', [NPLIM])
    if NPLIM>0:
        writeFRec(fileName, 'f', xyz)
        writeFRec(fileName, 'I', tag)
        writeFRec(fileName, 'f', Q)


# Show simulation by pygame
def compute_simu(simu):

    # The file to record the output data of simulation
    FN_Temp = simu.outDataName + ".txt"
    f = open(FN_Temp, "a+")
    #simu.outFileName=f

    f.write("Start and compute simulation here.")
    # f.write('FN_FDS=', simu.FN_FDS)
    # f.write('FN_EVAC=', simu.FN_EVAC #,'\n')

    if not simu.inputDataCorrect:
        print("Input data is not correct!  Please modify input data file!")
        return

    # Initialize prt file in draw_func.py
    if simu.dumpBin:
        #fbin = open(simu.fpath + '\\' + simu.outDataName +'.bin', 'wb+')
        fbin = open(simu.outDataName +'.bin', 'wb+')
        intiPrt(fbin, simu.num_agents)
        
        npzTime=[]
        npzSee = np.zeros((1, simu.num_agents, simu.num_agents))
        npzComm = np.zeros((1, simu.num_agents, simu.num_agents))
        npzTalk = np.zeros((1, simu.num_agents, simu.num_agents))
    
        npzP = np.zeros((1, simu.num_agents, simu.num_agents))
        npzD = np.zeros((1, simu.num_agents, simu.num_agents))
        npzC = np.zeros((1, simu.num_agents, simu.num_agents))
        npzA = np.zeros((1, simu.num_agents, simu.num_agents))
        npzB = np.zeros((1, simu.num_agents, simu.num_agents))

        npzVD = np.zeros((1, simu.num_agents, simu.num_doors))
        npzVE = np.zeros((1, simu.num_agents, simu.num_exits))
        npzEP = np.zeros((1, simu.num_agents, simu.num_exits))
        
        dump_evac(simu.agents, fbin, simu.t_sim)
        npzTime.append(simu.t_sim)
        
        if len(npzTime)==1:
            npzSee[0,:,:]=person.see_flag

        if len(npzTime)==1:
            npzComm[0,:,:]=person.comm

        if len(npzTime)==1:
            npzTalk[0,:,:]=person.talk

        if len(npzTime)==1:
            npzP[0,:,:]=person.PFactor
            
        if len(npzTime)==1:
            npzD[0,:,:]=person.DFactor

        if len(npzTime)==1:
            npzC[0,:,:]=person.CFactor

        if len(npzTime)==1:
            npzA[0,:,:]=person.AFactor

        if len(npzTime)==1:
            npzB[0,:,:]=person.BFactor
        
        if len(npzTime)==1:
            npzVD[0,:,:]=person.visible_doors

        if len(npzTime)==1:
            npzVE[0,:,:]=person.visible_exits
        
        if len(npzTime)==1:
            npzEP[0,:,:]=person.exit_prob
        
    ##########################################
    ### Simulation starts here: Only Compute
    ##########################################

    simu.t_sim = 0.0
    simu.tt_OtherList = 0.0
    #t_pause=0.0
    running = True
    while running and simu.t_sim < simu.t_end:
        
        # Computation Step
        if simu.t_sim > 0.0:
            simu.simulation_update_agent_velocity()
            simu.simulation_update_agent_position()
        simu.simulation_step2022(f)
        simu.simulation_update_agent_desiredV(f)
        simu.simulation_update_agent_force(f)
        #simu.t_sim = simu.t_sim + simu.DT  # Maybe it should be in step()
        pass
        
        print('Current simulation time:', simu.t_sim, '\n')
        f.write('Current simulation time:'+str(simu.t_sim)+'\n')
        
        # Dump agent binary data file
        if simu.dumpBin and simu.t_sim >= simu.tt_DumpData:
            dump_evac(simu.agents, fbin, simu.t_sim)
            simu.tt_DumpData = simu.tt_DumpData + simu.DT_DumpData
            npzTime.append(simu.t_sim)
            
            if len(npzTime)==1:
                npzSee[0,:,:]=person.see_flag
            else:
                tempSee=np.zeros((1, simu.num_agents, simu.num_agents))
                tempSee[0,:,:]=person.see_flag
                npzSee = np.concatenate((npzSee, tempSee), axis=0)
            
            if len(npzTime)==1:
                npzComm[0,:,:]=person.comm
            else:
                tempComm=np.zeros((1, simu.num_agents, simu.num_agents))
                tempComm[0,:,:]=person.comm
                npzComm = np.concatenate((npzComm, tempComm), axis=0) 
                
            if len(npzTime)==1:
                npzTalk[0,:,:]=person.talk
            else:
                tempTalk=np.zeros((1, simu.num_agents, simu.num_agents))
                tempTalk[0,:,:]=person.talk
                npzTalk = np.concatenate((npzTalk, tempTalk), axis=0)

            if len(npzTime)==1:
                npzP[0,:,:]=person.PFactor
            else:
                tempP=np.zeros((1, simu.num_agents, simu.num_agents))
                tempP[0,:,:] =person.PFactor
                npzP = np.concatenate((npzP, tempP), axis=0)
                
            if len(npzTime)==1:
                npzD[0,:,:]=person.DFactor
            else:
                tempD=np.zeros((1, simu.num_agents, simu.num_agents))
                tempD[0,:,:] =person.DFactor
                npzD = np.concatenate((npzD, tempD), axis=0)

            if len(npzTime)==1:
                npzC[0,:,:]=person.CFactor
            else:
                tempC=np.zeros((1, simu.num_agents, simu.num_agents))
                tempC[0,:,:] =person.CFactor
                npzC = np.concatenate((npzC, tempC), axis=0)

            if len(npzTime)==1:
                npzA[0,:,:]=person.AFactor
            else:
                tempA=np.zeros((1, simu.num_agents, simu.num_agents))
                tempA[0,:,:] =person.AFactor
                npzA = np.concatenate((npzA, tempA), axis=0)

            if len(npzTime)==1:
                npzB[0,:,:]=person.BFactor
            else:
                tempB=np.zeros((1, simu.num_agents, simu.num_agents))
                tempB[0,:,:] =person.BFactor
                npzB = np.concatenate((npzB, tempB), axis=0)

            if len(npzTime)==1:
                npzVD[0,:,:]=person.visible_doors
            else:
                tempVD=np.zeros((1, simu.num_agents, simu.num_doors))
                tempVD[0,:,:] =person.visible_doors
                npzVD = np.concatenate((npzVD, tempVD), axis=0)

            if len(npzTime)==1:
                npzVE[0,:,:]=person.visible_exits
            else:
                tempVE=np.zeros((1, simu.num_agents, simu.num_exits))
                tempVE[0,:,:] =person.visible_exits
                npzVE = np.concatenate((npzVE, tempVE), axis=0)
                
            if len(npzTime)==1:
                npzEP[0,:,:]=person.exit_prob
            else:
                tempEP=np.zeros((1, simu.num_agents, simu.num_exits))
                tempEP[0,:,:] =person.exit_prob
                npzEP = np.concatenate((npzEP, tempEP), axis=0)

    f.close()
    
    npzRadius = []
    npzMass = []
    for agent in simu.agents:
        npzRadius.append(agent.radius)
        npzMass.append(agent.mass)
        
    if simu.dumpBin:
        fbin.close()
        #np.savez(simu.outDataName +'.npz', npzTime, npzSee, npzComm, npzTalk, npzP, npzD, npzC, npzB, npzA)
        
        np.savez(simu.outDataName +'.npz', npzTime, npzSee, npzComm, npzTalk, \
        npzP, npzD, npzC, npzB, npzA, \
        npzVD, npzVE, npzEP, npzRadius, npzMass)
    
    
    '''
    if simu.autoPlot:
        
        try:
            visualizeTpre(simu.outDataName +'.bin')
            
            #np.histogram() ??
            
            if len(simu.exits)>0:
                plt.bar(np.arange(len(simu.exits)), simu.exitUsage)
                plt.title("Exit Usage Histogram:")
                plt.grid()
                plt.legend(loc='best')
                plt.xlabel("Exit_Index")
                plt.ylabel("Num_of_Agents")
                plt.show()
        except:
            input("Unable to plot figures from output data!  Please check!")
    '''
    

if __name__ == '__main__':

    test = readCSV_base(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    print(test)
    doorFeatures = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Door')
    
    #print (doorFeatures)
    print (np.shape(doorFeatures))

    pedFeatures = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Ped')
    #print (pedFeatures)
    print (np.shape(pedFeatures))

    agents = readAgents("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    walls = readWalls("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    doors = readDoors("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    exits = readExits("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    
    print ('Length of agents:', len(agents))
    print ('Length of walls:', len(walls))
    
    ped2ExitFeatures, LowerIndex, UpperIndex = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Ped2Exit')
    #print (ped2ExitFeatures)
    matrix = np.zeros((len(agents), len(exits)))
    
    for i in range(len(agents)):
            for j in range(len(exits)):
                matrix[i,j] = float(ped2ExitFeatures[i+1][j+1])
    print ('matrix', matrix)

    #Exit2DoorFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Exit2Door')
    #print (Exit2DoorFeatures)
    #matrix = np.zeros((len(exits), len(doors)))
    #for i in range(len(exits)):
    #        for j in range(len(doors)):
    #            matrix[i,j] = float(Exit2DoorFeatures[i+1][j+1])
    #print ('matrix', matrix)
    
        #for index in range(Num_Data):
        #if dataFeatures[0,index]=='&Ped':
        #    IPedStart=index
        #    while dataFeatures[0,index]!='':
        #        index=index+1
        #    IPedEnd=index

    #agentFeatures = dataFeatures[IPedStart : IPedEnd]
    #[Num_Agents, Num_Features] = np.shape(agentFeatures)

    #doors = readDoors("doorData2019.csv", True)
    #exits = readExits("doorData2018.csv", True)
    
    # Initialize Desired Interpersonal Distance
    #DFactor_Init = readCSV("D_Data2018.csv", 'float')
    #AFactor_Init = readCSV("A_Data2018.csv", 'float')
    #BFactor_Init = readCSV("B_Data2018.csv", 'float')

    tableFeatures, LowerIndex, UpperIndex = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&groupB')
    BFactor_Init = readFloatArray(tableFeatures, len(agents), len(agents))
    BFactor_Init

    # Input Data Check
    #[Num_D1, Num_D2]=np.shape(DFactor_Init)
    #[Num_A1, Num_A2]=np.shape(AFactor_Init)
    #[Num_B1, Num_B2]=np.shape(BFactor_Init)

    #print >>f, np.shape(DFactor_Init), [Num_Agents, Num_Agents], '\n'

    print('\n', 'Test Output: exit2door.csv')
    exit2door=np.array([[ 1.0,  1.0,  1.0], [ 1.0,  -1.0,  -2.0], [ 1.0,  1.0,  1.0]])
    #print(exit2door)
    updateExit2Doors(exit2door, 'test_exit2door.csv')
    
    readDoorProb(r'/mnt/sda6/gitwork2022/CrowdEgress/examples/3Doors/ped2023Jan_2023-05-16_02_11_26.txt',0)
    
    
""" Test struct to read and write binary data
    n_part=2
    [n_quant,zero_int]=[1,0]
    f=open('test.bin', 'wb+')
    writeFRec(f, 'I', [1])      #! Integer 1 to check Endian-ness
    writeFRec(f, 'I', [653])    # FDS version number
    writeFRec(f, 'I', [n_part]) # Number of PARTicle classes
    for npc in range(n_part):
        writeFRec(f, 'I', [n_quant, zero_int])
        for nq in range(n_quant):
            smv_label =writeFRec(f,'s', "test")
            units     =writeFRec(f,'s', "Newton")
            #q_units.append(units)  
            #q_labels.append(smv_label)
    x1=[1.0, 2.0, 3.0]
    writeFRec(f, 'f', x1)
    x2=[1,2,3]
    writeFRec(f, 'I', x2)
    x3="abcdefg"
    writeFRec(f, 's', x3)
    f.close()
    
    f=open('test.bin', 'rb')
    testEnd =readFRec(f, 'I')
    ver =readFRec(f, 'I')
    n_part =readFRec(f, 'I')
    y1 = readFRec(f, 'f')
    y2 = readFRec(f, 'I')
    y3 = readFRec(f, 's') 
    print testEnd
    print ver
    print n_part
    print y1
    print y2
    print y3
    
"""
