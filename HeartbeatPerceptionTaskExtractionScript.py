
# coding: utf-8

# In[157]:


#/Python 3.6 build
import pandas as pd
import os
import glob
from datetime import date
import numpy as np

os.chdir("/Users/janebarker/Desktop/Heartbeat Perception Data") #note: change to current data directory

outputfile = os.getcwd() + '/Summary_HBPerception_Data_' + (str(date.today())) + '.csv'

#%load_ext rpy2.ipython #drop this line unless working in jupyter (w/R)

files = glob.glob('ChildMF*.csv') #currently iterates through any .csv files starting with ChildMF

#print(files) #uncomment to generate list of files in current summary file in python output

SubjectID = []
SessionID = []
int1meanHR = []
int2meanHR = []
int3meanHR = []
int1totHB = []
int2totHB = []
int3totHB = []

for f in files:
    df = pd.read_csv(f)
    SubjectID_tmp = f.split("_")[2] #grab subject and session ID from file name
    SessionID_tmp = f.split("_")[3][:-4]
    T0stop = df['Timestamps'].loc[df['Markers']=='test_stop0'].astype(float) #grab testing timestamps
    T0start = df['Timestamps'].loc[df['Markers']=='test_start0'].astype(float)
    T1stop = df['Timestamps'].loc[df['Markers']=='test_stop1'].astype(float)
    T1start = df['Timestamps'].loc[df['Markers']=='test_start1'].astype(float)
    T2stop = df['Timestamps'].loc[df['Markers']=='test_stop2'].astype(float)
    T2start = df['Timestamps'].loc[df['Markers']=='test_start2'].astype(float)
    T0int = (T0stop - T0start.values)/60 #calculate timing interval for each test trial
    T1int = (T1stop - T1start.values)/60
    T2int = (T2stop - T2start.values)/60
    
    t1 = df.index[df['Markers'] == "test_start0"].astype(int) #grab row indices of start/stop times
    t2 = df.index[df['Markers'] == "test_stop0"].astype(int)
    t3 = df.index[df['Markers'] == "test_start1"].astype(int)
    t4 = df.index[df['Markers'] == "test_stop1"].astype(int)
    t5 = df.index[df['Markers'] == "test_start2"].astype(int)
    t6 = df.index[df['Markers'] == "test_stop2"].astype(int)
    
    int1meanHR_tmp = df['Heart Rate'].loc[t1[0]:t2[0]].mean()
    int2meanHR_tmp = df['Heart Rate'].loc[t3[0]:t4[0]].mean()
    int3meanHR_tmp = df['Heart Rate'].loc[t5[0]:t6[0]].mean()
    
    int1meanHR.append(int1meanHR_tmp) #calculate mean HR across each test interval
    int2meanHR.append(int2meanHR_tmp)
    int3meanHR.append(int3meanHR_tmp)
        
    int1totHB.append(int1meanHR_tmp*T0int.values[0]) #calculate heartbeat N across each test interval
    int2totHB.append(int2meanHR_tmp*T1int.values[0])
    int3totHB.append(int3meanHR_tmp*T2int.values[0])
    
    SubjectID.append(SubjectID_tmp)
    SessionID.append(SessionID_tmp)
    
fulld = { 'SubjectID' : SubjectID, 'SessionID': SessionID, 'TestInt1meanHR': int1meanHR, 'TestInt2meanHR': int2meanHR,
     'TestInt3meanHR': int3meanHR, 'TestInt1totHB': int1totHB, 'TestInt2totHB': int2totHB, 'TestInt3totHB': int3totHB }
                              
fin_df = pd.DataFrame(data=fulld)
fin_df.to_csv(outputfile)
    
    


