
import os, sys, csv
import re
from simulation import *
from data_func import *
from draw_func import *
#import numpy as np

#from tkinter import ttk
#from tkinter import *

# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    #from tkinter import ttk
    from tkinter.ttk import Notebook
    from tkinter.ttk import Treeview
    from tkinter.ttk import Button
    import tkinter.filedialog as tkf
    import tkinter.messagebox as msg
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    from ttk import Treeview
    from ttk import Entry
    import tkFileDialog as tkf
    import tkMessageBox as msg


agents=None
agent2exit=None
agentgroup=None
walls=None
exits=None
doors=None
exit2door=None

'''
RNA=0
RNA2E=0
RNAG=0
RNW=0
RNE=0
RNR=0
RNE2D=0
'''

openFileName = None
currentdir = None
if os.path.exists("log.txt"):
    for line in open("log.txt", "r"):
        if re.match('FN', line):
            temp =  line.split('=')
            openFileName = temp[1].strip()
            currentdir = os.path.dirname(openFileName)


def viewCSV(event=None):
    os.system('notepad '+ os.path.join(openFileName))

##############################################################
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


# Sequentially search for Title1, Title2 and Title3 through FileName
def readTitle(FileName, Title1=None, Title2=None, Title3=None):
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
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    #dataNP = np.array(strData)
    #print (dataNP)
    #print ('np.shape(dataNP)', np.shape(dataNP))
    #print ('\n')

    #print(strData[1:,1:])
    csvFile.close()
    #return dataNP
    return strData


def getData(fileName, strNote):
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

        dataOK = list(dataFeatures[IPedStart : IPedEnd])
        return dataOK, IPedStart, IPedEnd

    #data_result = np.array(dataOK)
    #return data_result[1:, 1:]
    

def readSocialCSV(FileName, debug=True, marginTitle=1):

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
        agent2exitFeatures, lowerIndex, upperIndex = getData(FileName, '&Agent2Exit')
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
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupS')
        Num_AgentGroup=len(agentgroupFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&GroupS')
        Num_AgentGroup=len(agentgroupFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupCABD')
        Num_AgentGroup=len(agentgroupFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupSABD')
        Num_AgentGroup=len(agentgroupFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&GroupSABD')
        Num_AgentGroup=len(agentgroupFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupABD')
        Num_AgentGroup=len(agentgroupFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&GroupABD')
        Num_AgentGroup=len(agentgroupFeatures)-marginTitle
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

    zoomFeature = readTitle(FileName, '&ZOOM', '&zoom', 'ZOOM')
    xspaceFeature = readTitle(FileName, '&OFFSET_X', '&offset_x', 'xSpace')
    yspaceFeature = readTitle(FileName, '&OFFSET_Y', '&offset_y', 'ySpace')
    
    dtFeature = readTitle(FileName, '&DT', '&dt', 'DT')
    dt1Feature = readTitle(FileName, '&DT_LIST', '&dt_list', 'DT_UpdateList')
    dt2Feature = readTitle(FileName, '&DT_EXIT', '&dt_exit', 'DT_ChangeExit')
    dt3Feature = readTitle(FileName, '&DT_DUMPBIN',  '&dt_dumpbin',  'DT_DumpData')
    tendFeature = readTitle(FileName, '&TEND', '&tend', 'TEND')
    
    solverFeature = readTitle(FileName, '&SOLVER', '&solver', 'solver')
    groupFeature = readTitle(FileName, '&GROUPF', '&groupf', 'groupbehavior')

    simuObjFeatures = []
    if solverFeature:
        simuObjFeatures.append(solverFeature)
    if groupFeature:
        simuObjFeatures.append(groupFeature)
    if zoomFeature:
        simuObjFeatures.append(zoomFeature)
    if xspaceFeature:
        simuObjFeatures.append(xspaceFeature)
    if yspaceFeature:
        simuObjFeatures.append(yspaceFeature)
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


def file_new(event=None):
    global agents, agent2exit, agentgroup, walls, exits, doors, exit2door
    global openFileName, currentdir
    
    agents=[['agent', 'iniX', 'iniY', 'iniVx', 'iniVy', 'timelag', 'tpre', 'p', 'pMode', 'p2', 'tpreR', 'aType', 'inC', 'range']]
    agent2exit=[['agent2exit', 'exit0', 'exit1', 'exit2', 'exit3', 'exit4', 'exit5', 'exit6']]
    agentgroup=[['agent2group', 'agent0', 'agent1', 'agent2','agent3', 'agent4', 'agent5', 'agent6']]
    walls=[['walls', 'startX', 'startY', 'endX', 'endY', 'arrow', 'shape', 'inComp']]
    exits=[['exits', 'startX', 'startY', 'endX', 'endY', 'arrow', 'shape', 'inComp']]
    doors=[['doors', 'startX', 'startY', 'endX', 'endY', 'arrow', 'shape', 'inComp']]
    exit2door=[['exit2door', 'door0', 'door1', 'door2']]
       
    treeviewA.delete(*treeviewA.get_children())    
    treeviewA2E.delete(*treeviewA2E.get_children())
    treeviewAG.delete(*treeviewAG.get_children())
    treeviewE.delete(*treeviewE.get_children())
    treeviewD.delete(*treeviewD.get_children())
    treeviewW.delete(*treeviewW.get_children())
    treeviewE2D.delete(*treeviewE2D.get_children())
    treeviewA.update()    
    treeviewA2E.update()    
    treeviewAG.update()
    treeviewE.update()    
    treeviewD.update()    
    treeviewW.update()
    treeviewE2D.update()
    
    for i in range(len(agents[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewA.heading(columns[i], text=agents[0][i])
    for i in range(1, len(agents)): #
        try:
            treeviewA.insert('', i, values=tuple(agents[i])) #[0], agents[i][1], agents[i][2], agents[i][3], agents[i][4], agents[i][5],  agents[i][6], agents[i][7], agents[i][8], agents[i][9], agents[i][10]))
        except:
            treeviewA.insert('', i, values=(i))

    for i in range(len(agent2exit[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewA2E.heading(columns[i], text=agent2exit[0][i])
    for i in range(1, len(agent2exit)): #
        try:
            treeviewA2E.insert('', i, values=tuple(agent2exit[i])) #[0], agent2exit[i][1], agent2exit[i][2], agent2exit[i][3], agent2exit[i][4], agent2exit[i][5],  agent2exit[i][6], agent2exit[i][7], agent2exit[i][8], agent2exit[i][9], agent2exit[i][10]))
        except:
            treeviewA2E.insert('', i, values=(i))

    for i in range(len(agentgroup[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewAG.heading(columns[i], text=agentgroup[0][i])
    for i in range(1, len(agentgroup)): #
        try:
            treeviewAG.insert('', i, values=tuple(agentgroup[i])) #[0], agentgroup[i][1], agentgroup[i][2], agentgroup[i][3], agentgroup[i][4], agentgroup[i][5],  agentgroup[i][6], agentgroup[i][7], agentgroup[i][8], agentgroup[i][9], agentgroup[i][10]))
        except:
            treeviewAG.insert('', i, values=(i))

    for i in range(len(walls[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewW.heading(columns[i], text=walls[0][i])
    for i in range(1, len(walls)): #
        try:
            treeviewW.insert('', i, values=tuple(walls[i])) #[0], walls[i][1], walls[i][2], walls[i][3], walls[i][4], walls[i][5],  walls[i][6], walls[i][7], walls[i][8]))
        except:
            treeviewW.insert('', i, values=(i))
            
    for i in range(len(exits[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewE.heading(columns[i], text=exits[0][i])
    for i in range(1, len(exits)): #
        try: 
            treeviewE.insert('', i, values=tuple(exits[i])) #[0], exits[i][1], exits[i][2], exits[i][3], exits[i][4], exits[i][5],  exits[i][6], exits[i][7], exits[i][8]))
        except:
            treeviewE.insert('', i, values=(i))
            
    for i in range(len(doors[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewD.heading(columns[i], text=doors[0][i])
    for i in range(1, len(doors)): #
        try: 
            treeviewD.insert('', i, values=tuple(doors[i])) #[0], doors[i][1], doors[i][2], doors[i][3], doors[i][4], doors[i][5],  doors[i][6], doors[i][7], doors[i][8]))
        except:
            treeviewD.insert('', i, values=(i))

    for i in range(len(exit2door[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewE2D.heading(columns[i], text=exit2door[0][i])
    for i in range(1, len(exit2door)): #
        try: 
            treeviewE2D.insert('', i, values=tuple(exit2door[i])) #[0], exit2door[i][1], exit2door[i][2], exit2door[i][3], exit2door[i][4], exit2door[i][5],  exit2door[i][6], exit2door[i][7], exit2door[i][8]))
        except:
            treeviewE2D.insert('', i, values=(i))
    

def file_open(event=None):
    
    global agents, agent2exit, agentgroup, walls, exits, doors, exit2door
    global openFileName, currentdir
    
    fnameCSV = tkf.askopenfilename(filetypes=(("csv files", "*.csv"),("All files", "*.*")), initialdir=currentdir) 
    #,initialdir=self.currentdir)
    #temp=self.fname_EVAC.split('/') 
    temp=os.path.basename(fnameCSV)
    currentdir = os.path.dirname(fnameCSV)
    #lb_csv.config(text = "The input csv file selected: "+str(fnameCSV)+"\n")
    #self.textInformation.insert(END, 'fname_EVAC:   '+self.fname_EVAC)
    print('fname', fnameCSV)
    #setStatusStr("Simulation not yet started!")
    #textInformation.insert(END, '\n'+'EVAC Input File Selected:   '+self.fname_EVAC+'\n')
    if fnameCSV:
        openFileName = fnameCSV
    
    file_name_label.config(text=openFileName, fg="black", bg="lightgrey", font=(None, 10))
    agents, agent2exit, agentgroup, walls, exits, doors, exit2door, simuObj = readSocialCSV(fnameCSV, debug=True, marginTitle=1)
    
    treeviewA.delete(*treeviewA.get_children())    
    treeviewA2E.delete(*treeviewA2E.get_children())
    treeviewAG.delete(*treeviewAG.get_children())
    treeviewE.delete(*treeviewE.get_children())
    treeviewD.delete(*treeviewD.get_children())
    treeviewW.delete(*treeviewW.get_children())
    treeviewE2D.delete(*treeviewE2D.get_children())
    treeviewA.update()    
    treeviewA2E.update()    
    treeviewAG.update()
    treeviewE.update()    
    treeviewD.update()    
    treeviewW.update()
    treeviewE2D.update()
    textSimu.delete(1.0, END)
    #treeviewA.column(chr(66), width=130, anchor='center')
    #treeviewA2E.column(chr(66), width=130, anchor='center')
    #treeviewAG.column(chr(66), width=130, anchor='center')

    try:
        treeviewA.heading(columns[0], text="SN")
        for i in range(len(agents[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewA.heading(columns[i+1], text=agents[0][i])
        for i in range(1, len(agents)): #
            #agents[i][0]=str(i)+"# "+agents[i][0]
            try:
                treeviewA.insert('', i, values=tuple(["#"+str(i-1)]+agents[i])) #[0], agents[i][1], agents[i][2], agents[i][3], agents[i][4], agents[i][5],  agents[i][6], agents[i][7], agents[i][8], agents[i][9], agents[i][10]))
            except:
                treeviewA.insert('', i, values=(i))
    except:
        print("No agent defined in the input csv file!")

    try:
        treeviewA2E.heading(columns[0], text="SN")
        for i in range(len(agent2exit[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewA2E.heading(columns[i+1], text=agent2exit[0][i])
        for i in range(1, len(agent2exit)): #
            #agent2exit[i][0]=str(i)+"# "+agent2exit[i][0]
            try:
                treeviewA2E.insert('', i, values=tuple(["#"+str(i-1)]+agent2exit[i])) #[0], agent2exit[i][1], agent2exit[i][2], agent2exit[i][3], agent2exit[i][4], agent2exit[i][5],  agent2exit[i][6], agent2exit[i][7], agent2exit[i][8], agent2exit[i][9], agent2exit[i][10]))
            except:
                treeviewA2E.insert('', i, values=(i))
    except:
        print("No agent2exit defined in the input csv file!")

    try:
        treeviewAG.heading(columns[0], text="SN")
        for i in range(len(agentgroup[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewAG.heading(columns[i+1], text=agentgroup[0][i])
        for i in range(1, len(agentgroup)): #
            #agentgroup[i][0]=str(i)+"# "+agentgroup[i][0]
            try:
                treeviewAG.insert('', i, values=tuple(["#"+str(i-1)]+agentgroup[i])) #[0], agentgroup[i][1], agentgroup[i][2], agentgroup[i][3], agentgroup[i][4], agentgroup[i][5],  agentgroup[i][6], agentgroup[i][7], agentgroup[i][8], agentgroup[i][9], agentgroup[i][10]))
            except:
                treeviewAG.insert('', i, values=(i))
    except:
        print("No agentgroup defined in the input csv file!")

    try:
        treeviewW.heading(columns[0], text="SN")
        for i in range(len(walls[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewW.heading(columns[i+1], text=walls[0][i])
        for i in range(1, len(walls)): #
            try:
                treeviewW.insert('', i, values=tuple(["#"+str(i-1)]+walls[i])) #[0], walls[i][1], walls[i][2], walls[i][3], walls[i][4], walls[i][5],  walls[i][6], walls[i][7], walls[i][8]))
            except:
                treeviewW.insert('', i, values=(i))
    except:
        print("No wall defined in the input csv file!")

    try:
        treeviewE.heading(columns[0], text="SN")
        for i in range(len(exits[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewE.heading(columns[i+1], text=exits[0][i])
        for i in range(1, len(exits)): #
            try: 
                treeviewE.insert('', i, values=tuple(["#"+str(i-1)]+exits[i])) #[0], exits[i][1], exits[i][2], exits[i][3], exits[i][4], exits[i][5],  exits[i][6], exits[i][7], exits[i][8]))
            except:
                treeviewE.insert('', i, values=(i))
    except:
        print("No exit defined in the input csv file!")

    try:
        treeviewD.heading(columns[0], text="SN")
        for i in range(len(doors[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewD.heading(columns[i+1], text=doors[0][i])
        for i in range(1, len(doors)): #
            try: 
                treeviewD.insert('', i, values=tuple(["#"+str(i-1)]+doors[i])) #[0], doors[i][1], doors[i][2], doors[i][3], doors[i][4], doors[i][5],  doors[i][6], doors[i][7], doors[i][8]))
            except:
                treeviewD.insert('', i, values=(i))
    except:
        print("No door defined in the input csv file!")

    try:
        treeviewE2D.heading(columns[0], text="SN")
        for i in range(len(exit2door[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewE2D.heading(columns[i+1], text=exit2door[0][i])
        for i in range(1, len(exit2door)): #
            try: 
                treeviewE2D.insert('', i, values=tuple(["#"+str(i-1)]+exit2door[i])) #[0], exit2door[i][1], exit2door[i][2], exit2door[i][3], exit2door[i][4], exit2door[i][5],  exit2door[i][6], exit2door[i][7], exit2door[i][8]))
            except:
                treeviewE2D.insert('', i, values=(i))
    except:
        print("No exit2door defined in the input csv file!")
    
    textSimu.delete(1.0, END)
    #textSimu.insert(END, 'QuickStart: \nStep1: Please select csv file file to read in agent data and compartement geometry data!\n')
    #textSimu.insert(END, 'Step2: Create simulation object!\n')       
    textSimu.insert(END, 'Files selected:'+str(openFileName)+'\n')
    for i in range(len(simuObj)):
        textSimu.insert(END, str(simuObj[i]))


def file_save(event=None):
    
    global agents, agent2exit, agentgroup, walls, exits, doors, exit2door
    global openFileName, currentdir
    
    if openFileName:
        pass
    else:
        new_file_name = tkf.asksaveasfilename(filetypes=(("csv files", "*.csv"),("All files", "*.*")), initialdir=currentdir)
        if new_file_name:
            openFileName = new_file_name
        else:
            msg.showerror("No File Saved!", "Please open a csv file first!")
            return None
    #with open(self.active_ini_filename, "w") as ini_file:
    #self.active_ini.write(ini_file)
    file_name_label.config(text=openFileName, fg="black", bg="lightgrey", font=(None, 10))
    #saveEmpty()
    
    clearCSV(openFileName, 'Initialize the csv data file.')
    saveCSV(agents, openFileName, 'Agent Data is written as below.')
    
    try:
        saveCSV(agent2exit, openFileName, 'Exit selection probilibty is written as below.')
    except:
        print("agent2exit data is not defined!")
        
    try:
        saveCSV(agentgroup, openFileName, 'Agent group data is written as below.')
    except:
        print("agentgroup data is not defined!")
        
    try:
        saveCSV(walls, openFileName, 'Wall/Obstruction data is written as below.')
    except:
        print("Wall data is not defined!")
    
    try:
        saveCSV(exits, openFileName, 'Exit/Sink data is written as below.')
    except:
        print("Exit/Sink data is not defined!")
    
    try:
        saveCSV(doors, openFileName, 'Door/Path data is written as below.')
    except:
        print("Door/Path data is not defined!")
        
    try:
        saveCSV(door2exit, openFileName, 'Door2exit data is written as below.')
    except:
        print("Door2exit data is not defined!")

    new_contents = textSimu.get(1.0, END)
    with open(openFileName, "a+") as open_file:
        open_file.write(new_contents)
        #new_contents2 = re.sub(',\t', ',', new_contents)
        #open_file.write(new_contents2)
    msg.showinfo("Saved", "File Saved Successfully")
    return 


def file_save_as(event=None):

    global agents, agent2exit, agentgroup, walls, exits, doors, exit2door
    global openFileName, currentdir

    new_file_name = tkf.asksaveasfilename(filetypes=(("csv files", "*.csv"),("All files", "*.*")), initialdir=currentdir)
    
    if new_file_name:
        openFileName = new_file_name
    else:
        msg.showerror("No File Saved", "Please input a new csv file name.")
        return None
    #with open(self.active_ini_filename, "w") as ini_file:
    #self.active_ini.write(ini_file)
    file_name_label.config(text=openFileName, fg="black", bg="lightgrey", font=(None, 10))
    #saveEmpty()
    
    clearCSV(openFileName, 'Initialize the csv data file.')
    saveCSV(agents, openFileName, 'Agent Data is written as below.')
    
    try:
        saveCSV(agent2exit, openFileName, 'Exit selection probilibty is written as below.')
    except:
        print("agent2exit data is not defined!")
        
    try:
        saveCSV(agentgroup, openFileName, 'Agent group data is written as below.')
    except:
        print("agentgroup data is not defined!")
        
    try:
        saveCSV(walls, openFileName, 'Wall/Obstruction data is written as below.')
    except:
        print("Wall data is not defined!")
    
    try:
        saveCSV(exits, openFileName, 'Exit/Sink data is written as below.')
    except:
        print("Exit/Sink data is not defined!")
    
    try:
        saveCSV(doors, openFileName, 'Door/Path data is written as below.')
    except:
        print("Door/Path data is not defined!")
        
    try:
        saveCSV(door2exit, openFileName, 'Door2exit data is written as below.')
    except:
        print("Door2exit data is not defined!")

    new_contents = textSimu.get(1.0, END)
    with open(openFileName, "a+") as open_file:
        open_file.write(new_contents)
        #new_contents2 = re.sub(',\t', ',', new_contents)
        #open_file.write(new_contents2)
    msg.showinfo("Saved", "File Saved Successfully")
    return


def clearCSV(outputFile, inputStr=''):
    try:
        with open(outputFile, mode='w', newline='') as exit_file:
            csv_writer = csv.writer(exit_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if inputStr:
                csv_writer.writerow([inputStr])
                csv_writer.writerow([])
            csv_writer.writerow([])               
    
    except:
        with open(outputFile, mode='w') as exit_file:
            csv_writer = csv.writer(exit_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if inputStr:
                csv_writer.writerow([inputStr])
                csv_writer.writerow([])
            csv_writer.writerow([])
            

def saveCSV(dataList, outputFile, inputStr=''):
    
    I=len(dataList)
    #(I, J) = np.shape(dataNP)
    #(I, J) = np.shape(exit2doors)
    #print "The size of exit2door:", [I, J]
    #dataNP = np.zeros((I+1, J+1))

    #dataNP[1:, 1:] = exit2doors
    #np.savetxt(fileName, dataNP, delimiter=',', fmt='%s')   #'2darray.csv'
    try:
        with open(outputFile, mode='a+', newline='') as exit_file:
            csv_writer = csv.writer(exit_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if inputStr:
                csv_writer.writerow([inputStr])
            for i in range(I):
                #print(dataNP[i])
                csv_writer.writerow(dataList[i])
            csv_writer.writerow([])
            csv_writer.writerow([])               
    
    except:
        with open(outputFile, mode='a+') as exit_file:
            csv_writer = csv.writer(exit_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if inputStr:
                csv_writer.writerow([inputStr])
            #csv_writer.writerow(['&Wall', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/shape', '6/inComp'])
            #index_temp=0
            for i in range(I):
                csv_writer.writerow(dataList[i])
            csv_writer.writerow([])
            csv_writer.writerow([])
            #for wall in walls:
            #    csv_writer.writerow(['--', str(wall.params[0]), str(wall.params[1]), str(wall.params[2]), str(wall.params[3]), str(wall.arrow), str(wall.mode), str(wall.inComp)])
            #    index_temp=index_temp+1

root = Tk()

file_name_var = StringVar()
file_name_label = Label(root, textvar=openFileName, fg="black", bg="lightgrey", font=(None, 12))
file_name_label.pack(side=TOP, expand=1, fill=X)

'''
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0, bg="lightgrey", fg="black")
file_menu.add_command(label="Open", command=file_open, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=file_save, accelerator="Ctrl+S")
menubar.add_cascade(label="File", menu=file_menu)

add_menu = Menu(menubar, tearoff=0, bg="lightgrey", fg="black")
add_menu.add_command(label="Add Item", command=newrow, accelerator="Ctrl+O")
menubar.add_cascade(label="Add", menu=add_menu)

delete_menu = Menu(menubar, tearoff=0, bg="lightgrey", fg="black")
delete_menu.add_command(label="Delete Item", command=file_open, accelerator="Ctrl+O")
menubar.add_cascade(label="Delete", menu=delete_menu)
'''

notebook = Notebook(root,  width=45, height=300)      
notebook.pack(side=TOP, padx=2, pady=2)

frameSimuObj = Frame(root)
frameAgent = Frame(root)
frameAgent2Exit = Frame(root)
frameAgentGroup = Frame(root)
frameWall = Frame(root)
frameExit = Frame(root)
frameDoor = Frame(root)
frameExit2Door = Frame(root)

notebook.add(frameSimuObj,text="  <SimuObj>  ")
notebook.add(frameAgent,text="  <AgentFeatures>  ")
notebook.add(frameAgent2Exit,text="  <AgentExitProb>  ")
notebook.add(frameAgentGroup,text="  <AgentGroup>  ")
notebook.add(frameWall,text="  <Wall/Obstruction>  ")
notebook.add(frameExit,text="  <Exit/SinkPoint>  ")
notebook.add(frameDoor,text="  <Door/Passage/WayPoint>  ")
notebook.add(frameExit2Door,text="  <Exit2DoorArray>  ")


#left_frame = Frame(root, width=200, height=600, bg="grey")
#left_frame.pack_propagate(0)
        
#right_frame = Frame(root, width=400, height=600, bg="lightgrey")
#right_frame.pack_propagate(0)

#columns = ("agent", "iniPosX", "iniPosY", "iniVx", "iniVy", "timelag", "tpre", "p", "pMode", "p2", "talkRange", "aType", "inComp", "tpreMode")
#columns = tuple(np.arange(1, 100))

col_list=[]
for i in range(26):
    col_list.append(chr(i+65))
print(col_list)
columns = tuple(col_list)

scrollbarAy = Scrollbar(frameAgent, orient="vertical") #, orient="vertical", command=treeview.yview)
scrollbarAy.pack(side=RIGHT, fill=Y)

scrollbarAx = Scrollbar(frameAgent, orient="horizontal") #, orient="vertical", command=treeview.yview)
scrollbarAx.pack(side=BOTTOM, fill=X)

treeviewA = Treeview(frameAgent, height=18, show="headings", columns=columns)  #Table
scrollbarAy.config(command=treeviewA.yview)
scrollbarAx.config(command=treeviewA.xview)

for i in range(26):
    treeviewA.column(chr(i+65), width=70, anchor='center')
treeviewA.pack(side=LEFT, fill=BOTH)

scrollbarA2Ey = Scrollbar(frameAgent2Exit, orient="vertical") #, orient="vertical", command=treeview.yview)
scrollbarA2Ey.pack(side=RIGHT, fill=Y)

scrollbarA2Ex = Scrollbar(frameAgent2Exit, orient="horizontal") #, orient="vertical", command=treeview.yview)
scrollbarA2Ex.pack(side=BOTTOM, fill=X)

treeviewA2E = Treeview(frameAgent2Exit, height=18, show="headings", columns=columns)  #Table
scrollbarA2Ey.config(command=treeviewA2E.yview)
scrollbarA2Ex.config(command=treeviewA2E.xview)

for i in range(26):
    treeviewA2E.column(chr(i+65), width=70, anchor='center')
treeviewA2E.pack(side=LEFT, fill=BOTH)

scrollbarAGy = Scrollbar(frameAgentGroup, orient="vertical") #, orient="vertical", command=treeview.yview)
scrollbarAGy.pack(side=RIGHT, fill=Y)

scrollbarAGx = Scrollbar(frameAgentGroup, orient="horizontal") #, orient="vertical", command=treeview.yview)
scrollbarAGx.pack(side=BOTTOM, fill=X)

treeviewAG = Treeview(frameAgentGroup, height=18, show="headings", columns=columns)  #Table
scrollbarAGy.config(command=treeviewAG.yview)
scrollbarAGx.config(command=treeviewAG.xview)

for i in range(26):
    treeviewAG.column(chr(i+65), width=70, anchor='center')
treeviewAG.pack(side=LEFT, fill=BOTH)


scrollbarWy = Scrollbar(frameWall, orient="vertical") #, orient="vertical", command=treeview.yview)
scrollbarWy.pack(side=RIGHT, fill=Y)

scrollbarWx = Scrollbar(frameWall, orient="horizontal") #, orient="vertical", command=treeview.yview)
scrollbarWx.pack(side=BOTTOM, fill=X)

treeviewW = Treeview(frameWall, height=18, show="headings", columns=columns)  #Table
scrollbarWy.config(command=treeviewW.yview)
scrollbarWx.config(command=treeviewW.xview)

for i in range(26):
    treeviewW.column(chr(i+65), width=70, anchor='center')
treeviewW.pack(side=LEFT, fill=BOTH)

### Frame of Exit
scrollbarEy = Scrollbar(frameExit, orient="vertical") #, orient="vertical", command=treeview.yview)
scrollbarEy.pack(side=RIGHT, fill=Y)

scrollbarEx = Scrollbar(frameExit, orient="horizontal") #, orient="vertical", command=treeview.yview)
scrollbarEx.pack(side=BOTTOM, fill=X)

treeviewE = Treeview(frameExit, height=18, show="headings", columns=columns)  #Table
scrollbarEy.config(command=treeviewE.yview)
scrollbarEx.config(command=treeviewE.xview)

for i in range(26):
    treeviewE.column(chr(i+65), width=70, anchor='center')
treeviewE.pack(side=LEFT, fill=BOTH)

### Frame of Exit
scrollbarDy = Scrollbar(frameDoor, orient="vertical") #, orient="vertical", command=treeview.yview)
scrollbarDy.pack(side=RIGHT, fill=Y)

scrollbarDx = Scrollbar(frameDoor, orient="horizontal") #, orient="vertical", command=treeview.yview)
scrollbarDx.pack(side=BOTTOM, fill=X)

treeviewD = Treeview(frameDoor, height=18, show="headings", columns=columns)  #Table
scrollbarDy.config(command=treeviewD.yview)
scrollbarDx.config(command=treeviewD.xview)

for i in range(26):
    treeviewD.column(chr(i+65), width=70, anchor='center')
treeviewD.pack(side=LEFT, fill=BOTH)

### Frame of Exit2Door
scrollbarE2Dy = Scrollbar(frameExit2Door, orient="vertical") #, orient="vertical", command=treeview.yview)
scrollbarE2Dy.pack(side=RIGHT, fill=Y)

scrollbarE2Dx = Scrollbar(frameExit2Door, orient="horizontal") #, orient="vertical", command=treeview.yview)
scrollbarE2Dx.pack(side=BOTTOM, fill=X)

treeviewE2D = Treeview(frameExit2Door, height=18, show="headings", columns=columns)  #Table
scrollbarE2Dy.config(command=treeviewE2D.yview)
scrollbarE2Dx.config(command=treeviewE2D.xview)

for i in range(26):
    treeviewE2D.column(chr(i+65), width=70, anchor='center')
treeviewE2D.pack(side=LEFT, fill=BOTH)

scrollbarSimuy = Scrollbar(frameSimuObj, orient="vertical") #, orient="vertical", command=treeview.yview)
scrollbarSimuy.pack(side=RIGHT, fill=Y)

scrollbarSimux = Scrollbar(frameSimuObj, orient="horizontal") #, orient="vertical", command=treeview.yview)
scrollbarSimux.pack(side=BOTTOM, fill=X)

textSimu = Text(frameSimuObj, bg="white", fg="black", font=("Times", 13))
scrollbarSimuy.config(command=textSimu.yview)
scrollbarSimux.config(command=textSimu.xview)
textSimu.pack(expand=1, fill=BOTH)

def treeview_sort_column(tv, col, reverse):  # Treeview

    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)  # sort method
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))  # 


def set_cell_value_A(event): # double click to edit the item
    
    global agents
    for item in treeviewA.selection():

        #item = I001
        item_text = treeviewA.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users

    column= treeviewA.identify_column(event.x)# column
    row = treeviewA.identify_row(event.y)  # row

    cn = int(str(column).replace('#',''))
    rn = int(str(row).replace('I',''), base=16)
    temp = item_text[0].split(" ")
    rn = int(temp[0].strip("#"))
    
    print("cn:", cn)
    print("rn:", rn)

    #entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    entryedit = Text(root, width=56, height = 2)
    #entryedit = Entry(root,width=10)
    entryedit.insert(END, str(item_text[0])+'|'+str(item_text[1])+'|'+agents[0][cn-2]+' = '+str(item_text[cn-1]))
    #entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    entryedit.pack()
    #lb= Label(root, text = str(rn)+columns[cn-1])
    #lb.pack()

    def saveedit():

        global agents
        try:
            temp=entryedit.get(0.0, 'end').split('=')
            treeviewA.set(item, column=column, value=temp[1].strip())
            agents[rn+1][cn-2]=temp[1].strip()
            print(agents) #[rn, cn])
        except:
            treeviewA.set(item, column=column, value=entryedit.get(0.0, 'end').strip())
            agents[rn+1][cn-2]=entryedit.get(0.0, 'end').strip()
            print(agents) #[rn, cn])
            
        #treeviewA.set(item, column=column, value=entryedit.get(0.0, "end"))
        #agents[rn-1][cn-2]=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = Button(root, text=str(item_text[0])+'|'+str(item_text[1])+'|'+agents[0][cn-2]+': <Save Changes>', width=56, command=saveedit)
    okb.pack() #place(x=90+(cn-1)*242,y=2+rn*20)


def set_cell_value_A2E(event):
    global agent2exit
    for item in treeviewA2E.selection():

        #item = I001
        item_text = treeviewA2E.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users

    column= treeviewA2E.identify_column(event.x)# column
    row = treeviewA2E.identify_row(event.y)  # row

    cn = int(str(column).replace('#',''))
    rn = int(str(row).replace('I',''), base=16)
    temp = item_text[0].split(" ")
    rn = int(temp[0].strip("#"))
    
    print("cn:", cn)
    print("rn:", rn)

    #entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    entryedit = Text(root, width=56, height = 2)
    #entryedit = Entry(root,width=10)
    entryedit.insert(END, str(item_text[0])+'|'+str(item_text[1])+'|'+agent2exit[0][cn-2]+' = '+str(item_text[cn-1]))
    #entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    entryedit.pack()

    def saveedit():

        global agent2exit
        try:
            temp=entryedit.get(0.0, 'end').split('=')
            treeviewA2E.set(item, column=column, value=temp[1].strip())
            agent2exit[rn+1][cn-2]=temp[1].strip()
            print(agent2exit) #[rn, cn])
        except:
            treeviewA2E.set(item, column=column, value=entryedit.get(0.0, 'end').strip())
            agent2exit[rn+1][cn-2]=entryedit.get(0.0, 'end').strip()
            print(agent2exit) #[rn, cn])
            
        #treeviewA.set(item, column=column, value=entryedit.get(0.0, "end"))
        #agents[rn-1][cn-2]=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = Button(root, text=str(item_text[0])+'|'+str(item_text[1])+'|'+agent2exit[0][cn-2]+': <Save Changes>', width=56, command=saveedit)
    okb.pack() #place(x=90+(cn-1)*242,y=2+rn*20)
    

def set_cell_value_AG(event):
    global agentgroup
    for item in treeviewAG.selection():

        #item = I001
        item_text = treeviewAG.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users

    column= treeviewAG.identify_column(event.x)# column
    row = treeviewAG.identify_row(event.y)  # row

    cn = int(str(column).replace('#',''))
    rn = int(str(row).replace('I',''), base=16)
    temp = item_text[0].split(" ")
    rn = int(temp[0].strip("#"))
    
    print("cn:", cn)
    print("rn:", rn)

    #entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    entryedit = Text(root, width=56, height = 2)
    #entryedit = Entry(root,width=10)
    entryedit.insert(END, str(item_text[0])+'|'+str(item_text[1])+'|'+agentgroup[0][cn-2]+' = '+str(item_text[cn-1]))
    #entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    entryedit.pack()

    def saveedit():

        global agentgroup
        try:
            temp=entryedit.get(0.0, 'end').split('=')
            treeviewAG.set(item, column=column, value=temp[1].strip())
            agentgroup[rn+1][cn-2]=temp[1].strip()
            print(agentgroup) #[rn, cn])
        except:
            treeviewAG.set(item, column=column, value=entryedit.get(0.0, 'end').strip())
            agentgroup[rn+1][cn-2]=entryedit.get(0.0, 'end').strip()
            print(agentgroup) #[rn, cn])
            
        #treeviewA.set(item, column=column, value=entryedit.get(0.0, "end"))
        #agents[rn-1][cn-2]=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = Button(root, text=str(item_text[0])+'|'+str(item_text[1])+'|'+agentgroup[0][cn-2]+': <Save Changes>', width=56, command=saveedit)
    okb.pack() #place(x=90+(cn-1)*242,y=2+rn*20)

def set_cell_value_W(event):
    
    global walls
    for item in treeviewW.selection():

        #item = I001
        item_text = treeviewW.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users

    column= treeviewW.identify_column(event.x)# column
    row = treeviewW.identify_row(event.y)  # row

    cn = int(str(column).replace('#',''))
    rn = int(str(row).replace('I',''), base=16)
    temp = item_text[0].split(" ")
    rn = int(temp[0].strip("#"))
    
    print("cn:", cn)
    print("rn:", rn)

    #entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    entryedit = Text(root, width=56, height = 2)
    #entryedit = Entry(root,width=10)
    entryedit.insert(END, str(item_text[0])+'|'+str(item_text[1])+'|'+walls[0][cn-2]+' = '+str(item_text[cn-1]))
    #entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    entryedit.pack()

    def saveedit():

        global walls
        try:
            temp=entryedit.get(0.0, 'end').split('=')
            treeviewW.set(item, column=column, value=temp[1].strip())
            walls[rn+1][cn-2]=temp[1].strip()
            print(walls) #[rn, cn])
        except:
            treeviewW.set(item, column=column, value=entryedit.get(0.0, 'end').strip())
            walls[rn+1][cn-2]=entryedit.get(0.0, 'end').strip()
            print(walls) #[rn, cn])
            
        #treeviewA.set(item, column=column, value=entryedit.get(0.0, "end"))
        #agents[rn-1][cn-2]=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = Button(root, text=str(item_text[0])+'|'+str(item_text[1])+'|'+walls[0][cn-2]+': <Save Changes>', width=56, command=saveedit)
    okb.pack() #place(x=90+(cn-1)*242,y=2+rn*20)
    

def set_cell_value_D(event):
    
    global doors
    for item in treeviewD.selection():

        #item = I001
        item_text = treeviewD.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users

    column= treeviewD.identify_column(event.x)# column
    row = treeviewD.identify_row(event.y)  # row

    cn = int(str(column).replace('#',''))
    rn = int(str(row).replace('I',''), base=16)
    temp = item_text[0].split(" ")
    rn = int(temp[0].strip("#"))
    
    print("cn:", cn)
    print("rn:", rn)

    #entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    entryedit = Text(root, width=56, height = 2)
    #entryedit = Entry(root,width=10)
    entryedit.insert(END, str(item_text[0])+'|'+str(item_text[1])+'|'+doors[0][cn-2]+' = '+str(item_text[cn-1]))
    #entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    entryedit.pack()

    def saveedit():

        global doors
        try:
            temp=entryedit.get(0.0, 'end').split('=')
            treeviewD.set(item, column=column, value=temp[1].strip())
            doors[rn+1][cn-2]=temp[1].strip()
            print(doors) #[rn, cn])
        except:
            treeviewD.set(item, column=column, value=entryedit.get(0.0, 'end').strip())
            doors[rn+1][cn-2]=entryedit.get(0.0, 'end').strip()
            print(doors) #[rn, cn])
            
        #treeviewA.set(item, column=column, value=entryedit.get(0.0, "end"))
        #agents[rn-1][cn-2]=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = Button(root, text=str(item_text[0])+'|'+str(item_text[1])+'|'+doors[0][cn-2]+': <Save Changes>', width=56, command=saveedit)
    okb.pack() #place(x=90+(cn-1)*242,y=2+rn*20)


def set_cell_value_E(event):

    global exits
    for item in treeviewE.selection():

        #item = I001
        item_text = treeviewE.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users

    column= treeviewE.identify_column(event.x)# column
    row = treeviewE.identify_row(event.y)  # row

    cn = int(str(column).replace('#',''))
    rn = int(str(row).replace('I',''), base=16)
    temp = item_text[0].split(" ")
    rn = int(temp[0].strip("#"))
    
    print("cn:", cn)
    print("rn:", rn)

    #entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    entryedit = Text(root, width=56, height = 2)
    #entryedit = Entry(root,width=10)
    entryedit.insert(END, str(item_text[0])+'|'+str(item_text[1])+'|'+exits[0][cn-2]+' = '+str(item_text[cn-1]))
    #entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    entryedit.pack()

    def saveedit():

        global exits
        try:
            temp=entryedit.get(0.0, 'end').split('=')
            treeviewE.set(item, column=column, value=temp[1].strip())
            exits[rn+1][cn-2]=temp[1].strip()
            print(exits) #[rn, cn])
        except:
            treeviewE.set(item, column=column, value=entryedit.get(0.0, 'end').strip())
            exits[rn+1][cn-2]=entryedit.get(0.0, 'end').strip()
            print(exits) #[rn, cn])
            
        #treeviewA.set(item, column=column, value=entryedit.get(0.0, "end"))
        #agents[rn-1][cn-2]=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = Button(root, text=str(item_text[0])+'|'+str(item_text[1])+'|'+exits[0][cn-2]+': <Save Changes>', width=56, command=saveedit)
    okb.pack() #place(x=90+(cn-1)*242,y=2+rn*20)


def add_agent(event=None):
    global agents, agent2exit, agentgroup
    rn=None
    for item in treeviewA.selection():
        #item = I001
        item_text = treeviewA.item(item, "values")
        temp = item_text[0].split(" ")
        rn = int(temp[0].strip("#"))

    if rn is None:
        for item in treeviewA2E.selection():
            #item = I001
            item_text = treeviewA2E.item(item, "values")
            temp = item_text[0].split(" ")
            rn = int(temp[0].strip("#"))
    if rn is None:
        for item in treeviewAG.selection():
            #item = I001
            item_text = treeviewAG.item(item, "values")
            temp = item_text[0].split(" ")
            rn = int(temp[0].strip("#"))

    print("rn:", rn)
    #try:
    #    agents.insert(rn+2, agents[rn+1])
    #    if bool(agent2exit):
    #        agent2exit.insert(rn+2, agent2exit[rn+1])
    #    if bool(agentgroup):
    #        agentgroup.insert(rn+2, agentgroup[rn+1])
    #except:
    
    agents.append(agents[-1])
    if bool(agent2exit):
        agent2exit.append(agent2exit[-1])
    if bool(agentgroup):
        agentgroup.append(agentgroup[-1])
    
    if bool(agentgroup):
        num_agents=len(agents)
        agentgroup2=list(agentgroup) #.copy()
        print("num_agents", num_agents)
        #if bool(rn):
        #    for i in range(num_agents):
        #        agentgroup2[i].insert(rn+2, '0')
        #else:
        for i in range(num_agents):
            agentgroup2[i].insert(num_agents-1, '0')
        for i in range(num_agents):
            agentgroup[i]=agentgroup2[i][:num_agents]
        
        print(len(agentgroup)) #, np.shape(np.array(agentgroup)))
        print(agentgroup)
    

    treeviewA.delete(*treeviewA.get_children())    
    treeviewA2E.delete(*treeviewA2E.get_children())
    treeviewAG.delete(*treeviewAG.get_children())
    treeviewA.update()    
    treeviewA2E.update()    
    treeviewAG.update()
    
    treeviewA.heading(columns[0], text="SN")
    for i in range(len(agents[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewA.heading(columns[i+1], text=agents[0][i])
    for i in range(1, len(agents)): #
        #agents[i][0]=str(i)+"# "+agents[i][0]
        try:
            treeviewA.insert('', i, values=tuple(["#"+str(i-1)]+agents[i])) #[0], agents[i][1], agents[i][2], agents[i][3], agents[i][4], agents[i][5],  agents[i][6], agents[i][7], agents[i][8], agents[i][9], agents[i][10]))
        except:
            treeviewA.insert('', i, values=(i))

    if bool(agent2exit):
        treeviewA2E.heading(columns[0], text="SN")
        for i in range(len(agent2exit[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewA2E.heading(columns[i+1], text=agent2exit[0][i])
        for i in range(1, len(agent2exit)): #
            #agent2exit[i][0]=str(i)+"# "+agent2exit[i][0]
            try:
                treeviewA2E.insert('', i, values=tuple(["#"+str(i-1)]+agent2exit[i])) #[0], agent2exit[i][1], agent2exit[i][2], agent2exit[i][3], agent2exit[i][4], agent2exit[i][5],  agent2exit[i][6], agent2exit[i][7], agent2exit[i][8], agent2exit[i][9], agent2exit[i][10]))
            except:
                treeviewA2E.insert('', i, values=(i))

    if bool(agentgroup):
        treeviewAG.heading(columns[0], text="SN")
        for i in range(len(agentgroup[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewAG.heading(columns[i+1], text=agentgroup[0][i])
        for i in range(1, len(agentgroup)): #
            #agentgroup[i][0]=str(i)+"# "+agentgroup[i][0]
            try:
                treeviewAG.insert('', i, values=tuple(["#"+str(i-1)]+agentgroup[i])) #[0], agentgroup[i][1], agentgroup[i][2], agentgroup[i][3], agentgroup[i][4], agentgroup[i][5],  agentgroup[i][6], agentgroup[i][7], agentgroup[i][8], agentgroup[i][9], agentgroup[i][10]))
            except:
                treeviewAG.insert('', i, values=(i))
            

def del_agent(event=None):
    
    global agents, agent2exit, agentgroup
    rn=None
    for item in treeviewA.selection():
        #item = I001
        item_text = treeviewA.item(item, "values")
        temp = item_text[0].split(" ")
        rn = int(temp[0].strip("#"))
        
    if rn is None:
        for item in treeviewA2E.selection():
            #item = I001
            item_text = treeviewA2E.item(item, "values")
            temp = item_text[0].split(" ")
            rn = int(temp[0].strip("#"))
    if rn is None:
        for item in treeviewAG.selection():
            #item = I001
            item_text = treeviewAG.item(item, "values")
            temp = item_text[0].split(" ")
            rn = int(temp[0].strip("#"))
        
    #column= treeviewA.identify_column(event.x)# column
    #row = treeviewA.identify_row(event.y)  # row
    #cn = int(str(column).replace('#',''))
    #rn = int(str(row).replace('I',''), base=16)

    print("rn:", rn)
    
    del agents[rn+1]
    if bool(agent2exit):
        del agent2exit[rn+1]
    if bool(agentgroup):
        del agentgroup[rn+1]
    
    for i in range(len(agents)):
        del agentgroup[i][rn+1]

    treeviewA.delete(*treeviewA.get_children())    
    treeviewA2E.delete(*treeviewA2E.get_children())
    treeviewAG.delete(*treeviewAG.get_children())
    treeviewA.update()    
    treeviewA2E.update()    
    treeviewAG.update()

    treeviewA.heading(columns[0], text="SN")
    for i in range(len(agents[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
        treeviewA.heading(columns[i+1], text=agents[0][i])
    for i in range(1, len(agents)): #
        #agents[i][0]=str(i)+"# "+agents[i][0]
        try:
            treeviewA.insert('', i, values=tuple(["#"+str(i-1)]+agents[i])) #[0], agents[i][1], agents[i][2], agents[i][3], agents[i][4], agents[i][5],  agents[i][6], agents[i][7], agents[i][8], agents[i][9], agents[i][10]))
        except:
            treeviewA.insert('', i, values=(i))
    
    if bool(agent2exit):
        treeviewA2E.heading(columns[0], text="SN")
        for i in range(len(agent2exit[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewA2E.heading(columns[i+1], text=agent2exit[0][i])
        for i in range(1, len(agent2exit)): #
            #agent2exit[i][0]=str(i)+"# "+agent2exit[i][0]
            try:
                treeviewA2E.insert('', i, values=tuple(["#"+str(i-1)]+agent2exit[i])) #[0], agent2exit[i][1], agent2exit[i][2], agent2exit[i][3], agent2exit[i][4], agent2exit[i][5],  agent2exit[i][6], agent2exit[i][7], agent2exit[i][8], agent2exit[i][9], agent2exit[i][10]))
            except:
                treeviewA2E.insert('', i, values=(i))
                
    if bool(agentgroup):
        treeviewAG.heading(columns[0], text="SN")
        for i in range(len(agentgroup[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewAG.heading(columns[i+1], text=agentgroup[0][i])
        for i in range(1, len(agentgroup)): #
            #agentgroup[i][0]=str(i)+"# "+agentgroup[i][0]
            try:
                treeviewAG.insert('', i, values=tuple(["#"+str(i-1)]+agentgroup[i])) #[0], agentgroup[i][1], agentgroup[i][2], agentgroup[i][3], agentgroup[i][4], agentgroup[i][5],  agentgroup[i][6], agentgroup[i][7], agentgroup[i][8], agentgroup[i][9], agentgroup[i][10]))
            except:
                treeviewAG.insert('', i, values=(i))


def add_wall(event=None):
    global walls
    rn=None
    for item in treeviewW.selection():
        #item = I001
        item_text = treeviewW.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users
        temp = item_text[0].split(" ")
        rn = int(temp[0].strip("#"))
        
    print("rn:", rn)

    if bool(walls):
        #try:
        #    walls.insert(rn+2, walls[rn+1])
        #except:
        walls.append(walls[-1])
        
        #num_walls=len(walls)
        treeviewW.delete(*treeviewW.get_children())    
        treeviewW.update()    
        treeviewW.heading(columns[0], text="SN")
        for i in range(len(walls[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewW.heading(columns[i+1], text=walls[0][i])
        for i in range(1, len(walls)): #
            try:
                treeviewW.insert('', i, values=tuple(["#"+str(i-1)]+walls[i])) #[0], agents[i][1], agents[i][2], 
            except:
                treeviewW.insert('', i, values=(i))
                
def del_wall(event=None):
    global walls
    for item in treeviewW.selection():
        #item = I001
        item_text = treeviewW.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users

    temp = item_text[0].split(" ")
    rn = int(temp[0].strip("#"))
    
    print("rn:", rn)
    if bool(walls):
        del walls[rn+1]
        
        treeviewW.delete(*treeviewW.get_children())    
        treeviewW.update()    
        treeviewW.heading(columns[0], text="SN")
        for i in range(len(walls[0])): #np.shape(arr1D_2D(walls))[1])
            treeviewW.heading(columns[i+1], text=walls[0][i])
        for i in range(1, len(walls)): #
            #walls[i][0]=str(i)+"# "+walls[i][0]
            try:
                treeviewW.insert('', i, values=tuple(["#"+str(i-1)]+walls[i]))
            except:
                treeviewW.insert('', i, values=(i))

def add_door(event=None):
    global doors, exit2door
    rn=None
    for item in treeviewD.selection():
        item_text = treeviewD.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users
        temp = item_text[0].split(" ")
        rn = int(temp[0].strip("#"))

    print("rn:", rn)
    
    if bool(doors):
        #try:
        #    doors.insert(rn+2, doors[rn+1])
        #except:
        doors.append(doors[-1])
            
    if bool(exit2door):
        num_doors=len(doors)
        num_exits=len(exits)
        exit2door2=exit2door #list(exit2door) #.copy()
        print("num_doors", num_doors)
        #agentgroup_new = agentgroup
        #if bool(rn):
        #    for i in range(num_exits):
        #        exit2door2[i].insert(rn+2, '0')
        #else:
        for i in range(num_exits):
            exit2door2[i].insert(num_doors-1, '0')
        
        for i in range(num_exits):
            exit2door[i]=exit2door2[i][:num_doors]
        
        print(len(exit2door)) #, np.shape(np.array(agentgroup)))
        print(exit2door)
        
    if bool(doors):
        treeviewD.delete(*treeviewD.get_children())    
        treeviewD.update()    
        treeviewD.heading(columns[0], text="SN")
        
        for i in range(len(doors[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewD.heading(columns[i+1], text=doors[0][i])
        for i in range(1, len(doors)): #
            #agents[i][0]=str(i)+"# "+agents[i][0]
            try:
                treeviewD.insert('', i, values=tuple(["#"+str(i-1)]+doors[i])) #[0], agents[i][1], agents[i][2], 
            except:
                treeviewD.insert('', i, values=(i))

    if bool(exit2door):
        treeviewE2D.delete(*treeviewE2D.get_children())
        treeviewE2D.update()    
        treeviewE2D.heading(columns[0], text="SN")
        for i in range(len(exit2door[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewE2D.heading(columns[i+1], text=exit2door[0][i])
        for i in range(1, len(exit2door)): #
            #exit2door[i][0]=str(i)+"# "+exit2door[i][0]
            try:
                treeviewE2D.insert('', i, values=tuple(["#"+str(i-1)]+exit2door[i]))
            except:
                treeviewE2D.insert('', i, values=(i))
                

def del_door(event=None):
    global doors, exit2door
    rn=None
    for item in treeviewD.selection():
        #item = I001
        item_text = treeviewD.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users    
        temp = item_text[0].split(" ")
        rn = int(temp[0].strip("#"))
    
    print("rn:", rn)
    if bool(doors):
        del doors[rn+1]
    
    if bool(exit2door):
        for i in range(len(exits)):
            del exit2door[i][rn+1]

    if bool(doors):
        treeviewD.delete(*treeviewD.get_children())    
        treeviewD.update()    
        treeviewD.heading(columns[0], text="SN")
        for i in range(len(doors[0])): #np.shape(arr1D_2D(doors))[1]):  # bind function: enable sorting in table headings
            treeviewD.heading(columns[i+1], text=doors[0][i])
        for i in range(1, len(doors)): #
            #doors[i][0]=str(i)+"# "+doors[i][0]
            try:
                treeviewD.insert('', i, values=tuple(["#"+str(i-1)]+doors[i]))
            except:
                treeviewD.insert('', i, values=(i))
    
    if bool(exit2door):
        treeviewE2D.delete(*treeviewE2D.get_children())
        treeviewE2D.update()    
        treeviewE2D.heading(columns[0], text="SN")
        for i in range(len(exit2door[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewE2D.heading(columns[i+1], text=exit2door[0][i])
        for i in range(1, len(exit2door)): #
            #exit2door[i][0]=str(i)+"# "+exit2door[i][0]
            try:
                treeviewE2D.insert('', i, values=tuple(["#"+str(i-1)]+exit2door[i]))
            except:
                treeviewE2D.insert('', i, values=(i))
                

def add_exit(event=None):
    global exits, exit2door
    rn=None
    for item in treeviewE.selection():
        item_text = treeviewE.item(item, "values")
        #print(item_text[0:2])  # Output the column number selected by users
        temp = item_text[0].split(" ")
        rn = int(temp[0].strip("#"))

    print("rn:", rn)
    
    if bool(exits):
        #try:
        #    exits.insert(rn+2, exits[rn+1])
        #except:
        exits.append(exits[-1])

    if bool(agent2exit):
        
        num_agents=len(agents)
        num_exits=len(exits)
        agent2exit2=agent2exit #list(exit2door) #.copy()
        print("num_exits", num_exits)
        
        for i in range(num_agents):
            agent2exit2[i].insert(num_exits-1, '0')
        
        for i in range(num_agents):
            agent2exit[i]=agent2exit2[i][:num_exits]
        
        print(len(agent2exit)) #, np.shape(np.array(agentgroup)))
        print(agent2exit)

    if bool(exit2door):
        #try:
        #    exit2door.insert(rn+2, exit2door[rn+1])
        #except:
        exit2door.append(exit2door[-1])

    if bool(exits):
        #num_walls=len(walls)
        treeviewE.delete(*treeviewE.get_children())    
        treeviewE.update()    
        treeviewE.heading(columns[0], text="SN")
        for i in range(len(exits[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewE.heading(columns[i+1], text=exits[0][i])
        for i in range(1, len(exits)): #
            #agents[i][0]=str(i)+"# "+agents[i][0]
            try:
                treeviewE.insert('', i, values=tuple(["#"+str(i-1)]+exits[i])) #[0], agents[i][1], agents[i][2], 
            except:
                treeviewE.insert('', i, values=(i))

    if bool(agent2exit):
        treeviewA2E.delete(*treeviewA2E.get_children())
        treeviewA2E.update() 
        treeviewA2E.heading(columns[0], text="SN")
        for i in range(len(agent2exit[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewA2E.heading(columns[i+1], text=agent2exit[0][i])
        for i in range(1, len(agent2exit)): #
            #agent2exit[i][0]=str(i)+"# "+agent2exit[i][0]
            try:
                treeviewA2E.insert('', i, values=tuple(["#"+str(i-1)]+agent2exit[i])) #[0], agent2exit[i][1], agent2exit[i][2], agent2exit[i][3], agent2exit[i][4], agent2exit[i][5],  agent2exit[i][6], agent2exit[i][7], agent2exit[i][8], agent2exit[i][9], agent2exit[i][10]))
            except:
                treeviewA2E.insert('', i, values=(i))

    if bool(exit2door):
        treeviewE2D.delete(*treeviewE2D.get_children())
        treeviewE2D.update() 
        treeviewE2D.heading(columns[0], text="SN")
        for i in range(len(exit2door[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewE2D.heading(columns[i+1], text=exit2door[0][i])
        for i in range(1, len(exit2door)): #
            #exit2door[i][0]=str(i)+"# "+exit2door[i][0]
            try:
                treeviewE2D.insert('', i, values=tuple(["#"+str(i-1)]+exit2door[i]))
            except:
                treeviewE2D.insert('', i, values=(i))


def del_exit(event=None):
    global exits, exit2door
    try:
        for item in treeviewE.selection():
            #item = I001
            item_text = treeviewE.item(item, "values")
            #print(item_text[0:2])  # Output the column number selected by users
    except:
        for item in treeviewE2D.selection():
            #item = I001
            item_text = treeviewE2D.item(item, "values")
            #print(item_text[0:2])  # Output the column number selected by users
            
    temp = item_text[0].split(" ")
    rn = int(temp[0].strip("#"))
    
    #print("cn:", cn)
    print("rn:", rn)
    
    if bool(exits):
        del exits[rn+1]
        
    if bool(agent2exit):
        for i in range(len(agents)):
            del agent2exit[i][rn+1]
            
    if bool(exit2door):
        del exit2door[rn+1]

    if bool(exits):
        treeviewE.delete(*treeviewE.get_children())    
        treeviewE.update()    
        treeviewE.heading(columns[0], text="SN")
        for i in range(len(exits[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewE.heading(columns[i+1], text=exits[0][i])
        for i in range(1, len(exits)): #
            #agents[i][0]=str(i)+"# "+agents[i][0]
            try:
                treeviewE.insert('', i, values=tuple(["#"+str(i-1)]+exits[i])) #[0], agents[i][1], agents[i][2], agents[i][3], agents[i][4], agents[i][5],  agents[i][6], agents[i][7], agents[i][8], agents[i][9], agents[i][10]))
            except:
                treeviewE.insert('', i, values=(i))

    if bool(agent2exit):
        treeviewA2E.delete(*treeviewA2E.get_children())
        treeviewA2E.update() 
        treeviewA2E.heading(columns[0], text="SN")
        for i in range(len(agent2exit[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewA2E.heading(columns[i+1], text=agent2exit[0][i])
        for i in range(1, len(agent2exit)): #
            #agent2exit[i][0]=str(i)+"# "+agent2exit[i][0]
            try:
                treeviewA2E.insert('', i, values=tuple(["#"+str(i-1)]+agent2exit[i])) #[0], agent2exit[i][1], agent2exit[i][2], agent2exit[i][3], agent2exit[i][4], agent2exit[i][5],  agent2exit[i][6], agent2exit[i][7], agent2exit[i][8], agent2exit[i][9], agent2exit[i][10]))
            except:
                treeviewA2E.insert('', i, values=(i))

    if bool(exit2door):
        treeviewE2D.delete(*treeviewE2D.get_children())
        treeviewE2D.update() 
        treeviewE2D.heading(columns[0], text="SN")
        for i in range(len(exit2door[0])): #np.shape(arr1D_2D(agents))[1]):  # bind function: enable sorting in table headings
            treeviewE2D.heading(columns[i+1], text=exit2door[0][i])
        for i in range(1, len(exit2door)): #
            #exit2door[i][0]=str(i)+"# "+exit2door[i][0]
            try:
                treeviewE2D.insert('', i, values=tuple(["#"+str(i-1)]+exit2door[i]))
            except:
                treeviewE2D.insert('', i, values=(i))


treeviewA.bind('<Double-1>', set_cell_value_A) # Double click to edit items
treeviewA2E.bind('<Double-1>', set_cell_value_A2E) 
treeviewAG.bind('<Double-1>', set_cell_value_AG) 
treeviewW.bind('<Double-1>', set_cell_value_W) 
treeviewD.bind('<Double-1>', set_cell_value_D) 
treeviewE.bind('<Double-1>', set_cell_value_E) 
#treeviewE2D.bind('<Double-1>', set_cell_value_E2D) 
root.bind("<Control-o>", file_open)
root.bind("<Control-s>", file_save)
root.bind("<Control-n>", file_new)
root.bind("<Control-b>", viewCSV)

treeviewA.bind('<Control-a>', add_agent)
treeviewA2E.bind('<Control-a>', add_agent) 
treeviewAG.bind('<Control-a>', add_agent) 
treeviewW.bind('<Control-a>', add_wall) 
treeviewD.bind('<Control-a>', add_door) 
treeviewE.bind('<Control-a>', add_exit) 

treeviewA.bind('<Control-d>', del_agent)
treeviewA2E.bind('<Control-d>', del_agent) 
treeviewAG.bind('<Control-d>', del_agent) 
treeviewW.bind('<Control-d>', del_wall) 
treeviewD.bind('<Control-d>', del_door) 
treeviewE.bind('<Control-d>', del_exit) 


for col in columns:  # bind function: enable sorting in table headings
    treeviewA.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeviewA, _col, False))

for col in columns:  # bind function: enable sorting in table headings
    treeviewA2E.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeviewA2E, _col, False))

for col in columns:  # bind function: enable sorting in table headings
    treeviewAG.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeviewAG, _col, False))

for col in columns:  # bind function: enable sorting in table headings
    treeviewW.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeviewW, _col, False))

for col in columns:  # bind function: enable sorting in table headings
    treeviewD.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeviewD, _col, False))

for col in columns:  # bind function: enable sorting in table headings
    treeviewE.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeviewE, _col, False))

for col in columns:  # bind function: enable sorting in table headings
    treeviewE2D.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeviewE2D, _col, False))


#######################
# Configure the menubar

menubar = Menu(root, bg="lightgrey", fg="black")
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0, bg="lightgrey", fg="black")
file_menu.add_command(label="New", command=file_new, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=file_open, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=file_save, accelerator="Ctrl+S")
file_menu.add_command(label="Save_As", command=file_save_as)
menubar.add_cascade(label="File", menu=file_menu)

add_menu = Menu(menubar, tearoff=0, bg="lightgrey", fg="black")
add_menu.add_command(label="Add Agent", command=add_agent, accelerator="Ctrl+A")
add_menu.add_command(label="Add Wall", command=add_wall)
add_menu.add_command(label="Add Exit", command=add_exit)
add_menu.add_command(label="Add Door", command=add_door)
menubar.add_cascade(label="Add", menu=add_menu)

delete_menu = Menu(menubar, tearoff=0, bg="lightgrey", fg="black")
delete_menu.add_command(label="Delete Agent", command=del_agent, accelerator="Ctrl+D")
delete_menu.add_command(label="Delete Wall", command=del_wall) #, accelerator="Ctrl+D")
delete_menu.add_command(label="Delete Exit", command=del_exit)#, accelerator="Ctrl+D")
delete_menu.add_command(label="Delete Door", command=del_door) #, accelerator="Ctrl+D")
menubar.add_cascade(label="Delete", menu=delete_menu)

#newA = Button(frameAgent, text='New Agent', width=20, command=add_agent)
#newA.pack() #place(x=120,y=20 ) #(len(name)-1)*20+45)

#delA = Button(frameAgent, text='Delete Agent', width=20, command=del_agent)
#delA.pack() #place(x=120,y=20 )

def selectOutTxtFile_DoorProb(event=None):
    #tempdir=os.path.dirname(self.fname_EVAC)
    #print(tempdir)
    fname_OutTXT = tkf.askopenfilename(filetypes=(("txt files", "*.txt"),("All files", "*.*")),\
    initialdir=currentdir)
    #self.lb_outtxt.config(text = "The output txt file selected: "+str(temp[-1])+"\n")
    #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
    print('fname_outTxtFile:', fname_OutTXT)
    exitNum = spin_exitnumber.get()
    print('Exit index in plot:', exitNum)
    readDoorProb(fname_OutTXT, int(exitNum))

def py3tpre(event=None):
    fname_OutBIN = tkf.askopenfilename(filetypes=(("bin files", "*.bin"),("All files", "*.*")),\
    initialdir=currentdir)
    temp=re.split(r'/', fname_OutBIN)
    #temp=self.fname_OutTXT.split('/') 
    #self.lb_outbin.config(text = "The output bin file selected: "+str(temp[-1])+"\n")
    #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
    print('fname_outBinFile:', fname_OutBIN)
    visualizeTpre(fname_OutBIN)
    
def py3vis(event=None):
    fname_OutBIN = tkf.askopenfilename(filetypes=(("bin files", "*.bin"),("npz files", "*.npz"),("All files", "*.*")),\
    initialdir=currentdir)
    

    if os.path.exists('log.txt'):
        for line in open('log.txt', "r"):
            if re.match('ZOOM', line):
                temp =  line.split('=')
                ZOOM = float(temp[1].strip())                    
            if re.match('xSpace', line):
                temp =  line.split('=')
                xSpa = float(temp[1].strip())
            if re.match('ySpace', line):
                temp =  line.split('=')
                ySpa = float(temp[1].strip())
    else:
        ZOOM = 60.0
        xSpa = 30.0
        ySpa = 30.0
    
    #temp=self.fname_OutTXT.split('/') 
    #self.lb_outbin.config(text = "The output bin file selected: "+str(temp[-1])+"\n")
    #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
    print('Output data file selected:', fname_OutBIN)
    temp= fname_OutBIN.split('.')
    if temp[1]=='bin':
        visualizeAgent(fname_OutBIN, None, None, ZOOM, xSpa, ySpa)
        

def py3preprocess(event=None):
    topPreData = Toplevel(root)
    topPreData.title("Preprocess Data")
    
    topPreData.grab_set()
    topPreData.transient(root)
    topPreData.geometry("900x360")
    
    buttonTpre = Button(topPreData, text='Read output files and plot time line', width=60, command=py3tpre)
    buttonTpre.pack()
    
    buttonExitProb = Button(topPreData, text='Read output files and plot the exit selection probablity', width=60, command=selectOutTxtFile_DoorProb)
    buttonExitProb.pack() #place(x=19, y=230)

    spin_exitnumber = Spinbox(topPreData, from_=0, to=100, width=5, bd=8) 
    spin_exitnumber.pack() #place(x=596, y=230)


def py3PostData(event=None):
    topPostData = Toplevel(root)
    topPostData.title("Plot Panel")
    
    topPostData.grab_set()
    topPostData.transient(root)
    #self.menubar.config(state=DISABLED)
    
    master_pos_x = root.winfo_x()
    master_pos_y = root.winfo_y()

    master_width = root.winfo_width()
    master_height = root.winfo_height()
    
    my_width = 300
    my_height = 100

    pos_x = (master_pos_x + (master_width // 2)) - (my_width // 2)
    pos_y = (master_pos_y + (master_height // 2)) - (my_height // 2)

    geometry = "{}x{}+{}+{}".format(my_width, my_height, pos_x, pos_y)
    
    topPostData.geometry("600x200")
    
    buttonTpre = Button(topPostData, text='Read output binary data and plot time line', width=60, command= py3tpre)
    buttonTpre.pack()

    buttonVis = Button(topPostData, text='Read output binary data and visualize simulation', width=60, command= py3vis)#py3tpre)
    buttonVis.pack()
    
    buttonExitProb = Button(topPostData, text='Read output files and plot the exit selection probablity', width=60, command= selectOutTxtFile_DoorProb)
    buttonExitProb.pack() #place(x=19, y=230)

    spin_exitnumber = Spinbox(topPostData, from_=0, to=100, width=5, bd=8) 
    spin_exitnumber.pack() #place(x=596, y=230)


def py3run(event=None):
    #os.system("python main.py "+self.open_file)

    myTest = simulation()
    myTest.select_file(openFileName, None, 'no-debug')
    #myTest.read_data()
    myTest.readconfig()
    myTest.preprocessAgent()
    show_geom(myTest)

    if myTest.continueToSimu:
        myTest.preprocessGeom()
        myTest.preprocessAgent()
        #if myTest.solver == 1 or myTest.solver == 2:
        if len(myTest.exits)>0 and myTest.solver!=0:
            myTest.buildMesh()
            myTest.flowMesh()
            myTest.computeDoorDirection()
            #show_flow(myTest)
        else:
            myTest.solver=0
            
        myTest.dataSummary()
        show_simu(myTest)
        myTest.dataComplete()
    else:
        os.remove(myTest.outDataName + ".txt")

run_menu = Menu(menubar, tearoff=0, bg="lightgrey", fg="black")
run_menu.add_command(label="Run Simulation", command=py3run, accelerator="F5")
run_menu.add_command(label="Data Tool (Post-process)", command=py3PostData, accelerator="F6")
run_menu.add_command(label="Data Tool (Pre-process)", command=py3preprocess, accelerator="F7")
#run_menu.add_command(label="Delete Exit", command=del_exit)#, accelerator="Ctrl+D")
#run_menu.add_command(label="Delete Door", command=del_door) #, accelerator="Ctrl+D")
menubar.add_cascade(label="Run", menu=run_menu)

root.mainloop()
