
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


import os, sys
from random import randint, choice, normalvariate
#from math import sin, cos, radians, floor, ceil
from math import *
import numpy as np
import re
import random
import time
#from random import *

from agent import *
from obst import *
from math_func import *
from data_func import *
from draw_func import *
from flow import *
from ui import*


class simulation(object):

    # basic defaults

    # Below are variables for users to set up pygame features
    ################################################################

    ZOOMFACTOR = 20.0    	
    xSpace=30.0
    ySpace=60.0
    #self.xyShift = np.array([xSpace, ySpace])

    #SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
    #GRID_SIZE = 20, 20
    #FIELD_SIZE = 500, 500
    #FIELD_LIMITS = 0, 0, 600, 600
    #field_bgcolor = white

    # Some variables for visualization of the simulation by pygame
    # They should be packed up into visControl class
    THREECIRCLES = False  	# Use 3 circles to draw agents
    SHOWVELOCITY = True	# Show velocity and desired velocity of agents
    SHOWINDEX = True        # Show index of agents
    SHOWTIME = True         # Show a clock on the screen
    SHOWINTELINE = True     # Draw a line between interacting agents
    MODETRAJ = False        # Draw trajectory of agents' movement
    PAUSE = False
    SHOWNAME = False
    SHOWMESH = False
    SHOWWALLDATA = True
    SHOWDOORDATA = True
    SHOWEXITDATA = True
    SHOWSTRESS = False
    DRAWWALLFORCE = True
    DRAWDOORFORCE = True
    DRAWGROUPFORCE = True
    DRAWSELFREPULSION = True
    
        
    def __init__(self, outputFileName=None, params=None):

        # Job Title
        self.CHID=''

        # Time parameters
        self.DT = 0.3
        self.t_sim=0.0
        self.t_end=float('inf')
        self.t_pause=0.0

        # A Logical Varible to Control if TestGeom Goes to Simulation
        self.continueToSimu=False
        
        self.DT_DumpData = self.DT
        self.tt_DumpData = 0.0
        
        self.DT_OtherList = 3.0
        self.tt_OtherList = 0.0

        self.DT_ChangeDoor = 3.0
        self.tt_ChangeDoor = 0.0

        # Below are variables to set up the simulation
        ################################################################
        self.TIMECOUNT = True
        self.WALLBLOCKHERDING = True
        self.TESTFORCE = True
        #self.TPREMODE = 2        ### Instructinn: 1 -- DesiredV = 0  2 -- Motive Force =0: 
        self.GROUPBEHAVIOR = True     # Enable the group social force
        self.SELFREPULSION = True      # Enable self repulsion
        self.FLUCTUATION = True        # Enable Fluctuation Force: Mainly useful for particles
        self.INTERACTION = 0
        self.OPINIONMODEL = 0
        self.DEBUG = True

        #self.DEBUGFORCE = False
        #self.DEBUGTAR = False
        #self.GUI = True
        #self.STARTPAGE = False
        #self.COHESION = False

        # Entities in simulation: Agnets Walls Doors Exits
        self.agents=[]
        self.walls=[]
        self.doors=[]
        self.exits=[]

        self.agent2exit = []
        self.exit2door = []
        self.exitUsage = None

        self.num_agents=0
        self.num_walls=0
        self.num_doors=0
        self.num_exits=0

        self.inComp_agents=0
        self.inComp_walls=0
        self.inComp_doors=0
        self.inComp_exits=0
        
        self.inputDataCorrect = True
        self.FN_FDS=None
        self.FN_EVAC = None
        self.outDataName =outputFileName

        if self.outDataName is None:
            self.outDataName ="outData"

        self.fpath = None # Input file path
        
        #self.autoPlotLogic = True
        #self.readConfig = True # Boolean Flag
        self.dumpBin = True # Boolean Flag
        #self.fbin = None    # File pointer
        #self.fnameBin = None  # Binary file path and name

        # intiPrt(simu.fbin)  # Have move this line in draw_func.py: show_simu()
        # Note that the birnary data file is created and written when simulation has started.
        # Note that the birnary data file is not in the phase of TestGeom

        #self.t_now =0.0
        #self.t_pause = 0.0

        self.solver=2
        self.bldmesh = None

        #Human Mesh Data
        self.xmin=None
        self.xmax=None
        self.ymin=None
        self.ymax=None
        self.xpt=None
        self.ypt=None
        self.dx=None
        self.dy=None

        self.zmin=None
        self.zmax=None
        # self.zpt is always one because this is 2D problem
        
        self.UallExit=None
        self.VallExit=None

        self.UeachExit=None
        self.VeachExit=None

        self.flucNoiseLevel = 1.0
    
    
    """
    def intiPrt(self, debug=True):
    
        n_part=1  # Number of PARTicle classes
        [n_quant,zero_int]=[1,0]  # Number of particle features
    
        fileName = open(self.outDataName +'.bin', 'wb+')
        writeFRec(fileName, 'I', [1])      #! Integer 1 to check Endian-ness
        writeFRec(fileName, 'I', [653])    # FDS version number
        writeFRec(fileName, 'I', [n_part]) # Number of PARTicle classes
        for npc in range(n_part):
            writeFRec(fileName, 'I', [n_quant, zero_int])
            for nq in range(n_quant):
                smv_label =writeFRec(fileName,'s', "test")
                units     =writeFRec(fileName,'s', "Newton")
                #q_units.append(units)  
                #q_labels.append(smv_label)
    """
    

    def select_file(self, FN_EVAC=None, FN_FDS=None, mode='smallGUI'):

        FN_Temp = "log.txt"
        
        if os.path.exists(FN_Temp) and FN_EVAC is None and FN_FDS is None and mode=="smallGUI":
            for line in open(FN_Temp, "r"):
                if re.match('FN_FDS', line):
                    temp =  line.split('=')
                    FN_FDS = temp[1].strip()
                if re.match('FN_EVAC', line):
                    temp =  line.split('=')
                    FN_EVAC = temp[1].strip()
                    
                #if re.match('ZOOM', line):
                #    temp =  line.split('=')
                #    self.ZOOMFACTOR = float(temp[1].strip())                    
                #if re.match('xSpace', line):
                #    temp =  line.split('=')
                #    self.xSpace = float(temp[1].strip())
                #if re.match('ySpace', line):
                #    temp =  line.split('=')
                #    self.ySpace = float(temp[1].strip())
                #if re.match('solver', line):
                #    temp =  line.split('=')
                #    self.solver = int(temp[1].strip())
                    
        # This is used for debug mode
        if self.DEBUG: #and sys.version_info[0] == 2: 
            print(FN_FDS)
            print(FN_EVAC)
            print("As above is the input file selected in your last run!")
            #raw_input('Input File Selection from Last Run.')

        # Update the data in simulation class
        self.FN_FDS = FN_FDS
        self.FN_EVAC = FN_EVAC
                
        temp = os.path.split(FN_EVAC)
        self.fpath = os.path.abspath(temp[0])
        #temp = os.path.split(FN_FDS)
        #self.fdspath = temp[0]
        #self.fpath = os.path.split(FN_EVAC)[0]
        self.outDataName= re.split('.csv', FN_EVAC)[0]+'_'+time.strftime('%Y-%m-%d_%H_%M_%S')
        #self.outDataName = os.path.join(self.fpath, self.outDataName)

        if self.DEBUG:
            print(self.outDataName)
            #raw_input('Please check output data path and filename!')
        #self.fnameBin = FN_EVAC.rstrip('.csv')+self.outDataName+'.bin'
        
        
        FN_Temp = os.path.join(self.fpath, "config.txt")
        if os.path.exists(FN_Temp):
            for line in open(FN_Temp, "r"):
                #if re.match('FN_FDS', line):
                #    temp =  line.split('=')
                #    FN_FDS = temp[1].strip()
                #if re.match('FN_EVAC', line):
                #    temp =  line.split('=')
                #    FN_EVAC = temp[1].strip()
                if re.match('ZOOM', line):
                    temp =  line.split('=')
                    self.ZOOMFACTOR = float(temp[1].strip())                    
                if re.match('xSpace', line):
                    temp =  line.split('=')
                    self.xSpace = float(temp[1].strip())
                if re.match('ySpace', line):
                    temp =  line.split('=')
                    self.ySpace = float(temp[1].strip())
                if re.match('solver', line):
                    temp =  line.split('=')
                    self.solver = int(temp[1].strip())
                if re.match('dumpBinary', line):
                    temp =  line.split('=')
                    self.dumpBin = bool(temp[1].strip())
        '''
                # Mesh parameters
                if re.match('xmin', line):
                    temp =  line.split('=')
                    self.xmin = int(temp[1].strip())
                if re.match('xmax', line):
                    temp =  line.split('=')
                    self.xmax = int(temp[1].strip())
                if re.match('ymin', line):
                    temp =  line.split('=')
                    self.ymin = int(temp[1].strip())
                if re.match('ymax', line):
                    temp =  line.split('=')
                    self.ymax = int(temp[1].strip())
                if re.match('xpt', line):
                    temp =  line.split('=')
                    self.xpt = int(temp[1].strip())
                if re.match('ypt', line):
                    temp =  line.split('=')
                    self.ypt = int(temp[1].strip())
        '''
        
        # This is a simple user interface to select input files
        if mode=="smallGUI":
            [self.FN_FDS, self.FN_EVAC] = startPage(FN_FDS, FN_EVAC)

        # The file to record the output data of simulation
        # FN_Temp = "log.txt" #self.outDataName + ".txt"
        f = open("log.txt", "a+")
        #self.outFileName=f
        
        '''
        if sys.version_info[0] == 2:
            print >> f, 'FN_FDS=', self.FN_FDS
            print >> f, 'FN_EVAC=', self.FN_EVAC #,'\n'
        else:
            f.write('FN_FDS='+str(self.FN_FDS)+'\n')
            f.write('FN_EVAC='+str(self.FN_EVAC)+'\n')
            f.write('Working path='+os.getcwd()+'\n')
            f.write('ZOOM='+str(self.ZOOMFACTOR)+'\n')    	
            f.write('xSpace='+str(self.xSpace)+'\n')
            f.write('ySpace='+str(self.ySpace)+'\n')
            f.write('solver='+str(self.solver)+'\n')
            #f.write('group=')
            f.write(time.strftime('%Y-%m-%d_%H_%M_%S')+'\n\n')
        '''
        
        f.write('FN_FDS='+str(self.FN_FDS)+'\n')
        f.write('FN_EVAC='+str(self.FN_EVAC)+'\n')
        f.write('Working path='+os.getcwd()+'\n')
        #f.write('ZOOM='+str(self.ZOOMFACTOR)+'\n')    	
        #f.write('xSpace='+str(self.xSpace)+'\n')
        #f.write('ySpace='+str(self.ySpace)+'\n')
        #f.write('solver='+str(self.solver)+'\n')
        #f.write('group=')
        f.write(time.strftime('%Y-%m-%d_%H_%M_%S')+'\n\n')
        
        f.close()
        
        #FN_FDS=self.FN_FDS
        #FN_EVAC=self.FN_EVAC

        ###  Read in Data from .CSV File ###
        self.agents = readAgents(FN_EVAC)
        self.num_agents = len(self.agents)

        # Prviously exits are only specified in csv file.
        # In version 2.2 exits are alternatively read from fds input file.  
        #self.exits = readExits(FN_EVAC)
        #self.num_exits = len(self.exits)
        
        # Here we give the default values of zmin and zmax
        # These values are used if no specific values are input in tab Parameters in GUI
        if self.zmin is None:
            self.zmin=0.0
        if self.zmax is None:
            self.zmax=3.0
            
        if FN_FDS!="" and FN_FDS!="None" and FN_FDS is not None:
            self.walls = readOBST(FN_FDS, '&OBST', self.zmin, self.zmax, 'fromFDS.csv')
            self.doors = readPATH(FN_FDS, '&HOLE', self.zmin, self.zmax, 'fromFDS.csv')
            #self.doors += readPATH(FN_FDS, '&DOOR', self.zmin, self.zmax, 'hole_fromFDS.csv')
            #self.doors += readPATH(FN_FDS, '&ENTRY', self.zmin, self.zmax, 'hole_fromFDS.csv')
            self.exits = readEXIT(FN_FDS, '&EXIT', self.zmin, self.zmax, 'fromFDS.csv')
            self.num_walls = len(self.walls)
            self.num_doors = len(self.doors)
            self.num_exits = len(self.exits)
            #self.CHID=readCHID(FN_FDS)
            #self.t_end = float(readTEnd(FN_FDS))
            #self.DT = float(readKeyOnce(FN_FDS, '&TIME', 'DT'))
            temp = readKeyOnce(FN_FDS, '&DUMP', 'DT_PART')
            tempTEND = readKeyOnce(FN_FDS, '&TIME', 'T_END')
            tempDT = readKeyOnce(FN_FDS, '&TIME', 'DT')
            if temp is not None and tempTEND is not None and tempDT is not None:
                self.DT = float(tempDT)
                self.DT_DumpData = float(temp)
                self.t_end = float(tempTEND)
                
        else:
            self.walls = readWalls(FN_EVAC)  #readWalls(FN_Walls) #readWalls("obstData2018.csv")
            self.doors = readDoors(FN_EVAC)
            self.exits = readExits(FN_EVAC)
            self.num_walls = len(self.walls)
            self.num_doors = len(self.doors)
            self.num_exits = len(self.exits)                
        
        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        if self.num_exits > 0: # Solver=1 or Solver=2 are only valid if exits are defined
            
            '''
            self.agent2exit = np.zeros((self.num_agents, self.num_exits)) 
            #==========Exit selection of each agent ===============
            ### This is not yet used in the door selection routine
            ###=== Probablity of Selecting an Exit ================
            tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&Ped2Exit')
            if len(tableFeatures)<=0:
                tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&Agent2Exit')
            if len(tableFeatures)<=0:
                tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&agent2exit')
            
            self.agent2exit = readFloatArray(tableFeatures, len(self.agents), len(self.exits))
    
            if np.shape(self.agent2exit)!= (self.num_agents, self.num_exits): 
                print('\nError on input data: exits or agent2exit \n')
                f.write('\nError on input data: exits or agent2exit \n')
                raw_input('Error on input data: exits or agent2exit!  Please check')
                self.inputDataCorrect = False
            '''

            if self.num_exits > 0:
                self.exit2door = np.zeros((self.num_exits, self.num_doors)) 
                # This is almost useless because users can add doors or exits in testGeom.  So the size of self.exit2door will be changed in testGeom.  
                ###=== Door Direction for Each Exit ========
                tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&Exit2Door')
                if len(tableFeatures)<=0:
                    tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&exit2door')
                self.exit2door = readFloatArray(tableFeatures, len(self.exits), len(self.doors))
                #exit2door = readCSV("Exit2Door2018.csv", "float")
                if np.shape(self.exit2door)!= (self.num_exits, self.num_doors): 
                    print('\nError on input data: exits or exit2door \n')
                    f.write('\nError on input data: exits or exit2door \n')
                    raw_input('Error on input data: exits or exit2door!  Please check')
                    self.inputDataCorrect = False
        else:
            self.solver = 0
            self.exit2door = None
            self.agent2exit = None
            print('\n No exits are defined in input data and solver=0: No egress flow field is calculated \n')
            f.write('\ No exits are defined in input data and solver=0: No egress flow field; No agent2exit; No exit2door \n')
        
        if self.inputDataCorrect:
            print("Input data format is correct!")
        else:
            print("Input data format is wrong! Please check and modify!")
            input("Please check")
        
        f.close()
        return None
        
        
    def readconfig(self):
        FN_Temp = self.FN_EVAC
        #if FN_Temp is None:
        #FN_Temp = os.path.join(self.fpath, "config.txt")
        if os.path.exists(FN_Temp):
            for line in open(FN_Temp, "r"):
                
                self.ZOOMFACTOR = float(findKey('&ZOOM', '&zoom', 'ZOOM'))
                
                if re.match('&ZOOM', line):
                    temp =  line.split('=')
                    self.ZOOMFACTOR = float(temp[1].rstrip('\n').rstrip(',').strip())
                elif re.match('&zoom', line):
                    temp =  line.split('=')
                    self.ZOOMFACTOR = float(temp[1].rstrip('\n').rstrip(',').strip())
                elif re.match('ZOOM', line):
                    temp =  line.split('=')
                    self.ZOOMFACTOR = float(temp[1].rstrip('\n').rstrip(',').strip())

                if re.match('&OFFSET_X', line):
                    temp =  line.split('=')
                    self.xSpace = float(temp[1].rstrip('\n').rstrip(',').strip())
                elif re.match('&offset_x', line):
                    temp =  line.split('=')
                    self.xSpace = float(temp[1].rstrip('\n').rstrip(',').strip())
                elif re.match('xSpace', line):
                    temp =  line.split('=')
                    self.xSpace = float(temp[1].rstrip('\n').rstrip(',').strip())

                if re.match('&OFFSET_Y', line):
                    temp =  line.split('=')
                    self.ySpace = float(temp[1].rstrip('\n').rstrip(',').strip())
                elif re.match('&offset_y', line):
                    temp =  line.split('=')
                    self.ySpace = float(temp[1].rstrip('\n').rstrip(',').strip())
                elif re.match('ySpace', line):
                    temp =  line.split('=')
                    self.ySpace = float(temp[1].rstrip('\n').rstrip(',').strip())   

                if re.match('&SOLVER', line):
                    temp =  line.split('=')
                    self.solver = int(temp[1].rstrip('\n').rstrip(',').strip()) 
                elif re.match('&solver', line):
                    temp =  line.split('=')
                    self.solver = int(temp[1].rstrip('\n').rstrip(',').strip()) 
                elif re.match('solver', line):
                    temp =  line.split('=')
                    self.solver = int(temp[1].rstrip('\n').rstrip(',').strip())   

                if re.match('&GROUPF', line):
                    temp =  line.split('=')
                    self.GROUPBEHAVIOR = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   
                elif re.match('&groupf', line):
                    temp =  line.split('=')
                    self.GROUPBEHAVIOR = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   
                elif re.match('groupbehavior', line):
                    temp =  line.split('=')
                    self.GROUPBEHAVIOR = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   

                if re.match('&OPINION', line):
                    temp =  line.split('=')
                    self.OPINIONMODEL = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   
                elif re.match('&opinion', line):
                    temp =  line.split('=')
                    self.OPINIONMODEL = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   

                #if re.match('pre-evac', line):
                #    temp =  line.split('=')
                #    self.TPREMODE = int(temp[1].strip())
                
                if re.match('&SELF_REP', line):
                    temp =  line.split('=')
                    self.SELFREPULSION = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   
                elif re.match('&self_rep', line):
                    temp =  line.split('=')
                    self.SELFREPULSION = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   
                elif re.match('self-repulsion', line):
                    temp =  line.split('=')
                    self.SELFREPULSION = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   

                if re.match('&DUMPBIN', line):
                    temp =  line.split('=')
                    self.dumpBin = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   
                elif re.match('&dumpbin', line):
                    temp =  line.split('=')
                    self.dumpBin = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   
                elif re.match('dumpBinary', line):
                    temp =  line.split('=')
                    self.dumpBin = bool(int(temp[1].rstrip('\n').rstrip(',').strip()))   
                
                # Time parameters
                if re.match('&DT', line):
                    temp =  line.split('=')
                    self.DT = float(temp[1].rstrip('\n').rstrip(',').strip())   
                elif re.match('&dt', line):
                    temp =  line.split('=')
                    self.DT = float(temp[1].rstrip('\n').rstrip(',').strip())   
                elif re.match('DT', line):
                    temp =  line.split('=')
                    self.DT = float(temp[1].rstrip('\n').rstrip(',').strip())   

                if re.match('&DT_DUMPBIN', line):
                    temp =  line.split('=')
                    self.DT_DumpData = float(temp[1].rstrip('\n').rstrip(',').strip()) 
                elif re.match('&dt_dumpbin', line):
                    temp =  line.split('=')
                    self.DT_DumpData = float(temp[1].rstrip('\n').rstrip(',').strip()) 
                elif re.match('DT_DumpData', line):
                    temp =  line.split('=')
                    self.DT_DumpData = float(temp[1].rstrip('\n').rstrip(',').strip())   
                    
                if re.match('&DT_LIST', line):
                    temp =  line.split('=')
                    self.DT_OtherList = float(temp[1].rstrip('\n').rstrip(',').strip())  
                elif re.match('&dt_list', line):
                    temp =  line.split('=')
                    self.DT_OtherList = float(temp[1].rstrip('\n').rstrip(',').strip())  
                elif re.match('DT_OtherList', line):
                    temp =  line.split('=')
                    self.DT_OtherList = float(temp[1].rstrip('\n').rstrip(',').strip())   

                if re.match('&DT_EXIT', line):
                    temp =  line.split('=')
                    self.DT_ChangeDoor = float(temp[1].rstrip('\n').rstrip(',').strip())  
                elif re.match('&dt_exit', line):
                    temp =  line.split('=')
                    self.DT_ChangeDoor = float(temp[1].rstrip('\n').rstrip(',').strip())  
                elif re.match('DT_ChangeDoor', line):
                    temp =  line.split('=')
                    self.DT_ChangeDoor = float(temp[1].rstrip('\n').rstrip(',').strip())   

                if re.match('&TEND', line):
                    temp =  line.split('=')
                    try:
                        self.t_end = float(temp[1].rstrip('\n').rstrip(',').strip())   
                    except:
                        self.t_end = float('inf')
                elif re.match('&tend', line):
                    temp =  line.split('=')
                    try:
                        self.t_end = float(temp[1].rstrip('\n').rstrip(',').strip())   
                    except:
                        self.t_end = float('inf')
                elif re.match('TEND', line):
                    temp =  line.split('=')
                    try:
                        self.t_end = float(temp[1].rstrip('\n').rstrip(',').strip())   
                    except:
                        self.t_end = float('inf')
                
                # Mesh parameters
                if re.match('&xmin', line):
                    temp =  line.split('=')
                    self.xmin = int(temp[1].rstrip('\n').rstrip(',').strip())   
                elif re.match('xmin', line):
                    temp =  line.split('=')
                    self.xmin = int(temp[1].rstrip('\n').rstrip(',').strip())  
                     
                if re.match('&xmax', line):
                    temp =  line.split('=')
                    self.xmax = int(temp[1].rstrip('\n').rstrip(',').strip())   
                elif re.match('xmax', line):
                    temp =  line.split('=')
                    self.xmax = int(temp[1].rstrip('\n').rstrip(',').strip())   

                if re.match('&ymin', line):
                    temp =  line.split('=')
                    self.ymin = int(temp[1].rstrip('\n').rstrip(',').strip())   
                elif re.match('ymin', line):
                    temp =  line.split('=')
                    self.ymin = int(temp[1].rstrip('\n').rstrip(',').strip())   

                if re.match('&ymax', line):
                    temp =  line.split('=')
                    self.ymax = int(temp[1].rstrip('\n').rstrip(',').strip())  
                elif re.match('ymax', line):
                    temp =  line.split('=')
                    self.ymax = int(temp[1].rstrip('\n').rstrip(',').strip())   
                    
                if re.match('&xpt', line):
                    temp =  line.split('=')
                    self.xpt = int(temp[1].rstrip('\n').rstrip(',').strip())   
                elif re.match('xpt', line):
                    temp =  line.split('=')
                    self.xpt = int(temp[1].rstrip('\n').rstrip(',').strip())   

                if re.match('&ypt', line):
                    temp =  line.split('=')
                    self.ypt = int(temp[1].rstrip('\n').rstrip(',').strip())   
                elif re.match('ypt', line):
                    temp =  line.split('=')
                    self.ypt = int(temp[1].rstrip('\n').rstrip(',').strip())   

        return None
        
        
    def dataSummary(self):

        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        
        tempNum=0
        for agent in self.agents:
            if agent.inComp:
                tempNum=tempNum+1
        self.inComp_agents=tempNum

        tempNum=0
        for wall in self.walls:
            if wall.inComp:
                tempNum=tempNum+1
        self.inComp_walls=tempNum

        tempNum=0
        for door in self.doors:
            if door.inComp:
                tempNum=tempNum+1
        self.inComp_doors=tempNum

        tempNum=0
        for exit in self.exits:
            if exit.inComp:
                tempNum=tempNum+1
        self.inComp_exits=tempNum
        
        ### Display a summary of input data
        print('Display a summary of input data as below.\n')
        print('number of agents in input file: '+str(self.num_agents)) #+ '\n')
        print('number of wall in input files: '+str(self.num_walls)) #+ '\n')
        print('number of doors in input file: '+str(self.num_doors)) #+ '\n')
        print('number of exits in input file: '+str(self.num_exits)) #+ '\n')
        print('\n')

        print('Display a summary of data in computation as below.\n')
        print('number of agents in computation: '+str(self.inComp_agents)) #+ '\n')
        print('number of walls in computation: '+str(self.inComp_walls)) #+ '\n')
        print('number of doors in computation: '+str(self.inComp_doors)) #+ '\n')
        print('number of exits in computation: '+str(self.inComp_exits)) #+ '\n')
        print('\n')

        print('mesh paramters:')  
        print('x-range:'+str(self.xmin)+' to '+str(self.xmax))
        print('number of x points:'+str(self.xpt))
        print('y-range:'+str(self.ymin)+' to '+str(self.ymax))
        print('number of y points:'+str(self.ypt)+ '\n')

        print('exit2door:'+'\n'+str(self.exit2door)+'\n')
        print('person exit_prob:'+'\n'+str(person.exit_prob)+ '\n')
        print('person exit_known:'+'\n'+str(person.exit_known)+ '\n')

        print('time-related paramters:') #\n')        
        print('DT = '+str(self.DT)) #+ '\n')
        print('DT_DumpData = '+str(self.DT_DumpData)) #+'\n')
        print('t_end = '+str(self.t_end)+ '\n')
        print('DT_OtherList ='+str(self.DT_OtherList)) #+ '\n')
        print('DT_ChangeDoor ='+str(self.DT_ChangeDoor)) #+ '\n')
        
        print('\n')
        
        print('simulation paramters=') # \n')     
        print('Solver= '+str(self.solver)) #+ '\n')   
        #print('TPRE Mode: '+str(self.TPREMODE)) #+ '\n')
        print('Group = '+str(self.GROUPBEHAVIOR)) #+ '\n')
        print('Self Repulsion = '+str(self.SELFREPULSION)) #+ '\n')
        if self.OPINIONMODEL==0:
            print('Opinion Model = '+str('0: Linear or Nonlinear System')) #+ '\n')
        if self.OPINIONMODEL==1:
            print('Opinion Model = '+str('1: Random Gossip'))
        print('Short-Range Force = '+str(self.INTERACTION)) #+ '\n')
        print('Dump Binary Data = '+str(self.dumpBin)) #+ '\n')
        print('Working Folder = '+str(self.fpath)) #+ '\n')

        print('\n')
        
        updateAgentData(self.agents, FN_Temp)
        updateWallData(self.walls, FN_Temp)
        updateDoorData(self.doors, FN_Temp)
        updateExitData(self.exits, FN_Temp)

        f.write('\n')
        f.write('Display a summary of input data as below.\n')
        f.write('number of agents in input file: '+str(self.num_agents)+ '\n')
        f.write('number of walls in input file: '+str(self.num_walls)+ '\n')
        f.write('number of doors in input file: '+str(self.num_doors)+ '\n')
        f.write('number of exits in input file: '+str(self.num_exits)+ '\n')
        f.write('\n')

        f.write('Display a summary of data in computation as below.\n')
        f.write('number of agents in computation: '+str(self.inComp_agents)+ '\n')
        f.write('number of walls in computation: '+str(self.inComp_walls)+ '\n')
        f.write('number of doors in computation: '+str(self.inComp_doors)+ '\n')
        f.write('number of exits in computation: '+str(self.inComp_exits)+ '\n')
        f.write('\n')

        f.write('exit2door:'+str(self.exit2door))
        f.write('person exit_prob:'+str(person.exit_prob)+ '\n')
        f.write('person exit_known:'+str(person.exit_known)+ '\n')
        f.write('\n')

        f.write('time-related paramters: \n')        
        f.write('DT = '+str(self.DT)+ '\n')
        f.write('DT_DumpData = '+str(self.DT_DumpData)+ '\n')
        f.write('t_end = '+str(self.t_end)+ '\n')
        f.write('DT_OtherList ='+str(self.DT_OtherList)+ '\n')
        f.write('DT_ChangeDoor ='+str(self.DT_ChangeDoor)+ '\n\n')

        f.write('simulation paramters:\n')   
        f.write('solver = '+str(self.solver)+ '\n')        
        #f.write('TPRE Mode: '+str(self.TPREMODE)+'\n')
        f.write('Group = '+str(self.GROUPBEHAVIOR)+'\n')
        f.write('Self Repulsion = '+str(self.SELFREPULSION)+'\n')
        
        if self.OPINIONMODEL==0:
            #print('Opinion Model = '+str('Linear or Nonlinear System')) #+ '\n')\
            f.write('Opinion Model = '+str('0: Linear or Nonlinear System')+'\n')
        if self.OPINIONMODEL==1:
            #print('Opinion Model = '+str('Random Gossip'))
            f.write('Opinion Model = '+str('1: Random Gossip')+'\n')
        f.write('Short-Range Force = '+str(self.INTERACTION)+ '\n')
        f.write('Dump Binary Data = '+str(self.dumpBin)+'\n')
        f.write('Working Folder = '+str(self.fpath)+ '\n')
        
        f.close()

        if self.inputDataCorrect:
            print("Input data format is correct!")
        else:
            print("Input data format is wrong! Please check and modify!")
            
        if self.DEBUG:
            print("Now you can check if the input data is correct or not!")
            print("If everything is OK, please press ENTER to continue!")
            if sys.version_info[0] == 2: 
                raw_input('Please check input data here!')
                #UserInput = raw_input('Check Input Data Here!')
            if sys.version_info[0] == 3:
                input('Please check input data here!')

        return self.inputDataCorrect
        # Return a boolean variable to check if the input data format is correct or not

    def buildMesh(self, showdata=False):
        
        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        if self.solver==0:
            print("The solver is 0, and it may not need the flow field.  Please check!")

        xxx=[]
        yyy=[]
        for wall in self.walls:
            if wall.inComp is 0:
                continue
            xxx.append(wall.params[0])
            xxx.append(wall.params[2])
            yyy.append(wall.params[1])
            yyy.append(wall.params[3])      

        for door in self.doors:
            if door.inComp is 0:
                continue
            xxx.append(door.params[0])
            xxx.append(door.params[2])
            yyy.append(door.params[1])
            yyy.append(door.params[3])

        for exit in self.exits:
            if exit.inComp is 0:
                continue
            xxx.append(exit.params[0])
            xxx.append(exit.params[2])
            yyy.append(exit.params[1])
            yyy.append(exit.params[3])

        for agent in self.agents:
            if agent.inComp is 0:
                continue
            xxx.append(agent.pos[0])
            yyy.append(agent.pos[1])
        
        # Here we give the values of xmin xmax ymin ymax xpt ypt by using automatic method
        # These values are used if no specific values are input in tab Egressflow in GUI
        if self.xmin is None:
            self.xmin=np.min(xxx)
        if self.xmax is None:
            self.xmax=np.max(xxx)
        if self.ymin is None:
            self.ymin=np.min(yyy)
        if self.ymax is None:
            self.ymax=np.max(yyy)
        
        if self.xpt is None:
            self.xpt=int(self.xmax-self.xmin)*2+20
        if self.ypt is None:
            self.ypt=int(self.ymax-self.ymin)*2+20

        if self.DEBUG:
            print("Range in x axis:", self.xmin, self.xmax, "Num of points in x axis:", self.xpt)
            print("Range in y axis:", self.ymin, self.ymax, "Num of points in y axis:", self.ypt)

        self.dx = (self.xmax-self.xmin)/float(self.xpt - 1)
        self.dy = (self.ymax-self.ymin)/float(self.ypt - 1)
        
        x_min=self.xmin
        y_min=self.ymin
        x_max=self.xmax
        y_max=self.ymax
        x_points=self.xpt
        y_points=self.ypt

        '''
        f.write('\n\n\n')
        f.write('x_points:'+str(x_points)+ '\n')
        f.write('y_points:'+str(y_points)+ '\n')
        f.write('x_min:'+str(x_min)+ '\n')
        f.write('x_max:'+str(x_max)+ '\n')
        f.write('y_min:'+str(y_min)+ '\n')
        f.write('y_max:'+str(y_max)+ '\n')
        
        f.write('delx:'+str(self.dx)+ '\n')
        f.write('dely:'+str(self.dy)+ '\n')
        '''
        
        #f.write('delt:'+str(self.DT)+ '\n')
        #f.write('courant number index???:'+str(self.DT/(self.dx+self.dy))+ '\n')
        
        BLDinfo = build_compartment(x_min, y_min, x_max, y_max, x_points, y_points, self.walls, self.doors, self.exits)
        
        self.bldmesh = BLDinfo
        f.close()


    def flowMesh(self, showdata=False, savedata=True):

        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        #mode=1 nearest exit strategy
        #mode=2 each exit is individually calculated
        if self.solver==0:
            print("The solver is 0, and it may not need the flow field.  Please check!")
        
        '''
        xxx=[]
        yyy=[]
        for wall in self.walls:
            if wall.inComp is 0:
                continue
            xxx.append(wall.params[0])
            xxx.append(wall.params[2])
            yyy.append(wall.params[1])
            yyy.append(wall.params[3])      

        for door in self.doors:
            if door.inComp is 0:
                continue
            xxx.append(door.params[0])
            xxx.append(door.params[2])
            yyy.append(door.params[1])
            yyy.append(door.params[3])

        for exit in self.exits:
            if exit.inComp is 0:
                continue
            xxx.append(exit.params[0])
            xxx.append(exit.params[2])
            yyy.append(exit.params[1])
            yyy.append(exit.params[3])

        for agent in self.agents:
            if agent.inComp is 0:
                continue
            xxx.append(agent.pos[0])
            yyy.append(agent.pos[1])


        self.xmin=np.min(xxx)
        self.xmax=np.max(xxx)
        self.ymin=np.min(yyy)
        self.ymax=np.max(yyy)
        
        if self.xpt is None:
            self.xpt=int(self.xmax-self.xmin)*3+3
        if self.ypt is None:
            self.ypt=int(self.ymax-self.ymin)*3+3

        if self.DEBUG:
            print("Range in x axis:", self.xmin, self.xmax, "Num of points in x axis:", self.xpt)
            print("Range in y axis:", self.ymin, self.ymax, "Num of points in y axis:", self.ypt)

        self.dx = (self.xmax-self.xmin)/float(self.xpt - 1)
        self.dy = (self.ymax-self.ymin)/float(self.ypt - 1)
        
        '''
        
        x_min=self.xmin
        y_min=self.ymin
        x_max=self.xmax
        y_max=self.ymax
        x_points=self.xpt
        y_points=self.ypt
        BLDinfo = self.bldmesh

        '''
        f.write('x_points:'+str(x_points)+ '\n')
        f.write('y_points:'+str(y_points)+ '\n')
        f.write('x_min:'+str(x_min)+ '\n')
        f.write('x_max:'+str(x_max)+ '\n')
        f.write('y_min:'+str(y_min)+ '\n')
        f.write('y_max:'+str(y_max)+ '\n')
        
        BLDinfo = build_compartment(x_min, y_min, x_max, y_max, x_points, y_points, self.walls, self.doors, self.exits)
        '''

        #Show flow field of all exit: The nearest exit strategy
        if self.solver==1:
            
            tempdir=os.path.join(self.fpath, "vel_flow1.npz")
            #if self.DEBUG:
            #    print(tempdir)
            #    if sys.version_info[0] == 2: 
            #        raw_input('Please check input data here!')
            #    if sys.version_info[0] == 3:
            #        input('Please check input data here!')
            if os.path.exists(tempdir):
                vel_flow2_data=np.load(tempdir)
                Ud0 = vel_flow2_data["arr_0"]
                Vd0 = vel_flow2_data["arr_1"]
                BLDread = vel_flow2_data["arr_5"]
                computeFlowFlag=False
                
                #print('BLDread:', BLDread)
                #print('BLDinfo:', BLDinfo)
                if np.shape(BLDread) != np.shape(BLDinfo): #len(UU) != self.num_exits or len(VV) != self.num_exits
                    if sys.version_info[0] == 2:
                        raw_input('\nWarning: egress flow field changed. \n Recalculate.  Please check!')
                    if sys.version_info[0] == 3:
                        input('\nWarning: egress flow field changed. \n Recalculate.  Please check!')
                    computeFlowFlag=True
                    
                elif (BLDread - BLDinfo).any():
                    if sys.version_info[0] == 2:
                        raw_input('\nWarning: egress flow field changed. \n Recalculate.  Please check!')
                    if sys.version_info[0] == 3:
                        input('\nWarning: egress flow field changed. \n Recalculate.  Please check!')
                    computeFlowFlag=True
            else:
                computeFlowFlag=True

            if computeFlowFlag:
                b = build_sink(x_min, y_min, x_max, y_max, x_points, y_points, self.exits)
                iterNum = int(x_points + y_points)
                Ud0, Vd0 = possion_func(x_min, y_min, x_max, y_max, x_points, y_points, b, BLDinfo, iterNum, True)
                if showdata:
                    draw_vel(x_min, y_min, x_max, y_max, Ud0, Vd0, BLDinfo, self.walls, self.doors, self.exits, self.ZOOMFACTOR)
                    print('\n')
                    print('Iteration Number:', iterNum)
                    print('x_points:', x_points)
                    print('y_points:', y_points, '\n')
                    print('x_min:', x_min)
                    print('x_max:', x_max)
                    print('y_min:', y_min)
                    print('y_max:', y_max, '\n')
                    f.write('Iteration Number:'+ str(iterNum))
    
                # Test of Eular Solver here
                zeroArray = np.zeros(np.shape(Ud0))
                D_t= self.DT #0.05
                tend=self.t_end
                R_ini = np.zeros(np.shape(Ud0))
                # Construct R_ini here!
                for agent in self.agents:
                    if agent.inComp == 0:
                        continue
                    #iii=int((door.pos[0]-self.xmin)/self.dx)
                    #jjj=int((door.pos[1]-self.ymin)/self.dy)
                    
                    iii=int((agent.pos[0]-self.xmin)/self.dx)
                    jjj=int((agent.pos[1]-self.ymin)/self.dy)
                    R_ini[iii,jjj]=0.5
    
                print('R_ini:\n',R_ini)
                print('np.sum(R_ini):',np.sum(R_ini))
                #eular2D(x_min, y_min, x_max, y_max, x_points, y_points, D_t, tend, bldInfo, R0, U0, V0, Rdes, Udes, Vdes, mode=0, saveData=True, showPlot=True, debug=True):
                exitpoints=build_exitpt(x_min, y_min, x_max, y_max, x_points, y_points, self.exits)
                RRt, UUt, VVt = lwr2D(x_min, y_min, x_max, y_max, x_points, y_points, tend, self.bldmesh, R0=R_ini, U0=zeroArray, V0=zeroArray, Rdes=zeroArray, Udes=Ud0, Vdes=Vd0, exitpt=exitpoints, mode=6, debug=False)
                ##saveData=False, showPlot=False
                if savedata:
                    np.savez(os.path.join(self.fpath, "vel_flow1.npz"), Ud0, Vd0, RRt, UUt, VVt, BLDinfo, [x_min, y_min, x_max, y_max, x_points,y_points])
              
                
        if self.solver==2: # Show flow field of each individual exit
            tempdir=os.path.join(self.fpath, "vel_flow2.npz")
            #tempdir=self.fpath+"/vel_flow2.npz"
            print(tempdir)
            #if self.DEBUG:
            #    if sys.version_info[0] == 2: 
            #        raw_input('Please check input data here!')
            #    if sys.version_info[0] == 3:
            #        input('Please check input data here!')
            if os.path.exists(tempdir):
                vel_flow2_data=np.load(tempdir)
                Ud0 = vel_flow2_data["arr_0"]
                Vd0 = vel_flow2_data["arr_1"]
                UU = vel_flow2_data["arr_2"]
                VV = vel_flow2_data["arr_3"]
                BLDread = vel_flow2_data["arr_4"]
                print('Length of UU or VV (Should be equal to number of exits):', len(UU), len(VV))
                computeFlowFlag=False
                
                #print('BLDread:', BLDread)
                #print('BLDinfo:', BLDinfo)
                if len(UU) != self.num_exits or len(VV) != self.num_exits or np.shape(BLDread) != np.shape(BLDinfo):
                    if sys.version_info[0] == 2:
                        raw_input('\nWarning: egress flow field changed. \n Recalculate.  Please check!')
                    if sys.version_info[0] == 3:
                        input('\nWarning: egress flow field changed. \n Recalculate.  Please check!')
                    computeFlowFlag=True
                    
                elif (BLDread - BLDinfo).any():
                    if sys.version_info[0] == 2:
                        raw_input('\nWarning: egress flow field changed. \n Recalculate.  Please check!')
                    if sys.version_info[0] == 3:
                        input('\nWarning: egress flow field changed. \n Recalculate.  Please check!')
                    computeFlowFlag=True
            else:
                computeFlowFlag=True

            if computeFlowFlag:
                UU=[]
                VV=[]
                b = build_sink(x_min, y_min, x_max, y_max, x_points, y_points, self.exits)
                iterNum = int(x_points + y_points)
                Ud0, Vd0 = possion_func(x_min, y_min, x_max, y_max, x_points, y_points, b, BLDinfo, iterNum, True)
                if showdata:
                    draw_vel(x_min, y_min, x_max, y_max, Ud0, Vd0, BLDinfo, self.walls, self.doors, self.exits, self.ZOOMFACTOR)

                #for exit in self.exits:
                for idexit, exit in enumerate(self.exits):
                    b = build_single_sink(x_min, y_min, x_max, y_max, x_points, y_points, exit)
                    iterNum = int(x_points + y_points)
                    Ud, Vd = possion_func(x_min, y_min, x_max, y_max, x_points, y_points, b, BLDinfo, iterNum, True)
                    #if self.DEBUG:
                    UU.append(Ud)
                    VV.append(Vd)
                    if showdata:
                        draw_vel(x_min, y_min, x_max, y_max, Ud, Vd, BLDinfo, self.walls, self.doors, self.exits, self.ZOOMFACTOR)
                        print('\n')
                        print('Iteration Number:', iterNum)
                        print('x_points:', x_points, '\n')
                        print('y_points:', y_points, '\n')
                        print('x_min:', x_min, '\n')
                        print('x_max:', x_max, '\n')
                        print('y_min:', y_min, '\n')
                        print('y_max:', y_max, '\n')
                        f.write('exit'+str(idexit)+':Iteration Number:'+ str(iterNum))

                if savedata:
                    np.savez(os.path.join(self.fpath, "vel_flow2.npz"), Ud0, Vd0, UU, VV, BLDinfo, [x_min, y_min, x_max, y_max, x_points,y_points], b)
                    #np.savez(os.path.join(self.fpath, "vel_flow2.npz"), UU, VV)
    
        if self.solver==1:
            self.UallExit=Ud0
            self.VallExit=Vd0
            
        if self.solver==2:
            self.UallExit=Ud0
            self.VallExit=Vd0
            self.UeachExit=UU
            self.VeachExit=VV

        f.close()
        
    ##############################################################################
    # Automatically generate door direction and exit2door matrix based on flow mesh result
    def computeDoorDirection(self, showdata=False, savedata=False):

        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        #solver=1 nearest exit strategy
        #solver=2 each exit is individually calculated
        if self.solver==0:
            print("The solver is 0, and it may not need the flow field.  Please check!")

        if self.DEBUG:
            f.write("\n========================================\n")
            f.write("===Compute Door Direction by Flow Field==="+'\n')
            f.write("==========================================\n")
            
        self.num_agents= len(self.agents)
        self.num_walls = len(self.walls)
        self.num_doors = len(self.doors)
        self.num_exits = len(self.exits)
        self.exit2door = np.zeros((self.num_exits, self.num_doors))
        
        ###=== Door Direction for Each Exit ========
        if self.solver==1: # Use Nearest Exit

            '''
            tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&Exit2Door')
            self.exit2door = readFloatArray(tableFeatures, len(self.exits), len(self.doors))

            if np.shape(self.exit2door)!= (self.num_exits, self.num_doors): 
                print('\nError on input data: exits or exit2door \n')
                #f.write('\nError on input data: exits or exit2door \n')
                #raw_input('Error on input data: exits or exit2door!  Please check')
                self.inputDataCorrect = False
            '''
            
            Utemp = self.UallExit[1:-1, 1:-1]
            Vtemp = self.VallExit[1:-1, 1:-1]
            for iddoor, door in enumerate(self.doors):
                if door.inComp == 0:
                    continue
                
                ipos=int((door.pos[0]-self.xmin)/self.dx)
                jpos=int((door.pos[1]-self.ymin)/self.dy)

                ifloor=int(floor((door.params[0]-self.xmin)/self.dx))
                jfloor=int(floor((door.params[1]-self.ymin)/self.dy))

                iceil=int(ceil((door.params[2]-self.xmin)/self.dx))
                jceil=int(ceil((door.params[3]-self.ymin)/self.dy))

                print('iii', ipos, 'jjj', jpos)
                print('floor and ceil check:', ifloor, iceil, jfloor, jceil)
                f.write('floor and ceil check:'+str([ifloor, iceil, jfloor, jceil])+'\n')

                Usum=0.0 #np.array([0.0, 0.0])
                Vsum=0.0 #np.array([0.0, 0.0])
                #for iii in range(ifloor, iceil+1):
                #    for jjj in range(jfloor, jceil+1):
                        #Usum += Utemp[iii, jjj]
                        #Vsum += Vtemp[iii, jjj]
                for iii in range(ipos-1, ipos+2):
                    for jjj in range(jpos-1, jpos+2):
                        vec=np.array([Utemp[iii, jjj],Vtemp[iii, jjj]])
                        vec=normalize(vec)
                        Usum += vec[0]
                        Vsum += vec[1]

                if Usum>=Vsum and Usum>=-Vsum:
                    door.arrow=1
                if Usum>=Vsum and Usum<-Vsum:
                    door.arrow=-2
                if Usum<Vsum and Usum>=-Vsum:
                    door.arrow=2
                if Usum<Vsum and Usum<-Vsum:
                    door.arrow=-1
                
                if self.DEBUG:
                    print('Nearest Exit Egress Field:')
                    print('door.oid:', door.oid, '\t', Usum, Vsum, '\t door.arrow:', door.arrow, '\n')
                    #f.write('Nearest Exit Egress Field:')
                    f.write('door.oid:'+str(door.oid)+str([Usum,Vsum])+'\t door.arrow:'+str(door.arrow)+'\n')
                    #input('Debug for door direction in egress flow field.  Please check!')
                
                if len(door.attachedWalls)>0:
                    r1, r2, r3, r4 = door.dirWithAttachedWalls(mode='average')
                    if r1 is None and r3 is None:
                        if Usum>0:
                            door.arrow=1
                        else:
                            #self.exit2door[idexit, iddoor]=-1
                            door.arrow=-1
                    if r2 is None and r4 is None:
                        if Vsum>0:
                            door.arrow=2
                        else:
                            door.arrow=-2
                if self.DEBUG:
                    print('door.oid:', door.oid, '\t', Usum, Vsum, '\t door.arrow:', door.arrow, '\n')
                    f.write('door.oid:'+str(door.oid)+ '\t door.arrow rechecked based on attached walls:'+str(door.arrow)+'\n')
                    #input('Door direction rechecked based on  attached walls!')


        if self.solver == 2:

            Utemp = self.UallExit[1:-1, 1:-1]
            Vtemp = self.VallExit[1:-1, 1:-1]
            for iddoor, door in enumerate(self.doors):
                if door.inComp == 0:
                    continue

                ipos=int((door.pos[0]-self.xmin)/self.dx)
                jpos=int((door.pos[1]-self.ymin)/self.dy)

                ifloor=int(floor((door.params[0]-self.xmin)/self.dx))
                jfloor=int(floor((door.params[1]-self.ymin)/self.dy))

                iceil=int(ceil((door.params[2]-self.xmin)/self.dx))
                jceil=int(ceil((door.params[3]-self.ymin)/self.dy))

                print('ipos', ipos, 'jpos', jpos)
                print('floor and ceil check:', ifloor, iceil, jfloor, jceil)
                f.write('floor and ceil check:'+str([ifloor, iceil, jfloor, jceil])+'\n')

                Usum=0.0 #np.array([0.0, 0.0])
                Vsum=0.0 #np.array([0.0, 0.0])
                for iii in range(ipos-1, ipos+2):
                    for jjj in range(jpos-1, jpos+2):
                        vec=np.array([Utemp[iii, jjj],Vtemp[iii, jjj]])
                        vec=normalize(vec)
                        Usum += vec[0]
                        Vsum += vec[1]
                #for iii in range(ifloor, iceil+1):
                #    for jjj in range(jfloor, jceil+1):
                        #Usum += Utemp[iii, jjj]
                        #Vsum += Vtemp[iii, jjj]

                if Usum>=Vsum and Usum>=-Vsum:
                    door.arrow=1
                if Usum>=Vsum and Usum<-Vsum:
                    door.arrow=-2
                if Usum<Vsum and Usum>=-Vsum:
                    door.arrow=2
                if Usum<Vsum and Usum<-Vsum:
                    door.arrow=-1
                
                if self.DEBUG:
                    print('Nearest Exit Egress Field:')
                    print('door.oid:', door.oid, '\t', Usum, Vsum, '\t door.arrow:', door.arrow, '\n')
                    #f.write('Nearest Exit Egress Field:')
                    f.write('door.oid:'+str(door.oid)+str([Usum,Vsum])+'\t door.arrow:'+str(door.arrow)+'\n')
                    #input('Debug for door direction in egress flow field.  Please check!')

                # Simple Revision
                '''
                if len(door.attachedWalls)==1:
                    wallTemp = door.attachedWalls[0]
                    xlen = abs(wallTemp.params[0]-wallTemp.params[2])
                    ylen = abs(wallTemp.params[1]-wallTemp.params[3])
                    if xlen>ylen:
                        if Vsum>0:
                            door.arrow=2
                        else:
                            door.arrow=-2
                    if xlen<ylen:
                        if Usum>0:
                            door.arrow=1
                        else:
                            #self.exit2door[idexit, iddoor]=-1
                            door.arrow=-1
                '''            
                
                if len(door.attachedWalls)>0:
                    r1, r2, r3, r4 = door.dirWithAttachedWalls(mode='average')
                    if r1 is None and r3 is None:
                        if Usum>0:
                            door.arrow=1
                        else:
                            #self.exit2door[idexit, iddoor]=-1
                            door.arrow=-1
                    if r2 is None and r4 is None:
                        if Vsum>0:
                            door.arrow=2
                        else:
                            door.arrow=-2
                #print('door.oid:', door.oid, 'door.arrow:', door.arrow, '\t')
                if self.DEBUG:
                    print('door.oid:', door.oid, '\t', Usum, Vsum, '\t door.arrow:', door.arrow, '\n')
                    f.write('door.oid:'+str(door.oid)+ '\t door.arrow rechecked based on attached walls:'+str(door.arrow)+'\n')
                    #input('Door direction rechecked based on  attached walls!')
                
            for idexit, exit in enumerate(self.exits):
                Utemp = self.UeachExit[idexit][1:-1, 1:-1]
                Vtemp = self.VeachExit[idexit][1:-1, 1:-1]
                for iddoor, door in enumerate(self.doors):
                    if door.inComp == 0:
                        continue
                    ipos=int((door.pos[0]-self.xmin)/self.dx)
                    jpos=int((door.pos[1]-self.ymin)/self.dy)

                    ifloor=int(floor((door.params[0]-self.xmin)/self.dx))
                    jfloor=int(floor((door.params[1]-self.ymin)/self.dy))

                    iceil=int(ceil((door.params[2]-self.xmin)/self.dx))
                    jceil=int(ceil((door.params[3]-self.ymin)/self.dy))

                    print('iii', ipos, 'jjj', jpos)
                    print('floor and ceil check:', ifloor, iceil, jfloor, jceil)

                    Usum=0.0 #np.array([0.0, 0.0])
                    Vsum=0.0 #np.array([0.0, 0.0])
                    #for iii in range(ifloor, iceil+1):
                    #    for jjj in range(jfloor, jceil+1):
                            #Usum += Utemp[iii, jjj]
                            #Vsum += Vtemp[iii, jjj]
                            
                    for iii in range(ipos-1, ipos+2):
                        for jjj in range(jpos-1, jpos+2):
                            vec=np.array([Utemp[iii, jjj],Vtemp[iii, jjj]])
                            vec=normalize(vec)
                            Usum += vec[0]
                            Vsum += vec[1]


                    if Usum>=Vsum and Usum>=-Vsum:
                        self.exit2door[idexit, iddoor]=1
                        # if door.attachedWalls
                    if Usum>=Vsum and Usum<-Vsum:
                        self.exit2door[idexit, iddoor]=-2
                    if Usum<Vsum and Usum>=-Vsum:
                        self.exit2door[idexit, iddoor]=2
                    if Usum<Vsum and Usum<-Vsum:
                        self.exit2door[idexit, iddoor]=-1

                    if self.DEBUG:
                        print('door.oid:', door.oid, '\t', Usum, Vsum, '\t exit2door:', self.exit2door[idexit, iddoor], '\n')
                        f.write('door.oid:'+str(door.oid)+str([Usum,Vsum])+'\t exit2door:'+str(self.exit2door[idexit, iddoor])+'\n')
                        #input('Debug for door direction in egress flow field.  Please check!')

                    '''
                    # Simple Revision
                    if len(door.attachedWalls)==1:
                        wallTemp = door.attachedWalls[0]
                        xlen = abs(wallTemp.params[0]-wallTemp.params[2])
                        ylen = abs(wallTemp.params[1]-wallTemp.params[3])
                        if xlen>ylen:
                            if Vsum>0:
                                self.exit2door[idexit, iddoor]=2
                            else:
                                self.exit2door[idexit, iddoor]=-2
                        if xlen<ylen:
                            if Usum>0:
                                self.exit2door[idexit, iddoor]=1
                            else:
                                self.exit2door[idexit, iddoor]=-1
                    '''

                    if len(door.attachedWalls)>0:
                        r1, r2, r3, r4 = door.dirWithAttachedWalls(mode='average')
                        if r1 is None and r3 is None:
                            if Usum>0:
                                self.exit2door[idexit, iddoor]=1
                            else:
                                self.exit2door[idexit, iddoor]=-1
                        if r2 is None and r4 is None:
                            if Vsum>0:
                                self.exit2door[idexit, iddoor]=2
                            else:
                                self.exit2door[idexit, iddoor]=-2


                    if self.DEBUG:
                        print('door.oid:', door.oid, '\t', Usum, Vsum, '\t exit2door:', self.exit2door[idexit, iddoor], '\n')
                        f.write('door.oid:'+str(door.oid)+ '\t exit2door rechecked based on attached walls:'+str(self.exit2door[idexit, iddoor])+'\n')
                        #input('Door direction recheck based on attachedw walls!')

                    '''
                    if Utemp[iii,jjj]>=Vtemp[iii,jjj] and Utemp[iii,jjj]>=-Vtemp[iii,jjj]:
                        self.exit2door[idexit, iddoor]=1
                    if Utemp[iii,jjj]>=Vtemp[iii,jjj] and Utemp[iii,jjj]<-Vtemp[iii,jjj]:
                        self.exit2door[idexit, iddoor]=-2
                    if Utemp[iii,jjj]<Vtemp[iii,jjj] and Utemp[iii,jjj]>=-Vtemp[iii,jjj]:
                        self.exit2door[idexit, iddoor]=2
                    if Utemp[iii,jjj]<Vtemp[iii,jjj] and Utemp[iii,jjj]<-Vtemp[iii,jjj]:
                        self.exit2door[idexit, iddoor]=-1
                    '''
                    
            print('exit2door:\n', self.exit2door, '\n')
            if self.DEBUG:
                f.write('exit2door:\n' + str(self.exit2door) + '\n\n')

        f.close()
            
    
    
    ##############################################################################
    # Find attached walls and doors and automatically adjust door params if needed
    def preprocessGeom(self):
        
        #===================================================
        #==========Preprocessing the Geom Data =====================
        #========= Find Relationship of Door and Wall ==================

        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        if self.DEBUG:
            f.write("\n========================================\n")
            f.write("Preprocessing the Geom Data"+'\n')
            f.write("=========================================\n")
            
        self.num_agents= len(self.agents)
        self.num_walls = len(self.walls)
        self.num_doors = len(self.doors)
        self.num_exits = len(self.exits)
        
        '''
        if self.num_exits>0 and self.num_doors>0:
            self.exit2door = np.zeros((self.num_exits, self.num_doors))
        else:
            self.exit2door = None
        '''
        if self.exit2door is not None:
            self.exit2door = self.exit2door[0:self.num_exits, 0:self.num_doors]
        
        if self.num_exits>0:
            self.exitUsage = np.zeros((self.num_exits, 1)) # To count number of agents selecting each exit
   
        for wall in self.walls:
            wall.findAttachedDoors(self.doors+self.exits)
            print("wall Name:", wall.name, 'isSingle:', wall.isSingleWall)
            if self.DEBUG:
                f.write("wall Name:" + str(wall.name) + 'isSingle:' + str(wall.isSingleWall)+'\n')
            for door in wall.attachedDoors:
                print("attached door name. :", door.name)
                if self.DEBUG:
                    f.write("attached door name. :" + str(door.name)+'\n')

        for door in self.doors:
            door.findAttachedWalls(self.walls)
            print("door name:", door.name, 'isSingle:', door.isSingleDoor)
            if self.DEBUG:
                f.write("door name:" + str(door.name) + 'isSingle:' + str(door.isSingleDoor)+'\n')
            for wall in door.attachedWalls:
                print("attached wall name. :", wall.name)
                if self.DEBUG:
                    f.write("attached wall name. :" + str(wall.name)+'\n')
                if wall.mode == 'rect':
                    if door.params[0]>=wall.params[0] and door.params[1]>=wall.params[1]:
                        flag5 = True
                    else:
                        flag5 = False
                    if door.params[2]<=wall.params[2] and door.params[3]<=wall.params[3]:
                        flag6 = True
                    else:
                        flag6 = False
                    flag0 = flag5 and flag6
                if flag0:
                    print("Warning: A door is placed inside a wall.  Please modify the input file manually.")
           

        for exit in self.exits:
            exit.findAttachedWalls(self.walls)
            print("exit name:", exit.name, 'isSingle:', exit.isSingleDoor)
            if self.DEBUG:
                f.write("exit name:" + str(exit.name) + 'isSingle:' + str(exit.isSingleDoor)+'\n')
            for wall in exit.attachedWalls:
                print("attached wall name. :", wall.name)
                if self.DEBUG:
                    f.write("attached wall name. :" + str(wall.name)+'\n')
                if wall.mode == 'rect':
                    if exit.params[0]>=wall.params[0] and exit.params[1]>=wall.params[1]:
                        flag5 = True
                    else:
                        flag5 = False
                    if exit.params[2]<=wall.params[2] and exit.params[3]<=wall.params[3]:
                        flag6 = True
                    else:
                        flag6 = False
                    flag0 = flag5 and flag6
                if flag0:
                    print("Warning: An exit is placed inside a wall.  Please modify the input file manually.")
      
        
        for iddoor, door in enumerate(self.doors):
            if door.inComp == 0:
                continue
            
            if len(door.attachedWalls)>0:
                r1, r2, r3, r4 = door.dirWithAttachedWalls(mode='maxmin')
                #for wall in door.attachedWalls:
                if r1 is not None and r3 is not None:
                    tempmin=min(door.params[1], door.params[3])
                    tempmax=max(door.params[1], door.params[3])
                    if r1[0]-tempmin<0.3 or r3[0]-tempmin<0.3:
                        if door.params[1]<door.params[3]:
                            door.params[1]=door.params[1]-0.3
                        else:
                            door.params[3]=door.params[3]-0.3
                    if r1[-1]-tempmax>-0.3 or r3[-1]-tempmax>-0.3:
                        if door.params[1]<door.params[3]:
                            door.params[3]=door.params[3]+0.3
                        else:
                            door.params[1]=door.params[1]+0.3
                
                if r2 is not None and r4 is not None:
                    tempmin=min(door.params[0], door.params[2])
                    tempmax=max(door.params[0], door.params[2])
                    if r2[0]-tempmin<0.3 or r4[0]-tempmin<0.3:
                        if door.params[0]<door.params[2]:
                            door.params[0]=door.params[0]-0.3
                        else:
                            door.params[2]=door.params[2]-0.3
                    if r2[-1]-tempmax>-0.3 or r4[-1]-tempmax>-0.3:
                        if door.params[0]<door.params[2]:
                            door.params[2]=door.params[2]+0.3
                        else:
                            door.params[0]=door.params[0]+0.3
            #print('door.ID:', iddoor, 'door.arrow:', door.arrow, '\t')                 
            

        if self.DEBUG:
            f.write('\n\n')
        f.close()


    def preprocessAgent(self):

        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        if self.DEBUG:
            f.write("\n========================================\n")
            f.write("Preprocessing the Agent Data"+'\n')
            f.write("=========================================\n")
        #==============================================================
        # Preprocess agent features including group and exit selection
        #==============================================================

        self.num_agents= len(self.agents)
        self.num_walls = len(self.walls)
        self.num_doors = len(self.doors)
        self.num_exits = len(self.exits)
        
        person.visible_doors = np.zeros((self.num_agents, self.num_doors))
        person.visible_exits = np.zeros((self.num_agents, self.num_exits))
        
        person.exit_selected = np.zeros((self.num_agents, 1))
        person.exit_prob = np.zeros((self.num_agents, self.num_exits))
        person.exit_known = np.zeros((self.num_agents, self.num_exits))

        person.comm = np.zeros((self.num_agents, self.num_agents))
        person.talk = np.zeros((self.num_agents, self.num_agents))

        person.wall_flag = np.zeros((self.num_agents, self.num_agents))
        person.see_flag = np.zeros((self.num_agents, self.num_agents))

        if self.GROUPBEHAVIOR:
            # Initialize Desired Interpersonal Distance
            tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupSABD')
            if len(tableFeatures)<=0:
                tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&GroupSABD')
            if len(tableFeatures)<=0:
                tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupCABD')
            if len(tableFeatures)<=0:
                tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&GroupCABD')
            if len(tableFeatures)>0:
                person.CFactor_Init, person.AFactor_Init, person.BFactor_Init, person.DFactor_Init = readGroupSABD(tableFeatures, len(self.agents), len(self.agents))
                ###=== Group Behavior is simulated ===
                self.GROUPBEHAVIOR = True
            else:
                try:
                    tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupABD')
                    if len(tableFeatures)>0:
                        person.AFactor_Init, person.BFactor_Init, person.DFactor_Init = readGroupABD(tableFeatures, len(self.agents), len(self.agents))
                        self.GROUPBEHAVIOR = True
                    else:
                        person.AFactor_Init = np.zeros((self.num_agents, self.num_agents))
                        person.BFactor_Init = np.zeros((self.num_agents, self.num_agents))
                        person.DFactor_Init = np.zeros((self.num_agents, self.num_agents))
                        self.GROUPBEHAVIOR = False
                        
                    tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupS')
                    if len(tableFeatures)<=0:
                        tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&GroupS')
                    if len(tableFeatures)<=0:
                        tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupC')
                    if len(tableFeatures)>0:
                        person.CFactor_Init = readGroupS(tableFeatures, len(self.agents), len(self.agents))
                    else:
                        person.CFactor_Init = np.zeros((self.num_agents, self.num_agents))
                except:
                    person.CFactor_Init = np.zeros((self.num_agents, self.num_agents))
                    person.DFactor_Init = np.zeros((self.num_agents, self.num_agents))
                    person.AFactor_Init = np.zeros((self.num_agents, self.num_agents))
                    person.BFactor_Init = np.zeros((self.num_agents, self.num_agents))
                    self.GROUPBEHAVIOR = False
                    
                    print('Matrix C D A B are required to define the social relationship of agents if group dynamics is enabled in simulation!\n')
                    print('However, users do not input such group parameters in input csv file!')
                    if sys.version_info[0] == 2: 
                        raw_input('Please check input data here!')
                        #UserInput = raw_input('Check Input Data Here!')
                    if sys.version_info[0] == 3:
                        input('Please check input data here!')
                    
            #tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupABD')
            #person.AFactor_Init = readArrayIndex(tableFeatures, len(self.agents), len(self.agents), index=0, iniX=1, iniY=1)
            #person.BFactor_Init = readArrayIndex(tableFeatures, len(self.agents), len(self.agents), index=1, iniX=1, iniY=1)
            #person.DFactor_Init = readArrayIndex(tableFeatures, len(self.agents), len(self.agents), index=2, iniX=1, iniY=1)
            
            #tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupA')
            #person.AFactor_Init = readFloatArray(tableFeatures, len(self.agents), len(self.agents))
            #AFactor_Init = readCSV("A_Data2018.csv", 'float')
    
            #tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupB')
            #person.BFactor_Init = readFloatArray(tableFeatures, len(self.agents), len(self.agents))
            #BFactor_Init = readCSV("B_Data2018.csv", 'float')
    
            # Initialize Desired Interpersonal Distance
            #tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&groupD')
            #person.DFactor_Init = readFloatArray(tableFeatures, len(self.agents), len(self.agents))
            #DFactor_Init = readCSV("D_Data2018.csv", 'float')
            
            if self.DEBUG:
                #print >> f, "Wall Matrix\n", walls, "\n"
                f.write("C Matrix\n"+str(person.CFactor_Init)+"\n")
                f.write("A Matrix\n"+str(person.AFactor_Init)+"\n")
                f.write("B Matrix\n"+str(person.BFactor_Init)+"\n")
                f.write("D Matrix\n"+str(person.DFactor_Init)+"\n")
                
                print("C Matrix\n", person.CFactor_Init, "\n")
                print("A Matrix\n", person.AFactor_Init, "\n")
                print("B Matrix\n", person.BFactor_Init, "\n")
                print("D Matrix\n", person.DFactor_Init, "\n")
    
            if np.shape(person.CFactor_Init)!= (self.num_agents, self.num_agents):
                print('\nError on input data: CFactor_Init\n')
                f.write('\nError on input data: CFactor_Init\n')
                #raw_input('Error on input data: CFactor_Init!  Please check')
                self.inputDataCorrect = False
                
            if np.shape(person.AFactor_Init)!= (self.num_agents, self.num_agents): 
                print('\nError on input data: AFactor_Init\n')
                f.write('\nError on input data: AFactor_Init\n')
                #raw_input('Error on input data: AFactor_Init!  Please check')
                self.inputDataCorrect = False
    
            if np.shape(person.BFactor_Init)!= (self.num_agents, self.num_agents): 
                print('\nError on input data: BFactor_Init\n')
                f.write('\nError on input data: BFactor_Init\n')
                #raw_input('Error on input data: BFactor_Init!  Please check')
                self.inputDataCorrect = False
                
            if np.shape(person.DFactor_Init)!= (self.num_agents, self.num_agents):
                print('\nError on input data: DFactor_Init\n')
                f.write('\nError on input data: DFactor_Init\n')
                #raw_input('Error on input data: DFactor_Init!  Please check')
                self.inputDataCorrect = False
    
            person.CFactor = person.CFactor_Init            
            person.AFactor = person.AFactor_Init
            person.BFactor = person.BFactor_Init
            person.DFactor = person.DFactor_Init
            
        ###=== If Group Behavior is not simulated ===
        if self.GROUPBEHAVIOR == False:
            
            person.CFactor_Init = np.zeros((self.num_agents, self.num_agents))
            person.DFactor_Init = np.zeros((self.num_agents, self.num_agents))
            person.AFactor_Init = np.zeros((self.num_agents, self.num_agents))
            person.BFactor_Init = np.zeros((self.num_agents, self.num_agents))
            
            person.CFactor = person.CFactor_Init
            person.DFactor = person.DFactor_Init
            person.AFactor = person.AFactor_Init
            person.BFactor = person.BFactor_Init

        person.PFactor_Init = np.zeros((self.num_agents, self.num_agents))
        person.PFactor = np.zeros((self.num_agents, self.num_agents))
        
        #Check ID of agents
        for idai, ai in enumerate(self.agents):
            if ai.inComp == 0:
                continue
            if idai != ai.ID:
                print("Problems found in ai.ID.  Please check!")
                input("Please check!")
        
        for idai, ai in enumerate(self.agents):
            if ai.inComp == 0:
                continue
            person.PFactor_Init[idai, idai]=1-ai.p
            person.PFactor[idai, idai]=1-ai.p

        if self.inputDataCorrect:
            print("Input data format is correct!")
        else:
            print("Input data format is wrong! Please check and modify!")

        #==========Exit selection of each agent ===============
        ### This is  used in the door selection routine
        ###=== Initialize Probablity of Selecting Exits ================
        
        if self.num_exits>0 and self.solver!=1:
            tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&Ped2Exit')
            if len(tableFeatures)<=0:
                tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&Agent2Exit')
            if len(tableFeatures)<=0:
                tableFeatures, LowerIndex, UpperIndex = getData(self.FN_EVAC, '&agent2exit')
            
            
            #print('shape of tableFeatures for &Agent2Exit:', np.shape(tableFeatures))
            try:
                table2D = arr1D_2D(tableFeatures)
                (mmm, nnn) = np.shape(table2D)
                #(mmm, nnn) = np.shape(tableFeatures)
                print('shape of tableFeatures for &Agent2Exit:', (mmm-1, nnn-1))
                
                if mmm-1 < len(self.agents):
                    print("Error possibly on input data! \n The number of agents is not consistent with agent2exit data array! Please check")
                    
                if nnn-1 < len(self.exits):
                    print("Error possibly on input data! \n The number of exits is not consistent with agent2exit data array! Please check")
                    print("Zero probability colomns are added!")
                    table_new = np.zeros((mmm, len(self.exits)+1))
                    table_new[0:mmm, 0:nnn] = table2D
                    tableFeatures = table_new
            except:
                tableFeatures = np.zeros((len(self.agents)+1, len(self.exits)+1))
                for i in range(1, len(self.agents)+1):
                    for j in range(1, len(self.exits)+1):
                        tableFeatures[i, j]=float(1/len(self.exits))
            
            if self.DEBUG:
                pass
                #input("Read data from tableFeatures to define agent2exit.  Please check!")
                
            #person.exit_prob, person.exit_known = readAgent2Exit(tableFeatures, len(self.agents), len(self.exits))
            self.agent2exit = readFloatArray(tableFeatures, len(self.agents), len(self.exits))
            
            if np.shape(self.agent2exit)!= (self.num_agents, self.num_exits): #or np.shape(agent2exit)[1]!=
                print('\n!!! Error on input data: exits or agent2exit !!! \n')
                f.write('\n!!! Error on input data: exits or agent2exit !!! \n')
                #raw_input('Error on input data: exits or agent2exit!  Please check')
                self.inputDataCorrect = False
            else:
                f.write('\n Input data: exits or agent2exit: \n'+str(self.agent2exit)+'\n')
            
            
            for idai, ai in enumerate(self.agents):
                for idexit, exit in enumerate(self.exits):
                    if ai.inComp == 0 or exit.inComp == 0:
                        continue
                    else:
                        if self.agent2exit[idai, idexit]>=0.0:
                            person.exit_prob[idai, idexit] = self.agent2exit[idai, idexit]
                            person.exit_known[idai, idexit]=int(1)
                        else:
                            person.exit_prob[idai, idexit] = 0.0
                            person.exit_known[idai, idexit]=int(0)
                            
                            
            person.exit_prob = person.exit_prob * person.exit_known
            ######################################
            # Normalization of probabiligy measure
            for idai, ai in enumerate(self.agents):
                if ai.inComp == 0:
                    continue
                sumTemp = sum(person.exit_prob[idai,:])
                person.exit_prob[idai,:] = person.exit_prob[idai,:]/sumTemp
    
            if self.DEBUG:
                f.write("\n========================================\n")
                f.write("Assign destinations of agents"+'\n')
                f.write("=========================================\n")
    
            # Initialize the exit selection algorithm for each individual
            for idai, ai in enumerate(self.agents):
                if ai.inComp == 0:
                    continue
                temp = np.random.multinomial(1, person.exit_prob[idai, :], size=1)
                print(person.exit_prob[idai, :])
                print(temp)
                #if len(self.exits)>0:
                exit_index = np.argmax(temp)
                ai.dest = self.exits[exit_index].pos
                ai.exitInMind = self.exits[exit_index]   # This is the exit in one's original mind
                ai.exitInMindIndex = exit_index
                person.exit_selected[idai]=exit_index
                #if self.solver==0:
                #    ai.pathMap = self.exit2door[exit_index]
                if self.exit2door is not None:
                    ai.pathMap = self.exit2door[exit_index]
                print('ai:', idai, '--- exit:', exit_index)
                if self.DEBUG:
                    f.write('ai:' + str(ai.ID) + '--- exit:' + str(exit_index) +'\n')

        if self.DEBUG:
            f.write('\n\n')
        f.close()


    def simulation_update_agent_position(self):
        for idai,ai in enumerate(self.agents):
            
            # Whether ai is in computation
            if ai.inComp == 0:
                continue
            
            # Calculate Positions
            ai.pos = ai.pos + ai.actualV*self.DT
            #print(ai.pos)
        return None
        
        
    def simulation_update_agent_velocity(self):
        for idai,ai in enumerate(self.agents):
            
            # Whether ai is in computation
            if ai.inComp == 0:
                continue
                
            ai.accl = ai.sumF/ai.mass
            
            # Store velocity last time point
            ai.desiredV_old = ai.desiredV
            ai.actualV_old = ai.actualV
            
            # Calculate agent velocity
            ai.actualV = ai.actualV + ai.accl*self.DT
            
            #ai.vel = ai.pos + ai.actualV*self.DT
            ###########################################
            # Solution to Overspeed: Agents will not move too fast
            ai.actualSpeed = np.linalg.norm(ai.actualV)
            if (ai.actualSpeed >= ai.maxSpeed):
                ai.actualV = ai.actualV*ai.maxSpeed/ai.actualSpeed
                #ai.actualV[0] = ai.actualV[0]*ai.maxSpeed/ai.actualSpeed
                #ai.actualV[1] = ai.actualV[1]*ai.maxSpeed/ai.actualSpeed
        return None
    
    
    def simulation_step2022(self, f):
        
        # Compute the agents in single step
        # Update two lists for social interaction: see list and attention list
        # OK for solver 0,1,2
        if self.t_sim >= self.tt_OtherList:
            print('\nTime for update OtherList:', self.t_sim)
            self.tt_OtherList = self.tt_OtherList + self.DT_OtherList
            for idai, ai in enumerate(self.agents):
                if ai.inComp == 0:
                    continue
                ai.updateSeeList(self.agents, self.walls) 
                ai.updateAttentionList(self.agents, self.GROUPBEHAVIOR) #, self.WALLBLOCKHERDING)
                ai.updateTalkList(self.agents)
                #ai.updateAttentionList(self.agents, self.GROUPBEHAVIOR) #, self.WALLBLOCKHERDING)
                #ai.updatePArray(self.agents)
                print ('=== ai id ===::', idai)
                print ('ai.others len:', len(ai.others))

                ###################################################
                # Herding indicator adjusted: There are two method:
                # 1. White Noise Method
                # 2. Stress Level Method (Or known as ratioV: Helbing's Equation)
                if ai.pMode == 'random':
                    ai.p = random.uniform(0.0, 0.6)  #random.uniform(-0.3, 0.6)  # Method-1
                    #ai.p = random.uniform(-0.3, 0.6*ai.stressLevel)
                elif ai.pMode =='stress':
                    ai.p = ai.stressLevel
                    #ai.p = 1 - ai.ratioV  	# Method-2 ai.p=ai.stressLevel
                elif ai.pMode =='fixed':
                    pass
                
            person.CFactor=person.CFactor_Init*person.comm
            CArray=person.CFactor_Init*person.comm
            for idai,ai in enumerate(self.agents):
                if ai.inComp == 0:
                    continue
                if np.sum(np.fabs(CArray[idai,:]))>0:
                    CArray[idai,:] = np.sign(CArray[idai,:])*np.fabs(CArray[idai,:])/np.sum(np.fabs(CArray[idai,:]))
                #if np.sum(CArray[idai,:])>0:
                    #CArray[idai,:] = CArray[idai,:]/np.sum(CArray[idai,:])
                    for idaj,aj in enumerate(self.agents):
                        if idaj == idai:
                            person.PFactor[idai,idaj] = 1-ai.p*np.sum(CArray[idai,:])
                            #person.PFactor[idai,idaj] = 1-ai.p
                        else:
                            person.PFactor[idai,idaj] = CArray[idai,idaj]*ai.p
                else:
                    #person.PFactor[idai,idai]=1.0
                    for idaj,aj in enumerate(self.agents):
                        if idaj == idai:
                            person.PFactor[idai,idaj] = 1.0
                            #person.PFactor[idai,idaj] = 1-ai.p
                        else:
                            person.PFactor[idai,idaj] = 0.0

            person.CFactor=CArray
            
            print("person.see_flag:\n", person.see_flag)
            print("person.comm:\n", person.comm)
            print("person.talk:\n", person.talk)
            #print("person.DFactor:\n", person.DFactor)
            print("person.CFactor:\n", person.CFactor)
            print("person.PFactor:\n", person.PFactor)

            #FN_Temp = self.outDataName + ".txt"
            #f = open(FN_Temp, "a+")
            f.write('\n\n&SimuTime\n')
            f.write('\n\n&AttentionList\n')
            f.write('SimulationTime=' + str(self.t_sim)+'\n')
            f.write("person.see_flag:\n"+str(person.see_flag)+'\n')
            f.write("person.comm:\n"+str(person.comm)+'\n')
            f.write("person.talk:\n"+str(person.talk)+'\n')
            #f.write("person.DFactor:\n"+str(person.DFactor))
            f.write("person.CFactor:\n"+str(person.CFactor)+'\n')
            f.write("person.PFactor:\n"+str(person.PFactor)+'\n')
            
            f.write("person.visible_doors:\n"+str(person.visible_doors)+'\n')
            f.write("person.visible_exits:\n"+str(person.visible_exits)+'\n')

            f.write('\nEndAttentionList!')
            f.write('\n')
            f.write('\n')
            #f.close()
                    
        #if (self.t_sim < ai.tpre):
        if self.t_sim >= self.tt_ChangeDoor and self.num_exits>0 and self.solver!=1:
            print('Time for update ExitProb:', self.t_sim)
            self.tt_ChangeDoor = self.tt_ChangeDoor + self.DT_ChangeDoor

            #ratio_exit_selected = np.zeros((1,self.num_exits))
            #for idexit, exit in enumerate(self.exits):
            #    if exit.inComp ==0:
            #        continue
            #    else:
            #        for idai in range(person.exit_selected):
            
            # Update door selection probability
            print("person.exit_known:\n", person.exit_known)


            #FN_Temp = self.outDataName + ".txt"
            #f = open(FN_Temp, "a+")
            f.write('\n\n&DoorProb\n')
            f.write('SimulationTime=' + str(self.t_sim)+'\n')
            f.write('person.exit_prob:\n'+str(person.exit_prob)+'\n')
            f.write('person.exit_known:\n'+str(person.exit_known)+'\n')
            for i in range(len(person.exit_prob)):
                f.write('prob=')
                f.write(str(person.exit_prob[i]))
                f.write('\n')
            f.write('\nWellDone!')
            f.write('\n')
            f.write('\n')
            #f.close()

            # Start to search visible doors
            #ai.visibleDoors=ai.findVisibleTarget(self.walls, self.doors)
            ai.updateVisibleDoors(self.walls, self.doors)
            print ('ai:', ai.ID, 'Length of visibleDoors:', len(ai.visibleDoors))
        
            # Start to search visible exits
            #ai.visibleExits=ai.findVisibleTarget(self.walls, self.exits)
            ai.updateVisibleExits(self.walls, self.exits)

            #Visible_exits are known exits           
            person.exit_konwn = person.visible_exits + person.exit_known
            (M,N)=np.shape(person.exit_konwn)
            for i in range(M):
                for j in range(N):
                    if person.exit_known[i,j]>0:
                        person.exit_known[i,j]=int(1)

            person.exit_prob = person.exit_prob * person.exit_known
            for idai, ai in enumerate(self.agents):

                if ai.inComp == 0:
                    continue
                #ai.updateExitProb(self.agents)

                if np.sum(person.comm[idai, :])<=1:
                    continue
                ratio_utility = np.zeros((1,self.num_exits))
                for idexit, exit in enumerate(self.exits):
                    if exit.inComp == 0:
                        continue
                    elif person.exit_known[idai, idexit] == 0:
                        continue
                    else:
                        distanceEuler = np.linalg.norm(ai.pos - exit.pos) #Manhattan Distance?
                        distanceManhatton = -0.2*(fabs(ai.pos[0] - exit.pos[0])+fabs(ai.pos[1] - exit.pos[1]))
                        ratio_utility[0, idexit] = np.exp(distanceManhatton)

                print('Initial ratio_utility', ratio_utility)
                if np.sum(ratio_utility)>0:
                    ratio_utility = ratio_utility/np.sum(ratio_utility)                
                                        
                ratio_exit_selected = np.zeros((1,self.num_exits))
                for aj in ai.others:
                    ratio_exit_selected[0, aj.exitInMindIndex] +=1

                print('Initial exit selected by others', ratio_exit_selected)
                if np.sum(ratio_exit_selected)>0:
                    ratio_exit_selected = ratio_exit_selected/np.sum(ratio_exit_selected)

                print('Print ratio_exit_selected and person.exit_prob[idai, :]!')
                print(ratio_exit_selected)
                print(person.exit_prob[idai, :])
                print("decision parameter p:", ai.p)

                if np.sum(ratio_exit_selected)>0:
                    #person.exit_prob[idai, :] = ai.p1*(ai.p1+ai.p2)*(1-ai.p)*person.exit_prob[idai, :] + ai.p2*(ai.p1+ai.p2)*(1-ai.p)*ratio_utility + ai.p*ratio_exit_selected
                    
                    #person.exit_prob[idai, :] = ai.W1*person.exit_prob[idai, :] + ai.W2*ratio_utility + ai.W3*ratio_exit_selected
                    
                    person.exit_prob[idai, :] = (1-ai.pp2)*(1-ai.p)*person.exit_prob[idai, :] + ai.pp2*(1-ai.p)*ratio_utility + ai.p*ratio_exit_selected
                    
                    #person.exit_prob[idai, :] = (1-ai.p)*person.exit_prob[idai, :] +ai.p*ratio_exit_selected
                    
                print(person.exit_prob[idai, :])
                temp = np.random.multinomial(1, person.exit_prob[idai, :], size=1)
                print(temp)
                exit_index = np.argmax(temp)
                ai.dest = self.exits[exit_index].pos
                ai.exitInMind = self.exits[exit_index]   # This is the exit in one's original mind
                person.exit_selected[idai]=exit_index
                ai.exitInMindIndex = exit_index
                #if self.solver==0:
                #    ai.pathMap = self.exit2door[exit_index]
                if self.exit2door is not None:
                    ai.pathMap = self.exit2door[exit_index]
                print('ai:', idai, '--- exit:', exit_index)
                if self.DEBUG:
                    f.write('ai:' + str(ai.ID) + '--- exit:' + str(exit_index) +'\n')

            print('Simulation Time:', self.t_sim)
            print(person.exit_prob)


        f.write('\n\n&SimulationTime:' + str(self.t_sim)+'\n')
        for idai,ai in enumerate(self.agents):
        
            # Whether ai is in computation
            if ai.inComp == 0:
                continue

            # Stress indicator is used (Or known as ratioV)
            if ai.desiredSpeed != 0: 
                ai.ratioV = ai.actualSpeed/ai.desiredSpeed
            else: 
                ai.ratioV = 1
            ai.stressLevel = 1 - ai.ratioV
            ai.test = 0.0 #??
            
            ai.updateStress(flag='accumulate')
            #ai.updateAttentionList(self.agents, self.GROUPBEHAVIOR)
            #ai.updateTalkList(self.agents)

            if self.OPINIONMODEL == 0:
                ai.opinionDynamics()
            elif self.OPINIONMODEL == 1:
                ai.opinionExchange()

            ###########################################
            ## Output time when agents reach the safety
            if self.solver==0 and self.num_exits==0:
                if (np.linalg.norm(ai.pos-ai.dest)<=0.2) and (ai.Goal == 0):
                    print ('Reaching the goal:')
                    ai.inComp = 0
                    ai.Goal = 1
                    ai.timeOut = self.t_sim
                    ai.tpre = 0.0
                    print ('Time to Reach the Goal:', ai.timeOut)
                    f.write('&FinalInfo')
                    f.write('agent ID'+str(ai.ID)+'\n'+'Time to Reach the Goal:'+str(ai.timeOut))

            ###########################################
            ## Remove agent when agent reaches the exit
            else:
                #for exit in self.exits:
                for idexit, exit in enumerate(self.exits):
                    if exit.inComp == 0:
                        continue
                    if exit.inside(ai.pos):
                        ai.inComp = 0
                        ai.Goal = 1
                        ai.timeOut = self.t_sim
                        ai.tpre = 0.0
                        self.exitUsage[idexit,0] +=1
                        print ('Time to reach an exit:', ai.timeOut)
                        #print('exitUsage:', np.transpose(self.exitUsage))
                        #print ('Time to reach an exit:', ai.timeOut)
                        #input("Please check!")
                        
                        f.write('\n\n&FinalInfo\n')
                        f.write('agent ID'+str(ai.ID)+'\t reach the exit ID'+str(exit.oid)+'\n')
                        f.write('agent ID'+str(ai.ID)+'\t reaches the exit at time   '+str(ai.timeOut)+'\n')
                        f.write('exitUsage in time:'+str(np.transpose(self.exitUsage)))


            '''
            FN_Temp = self.outDataName + ".txt"
            f = open(FN_Temp, "a+")
            f.write('&SimuTime\n')
            f.write('Simulation Time:' + str(self.t_sim)+'\n')
            f.write('&DoorProb\n')
            f.write('person.exit_prob:\n'+str(person.exit_prob)+'\n')
            for i in range(len(person.exit_prob)):
                f.write('prob=')
                f.write(str(person.exit_prob[i]))
                f.write('\n')
            f.write('\nWellDone!')
            f.write('\n')
            f.write('\n')
            f.close()
            '''
        

    def simulation_update_agent_desiredV(self, f):
        #f.write('\n\n&Simulation Time:\n')
        f.write('\n\n&SimulationTime:' + str(self.t_sim)+'\n')
        for idai,ai in enumerate(self.agents):
            
            # Whether ai is in computation
            if ai.inComp == 0:
                continue
            
            # Calculate Positions
            #ai.pos = ai.pos + ai.actualV*self.DT
            #print(ai.pos)
            #print(accl,ai.actualV,ai.pos)
            
            #ai.dest = ai.memory.peek()
            
            #ai.direction = normalize(ai.dest - ai.pos)
            #ai.desiredV = ai.desiredSpeed*ai.direction
            #ai.desiredV = 0.7*ai.desiredV + 0.3*ai.desiredV_old

            #ai.actualSpeed = np.linalg.norm(ai.actualV)
            #ai.desiredSpeed = np.linalg.norm(ai.desiredV)
            
            #print >> f, "desired speed of agent i:", ai.desiredSpeed, "/n"
            #print >> f, "actual speed of agent i:", ai.actualSpeed, "/n"
            
            #############################################
            # Calculate Motive Forces
            # Consider TPRE features
            #############################################	

            #Pre-Evacuation Time Effect
            #tt = pygame.time.get_ticks()/1000 - t_pause
            if (self.t_sim < ai.tpre):
                #ai.desiredSpeed = random.uniform(0.3,1.6)
                goDoor = None
                #ai.preEvacModel()
                motiveForce = ai.adaptMotiveForce()
                
                '''
                if (ai.tpreMode == 1): # Desired velocity is zero
                    ai.desiredV = ai.direction*0.0
                    ai.desiredSpeed = 0.0
                    #ai.dest = ai.pos
                    ai.tau = random.uniform(2.0,10.0) #ai.tpre_tau
                    motiveForce = ai.adaptMotiveForce()
            
                #ai.sumAdapt += motiveForce*0.2  #PID: Integration Test Here
            
                if (ai.tpreMode == 2): # Motive Force is zero
                    motiveForce = np.array([0.0, 0.0])
                    ai.motiveF = np.array([0.0, 0.0])

                if (ai.tpreMode == 3):
                    if outsideDoor:
                        doorInter = np.array([0.0, 0.0])
                        
                    goSomeone = ai.moveToAgent()
                    if goSomeone is not None:
                        gsid = goSomeone.ID
                        ai.diretion = normalize(goSomeone.pos - ai.pos)
                        ai.desiredSpeed = random.uniform(0.6,1.6)
                        ai.desiredV = ai.diretion*ai.desiredSpeed
                        ai.tau = random.uniform(0.6,1.6) #ai.tpre_tau
                        motiveForce = ai.adaptMotiveForce()
                        print ('ai:', ai.ID, '&&& In Tpre Stage:')
                        print ('goSomeone:', goSomeone.ID)
                        print ('postion:', ai.pos)
                    else:
                        ai.desiredV = ai.direction*0.0
                        ai.desiredSpeed = 0.0
                        ai.tau = random.uniform(2.0,10.0) #ai.tpre_tau
                        motiveForce = ai.adaptMotiveForce()
                        print  ('ai:', ai.ID, '&&& In Tpre Stage:')
                        print ('goSomeone is None.')
                        print ('postion:', ai.pos)
                '''
                    
            if (self.t_sim >= ai.tpre):

                print ('ai:', ai.ID, '&&& In Movement Stage:')
                print ('postion:', ai.pos)
                print ('goTarget:', ai.exitInMindIndex)
                
                # solver=0: No flow field is directly used in agent-based simulation
                # solver=0 has some problem unsolved
                if self.solver==0:
                    
                    goDoor = ai.selectTarget(self.exit2door)
                    
                    #goDoor.computePos()
                    if goDoor is None:
                        print ('goDoor is None.')
                        doorInter = np.array([0.0, 0.0])
                        
                        #print ('ai:', ai.ID)
                        otherDir = np.array([0.0, 0.0])
                        otherSpeed = 0.0
                        #otherMovingNum = 0
                        if len(ai.others)!=0: #and tt>ai.tpre:
                            otherDir, otherSpeed = ai.opinionDynamics()
                            ai.direction = (1-ai.p)*ai.direction + ai.p*otherDir
                            ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + ai.p*otherSpeed
                            ai.desiredV = ai.desiredSpeed*ai.direction
                        else:
                            ai.dest = ai.exitInMind.pos
                            ai.dirction=normalize(ai.exitInMind.pos - ai.pos)
                            ai.desiredV = ai.desiredSpeed*ai.direction                                    
                        
                        motiveForce = ai.adaptMotiveForce()
                        
                    else:
                        print ('go Door:', goDoor.oid, goDoor.pos)
                        doorInter = ai.doorForce(goDoor, 'edge', 0.3)
                        
                        #dir1=goDoor.direction()
                        #dir2=goDoor.pos-ai.pos
                        #if goDoor!=None: #and np.dot(dir1, dir2)>=0:
                        #visiblePx(ai, walls)
                        ai.direction = normalize(goDoor.pos-ai.pos)
                        ai.desiredSpeed = random.uniform(0.6,1.6) # 1.0
                        ai.desiredV = ai.desiredSpeed*ai.direction
                        motiveForce = ai.adaptMotiveForce()
                        
                        ### ??? ###
                        if goDoor.inside(ai.pos):
                            ai.direction = normalize(goDoor.direction(goDoor.arrow))  #(ai.desiredV_old) 
                            ai.desiredSpeed = random.uniform(0.6,1.6)
                            ai.desiredV = ai.desiredSpeed*ai.direction
                            motiveForce = ai.adaptMotiveForce()
                            if np.linalg.norm(goDoor.pos - ai.pos)<1.0e-6:
                                if len(ai.route) == 0:
                                    ai.route.append(goDoor.pos)
                                #if ai.route[len(ai.route)-1] is not goDoor.pos
                                #    print 'Error in ai.route!'
                                elif ai.route[-1] != goDoor.pos:
                                    ai.route.append(goDoor.pos)

                    # Interaction with enviroment
                    # Search for wall on the route
                    # temp = 0.0
                    closeWall = None #None #walls[0]
                    closeWallDist = 10.0 # Define how close the wall is
                    for wall in self.walls:
                        if wall.inComp ==0:
                            continue
                        crossp, diw, arrow = ai.wallOnRoute(wall, 1.0)
                        if diw!=None and diw < closeWallDist:
                            closeWallDist = diw
                            closeWall = wall
    
    
                    closeWallEffect = True
                    crossp, diw, wallDirection = ai.wallOnRoute(closeWall, 1.0)
                    if diw!=None and goDoor!=None and outsideDoor:
                        if goDoor.inside(crossp):
                            #wallInter = wallInter - ai.wallForce(closeWall)
                            closeWallEffect = False
                        else:
                            if np.dot(wallDirection, ai.desiredV) < 0.0 and wall.arrow==0:
                                #0.3*ai.desiredV+0.7*ai.desiredV_old) < 0.0:
                                wallDirection = -wallDirection
                            ai.direction = ai.direction + wallDirection*20/diw
                            ai.direction = normalize(ai.direction)
                            ai.desiredV = ai.desiredSpeed*ai.direction
    
    
                    if diw is not None and goDoor is None: # and not ai.visibleDoors:
                    #if closeWall!=None:
                    #    diw = ai.wallOnRoute(closeWall)
                        #wallDirection = np.array([closeWall.params[0],closeWall.params[1]]) - np.array([closeWall.params[2],closeWall.params[3]])
                        #wallDirection = -normalize(wallDirection)
                        #if wall.arrow==0 or ai.aType=='search': 
                        if np.dot(wallDirection, ai.actualV) < 0.0 and wall.arrow==0:
                            #0.3*ai.desiredV+0.7*ai.desiredV_old) < 0.0:
                            wallDirection = -wallDirection
    
                        #if (np.isnan(closeWall.pointer1[0]) or np.isnan(closeWall.pointer1[1])) and (np.isnan(closeWall.pointer2[0]) or np.isnan(closeWall.pointer2[1])) or ai.aType=='search': 
                        if np.isnan(closeWall.pointer1[0]) or np.isnan(closeWall.pointer1[1]) or ai.aType=='search':
                            pass
                            if diw==None:
                                print ('diw==None')
                                print ('ai:', idai)
                                print ('closeWall:', closeWall.id)
                                print ('################################')
                            
                            ai.direction = ai.direction + wallDirection*20/diw
                            ai.direction = normalize(ai.direction)
                            ai.desiredV = ai.desiredSpeed*ai.direction
                            #ai.destmemory.append([wall[2],wall[3]]+0.1*wallDirection)
                        #elif ai.destmemory[-1] is not [closeWall[5], closeWall[6]]:  
                            #ai.destmemory[-1][0]!=closeWall[5] or ai.destmemory[-1][1]!= closeWall[6]:
                            #ai.destmemory.append([wall[0],wall[1]]+0.1*wallDirection)
                            #ai.destmemory.append([closeWall[5], closeWall[6]])
                            #ai.direction = normalize(ai.destmemory[-1]-ai.pos)
                            #ai.desiredV = ai.desiredSpeed*ai.direction
                        else:
                            temp1= np.linalg.norm([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                            temp2= np.linalg.norm([closeWall.pointer2[0], closeWall.pointer2[1]]-ai.pos)
                            for aj in ai.others:
                                temp1 = temp1+np.linalg.norm([closeWall.pointer1[0], closeWall.pointer1[1]]-aj.pos)
                                temp2 = temp2+np.linalg.norm([closeWall.pointer2[0], closeWall.pointer2[1]]-aj.pos)
                            if temp1<temp2:
                                ai.direction = normalize([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                            else:
                                ai.direction = normalize([closeWall.pointer2[0], closeWall.pointer2[1]]-ai.pos)
                            #ai.direction = normalize([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                            ai.desiredV = ai.desiredSpeed*ai.direction
                    
                        #ai.direction = ai.direction + wallDirection/np.linalg.norm(wallDirection)*20/diw
                        #ai.desiredV = ai.desiredSpeed*ai.direction
                    
                    #if np.linalg.norm(ai.pos-ai.destmemory[-1])<=1e-3:
                    #    ai.destmemory.pop()
                    ai.tau=ai.moving_tau
                    motiveForce = ai.adaptMotiveForce()	
                    
                else:
                    if self.solver==1:
                        ai.pathMapU = self.UallExit[1:-1, 1:-1]
                        ai.pathMapV = self.VallExit[1:-1, 1:-1]
                    if self.solver==2:
                        for idexit, exit in enumerate(self.exits):
                            if ai.exitInMind == exit:
                                ai.pathMapU = self.UeachExit[idexit] 
                                ai.pathMapV = self.VeachExit[idexit]
                                ai.pathMapU = ai.pathMapU[1:-1, 1:-1]
                                ai.pathMapV = ai.pathMapV[1:-1, 1:-1]

                    iii=int((ai.pos[0]-self.xmin)/self.dx)
                    jjj=int((ai.pos[1]-self.ymin)/self.dy)

                    ifloor=int(floor((ai.pos[0]-self.xmin)/self.dx))
                    jfloor=int(floor((ai.pos[1]-self.ymin)/self.dy))

                    iceil=int(ceil((ai.pos[0]-self.xmin)/self.dx))
                    jceil=int(ceil((ai.pos[1]-self.ymin)/self.dy))

                    Uave=0.25*(ai.pathMapU[ifloor,jfloor]+ai.pathMapU[iceil,jceil]+ai.pathMapU[ifloor,jceil]+ai.pathMapU[iceil,jfloor])
                    Vave=0.25*(ai.pathMapV[ifloor,jfloor]+ai.pathMapV[iceil,jceil]+ai.pathMapV[ifloor,jceil]+ai.pathMapV[iceil,jfloor])
                    ai.direction = normalize(np.array([Uave, Vave]))

                    #ai.direction = normalize(np.array([ai.pathMapU[iii,jjj] , ai.pathMapV[iii,jjj]]))
                    ai.tau = 0.2
                    ai.desiredSpeed = random.uniform(2.0,3.0)
                    #ai.desiredSpeed = 2.0 #random.uniform(0.3,2.3) #1.8
                    ai.desiredV = ai.desiredSpeed*ai.direction
                    motiveForce = ai.adaptMotiveForce()

            if self.solver == 0 or self.num_exits == 0:
                if goDoor is not None:
                    f.write('goDoor:'+str(goDoor.oid)+'\n')
                else:
                    f.write('goDoor: None'+'\n')
            elif self.solver ==2:
                f.write('ExitSelected:'+str(ai.exitInMind.oid)+'\n')
            else:
                f.write('The Nearest Exit is Selected.  No exit selection algorithm is involved.'+'\n')

            #f.write('visibleDoors:'+str(ai.visibleDoors)+'\n')
            #f.write('visibleExits:'+str(ai.visibleExits)+'\n')

            #ai.others=list(set(ai.others))
            #################################
            # Herding Effect Computed
            # Also known as opinion dynamics
            #################################
            #if otherMovingNum != 0:
                #ai.direction = (1-ai.p)*ai.direction + ai.p*otherMovingDir
                #ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + #ai.p*otherMovingSpeed/otherMovingNum
                #ai.desiredV = ai.desiredSpeed*ai.direction
                #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*otherMovingDir


    def simulation_update_agent_force(self, f):
        #f.write('\n\n&Simulation Time:\n')
        f.write('\n\n&SimulationTime:' + str(self.t_sim)+'\n')
        for idai,ai in enumerate(self.agents):
            
            # Whether ai is in computation
            if ai.inComp == 0:
                continue
            
            # Calculate Positions
            #ai.pos = ai.pos + ai.actualV*self.DT
            #print(ai.pos)
            #print(accl,ai.actualV,ai.pos)
            
            #ai.dest = ai.memory.peek()
            
            #ai.direction = normalize(ai.dest - ai.pos)
            #ai.desiredV = ai.desiredSpeed*ai.direction
            #ai.desiredV = 0.7*ai.desiredV + 0.3*ai.desiredV_old

            #peopleInter = np.array([0.0, 0.0])
            #wallInter = np.array([0.0, 0.0])
            #doorInter = np.array([0.0, 0.0])
            
            #phyInter = np.array([0.0, 0.0])
            #phySFInter = np.array([0.0, 0.0])
            #phyWFInter = np.array([0.0, 0.0])

            #ai.diw_desired = max(0.2, ai.ratioV)*0.6
            #ai.A_WF = 700*max(0.3, ai.ratioV)
            #ai.B_WF = 1.6*max(min(0.6, ai.ratioV),0.2)
            
            ai.diw_desired = max(0.5, ai.ratioV)*0.6
            #ai.A_WF = 30*max(0.5, ai.ratioV)
            ai.B_WF = 2.2*max(min(0.5, ai.ratioV),0.2) 

            motiveForce = ai.adaptMotiveForce()
            peopleInter = np.array([0.0, 0.0])
            wallInter = np.array([0.0, 0.0])
            doorInter = np.array([0.0, 0.0])
            
            phyInter = np.array([0.0, 0.0])
            phySFInter = np.array([0.0, 0.0])
            phyWFInter = np.array([0.0, 0.0])

            ai.actualSpeed = np.linalg.norm(ai.actualV)
            ai.desiredSpeed = np.linalg.norm(ai.desiredV)
            
            #print >> f, "desired speed of agent i:", ai.desiredSpeed, "/n"
            #print >> f, "actual speed of agent i:", ai.actualSpeed, "/n"
            
            ######################
            # Wall force adjusted
            
            #ai.diw_desired = max(0.2, ai.ratioV)*0.6
            #ai.A_WF = 700*max(0.3, ai.ratioV)
            #ai.B_WF = 1.6*max(min(0.6, ai.ratioV),0.2)
            
            ai.diw_desired = max(0.5, ai.ratioV)*0.6
            #ai.A_WF = 30*max(0.5, ai.ratioV)
            ai.B_WF = 2.2*max(min(0.5, ai.ratioV),0.2) 
            
            #tt = pygame.time.get_ticks()/1000-t_pause
            wallInter, doorInter, outsideDoor = ai.adaptWallDoorForce(self.walls, self.doors)
            
            ########################################################
            # Turn on or off self-repulsion by boolean variable SELFREPULSION
            # Also known as sub-consciousness effect in crowd dynamics
            ########################################################
            if self.SELFREPULSION:
                selfRepulsion = ai.adaptSelfRep(person.DFactor[idai, idai], person.AFactor[idai, idai], person.BFactor[idai, idai])#*ai.direction
            else:
                selfRepulsion = np.array([0.0, 0.0])
            
            if self.FLUCTUATION:
                flucInter = ai.adaptFluctuationForce(noiseLevel=self.flucNoiseLevel)
            else:
                flucInter = np.array([0.0, 0.0])
                
            
            peopleInter = ai.adaptSocialForce(self.agents, self.GROUPBEHAVIOR, True)
                
            #peopleInter = + ai.adaptPhyForce(self.agents)
            
            phySFInter = ai.adaptPhysicSF(self.agents, f)
            phyWFInter = ai.adaptPhysicWF(self.walls)
            phyInter = phySFInter + phyWFInter
            
            ai.subF = motiveForce + peopleInter + wallInter + doorInter + ai.diss*ai.actualV + selfRepulsion + flucInter
            ai.objF = phyInter #ai.adaptPhysicSF(self.agents) + ai.adaptPhysicWF(self.walls)
                
            # Compute total force
            ai.sumF = motiveForce + peopleInter + wallInter + doorInter + ai.diss*ai.actualV + selfRepulsion + phyInter + flucInter #+ ai.sumAdapt
 
            # Compute acceleration
            #ai.accl = ai.sumF/ai.mass
            
            # Store velocity last time point
            #ai.desiredV_old = ai.desiredV
            #ai.actualV_old = ai.actualV
            # Update agent velocity
            #ai.actualV = ai.actualV + ai.accl*self.DT # consider dt = 0.5

            #ai.wallrepF = wallInter
            #ai.doorF = doorInter
            #ai.groupF = peopleInter

            if self.TESTFORCE:
                print ('@drivingForce:', np.linalg.norm(motiveForce), motiveForce)
                print ('@socialForce:', np.linalg.norm(peopleInter), peopleInter)
                print ('@wallForce:', np.linalg.norm(wallInter), wallInter)
                print ('@doorForce:', np.linalg.norm(doorInter), doorInter)
                print ('@diss:', np.linalg.norm(ai.diss*ai.actualV), ai.diss*ai.actualV)
                print ('@selfRepulsion:', np.linalg.norm(selfRepulsion), selfRepulsion, '\n')
            
                f.write('\nAgent:\t'+str(ai.ID) + ':'+str(ai.name) + '\n')
                f.write('Simulation Time:' + str(self.t_sim) + '\n')
                f.write('Position:\t'+str(ai.pos)+'\n')
                f.write('Velocity:\t'+str(np.linalg.norm(ai.actualV)) + ': ['+str(ai.actualV[0])+' , '+str(ai.actualV[1])+']\n')
                f.write('DesiredVelocity:\t'+str( np.linalg.norm(ai.desiredV))+ ': ['+str(ai.desiredV[0])+ ' , '+str(ai.desiredV[1])+']\n')
                f.write("@motiveForce:\t"+str( np.linalg.norm(motiveForce))+ ': ['+str(motiveForce[0])+ ' , '+str(motiveForce[1])+']\n')
                f.write('@socialForce:\t'+str(np.linalg.norm(peopleInter))+ ': ['+str(peopleInter[0])+ ' , '+str(peopleInter[1])+']\n')
                f.write('@wallForce:\t'+str(np.linalg.norm(wallInter))+ ': ['+str(wallInter[0])+ ' , '+str(wallInter[1])+']\n')
                f.write('@doorForce:\t'+str(np.linalg.norm(doorInter))+ ': ['+str(doorInter[0])+ ' , '+str(doorInter[1])+']\n')
                f.write('@diss:\t'+str(np.linalg.norm(ai.diss*ai.actualV))+ ': ['+str(ai.diss*ai.actualV[0])+ ' , '+str(ai.diss*ai.actualV[1])+']\n')
                f.write('@selfRepulsion:\t'+str(np.linalg.norm(selfRepulsion))+ ': ['+str(selfRepulsion[0])+ ' , '+str(selfRepulsion[1])+']\n')
                
                f.write('@subF:\t'+str(np.linalg.norm(ai.subF))+ ': ['+str(ai.subF[0])+ ' , '+str(ai.subF[1])+']\n')
                f.write('@objF:\t'+str(np.linalg.norm(ai.objF))+ ': ['+str(ai.objF[0])+ ' , '+str(ai.objF[1])+']\n')
                f.write('Premovement Time:'+str(ai.tpre)+'\n')
                f.write('numOtherSee:'+str(len(ai.seeothers))+'\n')
                f.write('numOther:'+str(len(ai.others))+'\n')
                
            '''
            ###########################################
            ## Output time when agents reach the safety
            if self.TIMECOUNT and (np.linalg.norm(ai.pos-ai.dest)<=0.2) and (ai.Goal == 0):
                print ('Reaching the goal:')
                ai.inComp = 0
                ai.Goal = 1
                ai.timeOut = self.t_sim
                print ('Time to Reach the Goal:', ai.timeOut)
                #f.write('agent ID'+str(ai.ID)+'\n'+'Time to Reach the Goal:'+str(ai.timeOut))
            

            ###########################################
            ## Remove agent when agent reaches the exit    
            for exit in self.exits:
                if exit.inComp == 0:
                    continue
                if exit.inside(ai.pos):
                    ai.inComp = 0
                    ai.Goal = 1
                    ai.timeOut = self.t_sim
                    print ('Time to reach an exit:', ai.timeOut)
                    #f.write('agent ID'+str(ai.ID)+'\n'+'Time to Reach the Goal:'+str(ai.timeOut))
            '''

        f.write('\n&EndofStep:'+str(self.t_sim)+'\n')
        #f.write('SimulationTime=' + str(self.t_sim)+'\n')
        # Update simulation time
        self.t_sim = self.t_sim + self.DT

                    
    def quit(self):
        #if self.dumpBin:
        #    self.fbin.close()
        #sys.exit()
        #self.destory()
        pass
        return None


    def autoPlot(self):
        #if self.autoPlotLogic:
        try:
            visualizeTpre(self.outDataName +'.bin', showdata=True)
            readDoorProb(self.outDataName +'.txt', showdata=True)
            
            #np.histogram() ??
            '''
            if len(self.exits)>0:
                plt.bar(np.arange(len(self.exits)), self.exitUsage)
                plt.title("Exit Usage Histogram:")
                plt.grid()
                plt.legend(loc='best')
                plt.xlabel("Exit_Index")
                plt.ylabel("Num_of_Agents")
                temp=self.outDataName.split('.')
                namePNG = temp[0]+'exitUsage.png'
                plt.savefig(namePNG)
                plt.show()
            '''
        except:
            input("Unable to plot figures from output data!  Please check!")
        return None
    
    
    def dataComplete(self):
        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        print('Exit Usage: ', np.transpose(self.exitUsage))
        f.write('Exit Usage: '+str(np.transpose(self.exitUsage)))
        f.close()
    

if __name__=="__main__":
    #from ui import*
    myTest = simulation() #("E:\gitwork\CrowdEgress\examples\DoorAlgorithm\testnote")
    myTest.select_file(None, None, "smallGUI")
    #myTest.read_data()
    show_geom(myTest)
    
    if myTest.continueToSimu:
        myTest.readconfig()
        myTest.preprocessGeom()
        myTest.preprocessAgent()
        if myTest.solver == 1 or myTest.solver == 2:
            myTest.buildMesh()
            myTest.flowMesh()
            myTest.computeDoorDirection()
            show_flow(myTest)
            
        myTest.dataSummary()
        show_simu(myTest)
    else:
        os.remove(myTest.outDataName + ".txt")
        #try
        #    os.remove(myTest.outDataName + ".bin")
        #except:
    #myTest.quit()



