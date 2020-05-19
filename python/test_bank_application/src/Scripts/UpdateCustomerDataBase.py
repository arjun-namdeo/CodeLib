import os 
import sys
import csv

import DateTime


def UpdateCustomerDataBase(BaseDirectory, CusIDNum,CusName,CusMainBalance,CusTransectionAmount,CusTransectionType,CusComment):

    
    CusIDNum = str(CusIDNum)
    CusName = str(CusName)
    CusComment = str(CusComment)
      
    CusDataBase_CSV  = BaseDirectory + 'DataBase/SMIP_Bank_CustomerDataBase/' + str(CusIDNum) + '__' + str(CusName) + '.csv'
    
    if os.path.exists(CusDataBase_CSV) == False :
        createCSV = open(CusDataBase_CSV, 'wb')
        writer = csv.writer(createCSV)
        createCSV.close()
    
    writeCSVFile = open(CusDataBase_CSV, 'a')
    openCSVFile = open(CusDataBase_CSV, 'r')
    readLines = openCSVFile.readlines()

    CusTrasectionDate = str(DateTime.CurrentDateTime())
    SetHeading = 'CusTransectionNum,CusMoneyBalance,CusTransectionAmount,CusTransectionType,CusTransectionDate,Comment\n'

    if int(len(readLines)) == 0:
        CTNum = 1
    else :
        CTNum = (int(len(readLines)))
    
    SetTransectionData = str(CTNum) + ',' + str(CusMainBalance) + ',' +  str(CusTransectionAmount) + ',' + str(CusTransectionType) + ',' + str(CusTrasectionDate) + ',' + str(CusComment) + '\n'

    if len(readLines) == 0:
        writeCSVFile.write(SetHeading)
    writeCSVFile.write(SetTransectionData)
    
    writeCSVFile.close()
    openCSVFile.close()







def MakeMoneyDW(BaseDirectory,CusAccNum,CusPassword,Amount,TransectionType,CusComment):
    import os, sys, csv
    sys.path.append(str(BaseDirectory))
    from Scripts import UpdateCustomerDataBase

    
    DataBaseFilePath = BaseDirectory + 'DataBase/SMIP_Bank_MainDataBase_V01.csv'
    CusAccNum = str(CusAccNum)
    CusPassword = str(CusPassword)
    CusComment = str(CusComment)
    Amount = int(Amount)
    TransectionType = str(TransectionType)
    
    openFile = open(DataBaseFilePath, 'r')
    readLines = openFile.readlines()
    
    Error = ""
    ErrorCount = 0
    
    for eachLine in readLines:
        if eachLine.__contains__(str(CusAccNum)) == True :
            if (str(eachLine.split(',')[4]) == str(CusPassword)):
                CusOldBalance = eachLine.split(',')[5]
                CusNewBalance = 0
                if TransectionType == 'Deposit':
                    CusNewBalance = int(CusOldBalance) + int(Amount)
                    ErrorCount = 0
                elif  TransectionType == 'Withdrawl':
                    if int(CusOldBalance)<int(Amount):
                        ErrorCount = 1
                        Error = "Error !!! You don't have mentioned Balance in Account."
                    else :
                        CusNewBalance = int(CusOldBalance) - int(Amount)
                        ErrorCount = 0
                if ErrorCount == 0:
                    CusIDNum = str(eachLine.split(',')[6])
                    CusName = str(eachLine.split(',')[1])
                    CusMainBalance = str(CusNewBalance)
                    CusTransectionAmount = str(Amount)
                    CusTransectionType = str(TransectionType)
                    CusComment = str(CusComment)
                    UpdateCustomerDataBase.UpdateCustomerDataBase(BaseDirectory, CusIDNum,CusName,CusMainBalance,CusTransectionAmount,CusTransectionType,CusComment)

            else:
                Error = "Error !!! Account No and Password are not Matching."
                ErrorCount = 1
    
    
    if ErrorCount == 0 :
        writeFile = open(DataBaseFilePath, 'w')
         
        for eachLine in readLines:
            if eachLine.__contains__(str(CusAccNum)) == True :
                SetNewData = str(eachLine.split(',')[0]) + ',' + str(eachLine.split(',')[1]) + ',' + str(eachLine.split(',')[2])  + ',' +  str(eachLine.split(',')[3])  + ',' +  str(eachLine.split(',')[4])  + ',' +  str(CusNewBalance)  + ',' +  str(eachLine.split(',')[6])  + ',' +  str(eachLine.split(',')[7]) 
            else:
                SetNewData = str(eachLine)
            writeFile.write(str(SetNewData))

        writeFile.close()
        openFile.close()
    
    return str(Error)

 
