

MainDirectory  = 'E:/AD_Lab_World/Python/PyQt/Bank/'

def MakeMoneyDW(MainDirectory,CusAccNum,CusPassword,Amount,TransectionType):
    DataBaseFilePath = MainDirectory + 'DataBase/SMIP_Bank_MainDataBase_V01.csv'
    CusAccNum = str('SMIP0AID10001')
    CusPassword = 'home'
    Amount = int('5000')
    TransectionType = 'D'
    
    openFile = open(DataBaseFilePath, 'r')
    readLines = openFile.readlines()
    
    Error = ""
    ErrorCount = 0
    
    for eachLine in readLines:
        if eachLine.__contains__(str(CusAccNum)) == True :
           if str(eachLine.split(',')[4]) == str(CusPassword):
                CusOldBalance = eachLine.split(',')[5]
                if TransectionType == 'D':
                    CusNewBalance = int(CusOldBalance) + int(Amount)
                elif  TransectionType == 'W':
                    CusNewBalance = int(CusOldBalance) - int(Amount)
                ErrorCount = 0
            else :
                Error = " Password didn't match as per DataBase"
                ErrorCount = 1
    
    
    if ErrorCount == 0 :
        writeFile = open(DataBaseFilePath, 'w')
         
        for eachLine in readLines:
            if eachLine.__contains__(str(CusAccNum)) == True :
                SetNewData = str(eachLine.split(',')[0]) + ',' + str(eachLine.split(',')[1]) + ',' + str(eachLine.split(',')[2])  + ',' +  str(eachLine.split(',')[3])  + ',' +  str(eachLine.split(',')[4])  + ',' +  str(CusNewBalance)  + ',' +  str(eachLine.split(',')[6])  + ',' +  str(eachLine.split(',')[7]) 
            else :
                SetNewData = str(eachLine)
            writeFile.write(str(SetNewData))
        writeFile.close()
        openFile.close()
    
    return str(Error)
