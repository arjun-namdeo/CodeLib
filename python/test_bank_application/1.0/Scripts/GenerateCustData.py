import sys
import os
import csv

def GenerateData_Cus(MainDirectory):
    MainDataBaseFile = MainDirectory + 'DataBase/SMIP_Bank_MainDataBase_V01.csv'
    openFile_generateID = open(MainDataBaseFile, 'r')
    readAllData = openFile_generateID.readlines()    
    CusNo = []
    for eachData in readAllData:
        CusNo.append(eachData.split(',')[7])
    if len(CusNo) < 2 :
        setLastCusNum = 0
    else :
        setLastCusNum = (CusNo[-1].split('CusID'))[1]
    setNewCusNum = int(setLastCusNum) + 1
    
    while (len(str(setNewCusNum)) != 5):
        setNewCusNum = '0' + str(setNewCusNum)     
    
    setNewCusID = 'CusID' + str(setNewCusNum)
    setNewCusAccNum = 'HFB0AN-' + str(int(10000) + int(setNewCusNum))
    openFile_generateID.close()

    return (str(setNewCusID), str(setNewCusAccNum))

