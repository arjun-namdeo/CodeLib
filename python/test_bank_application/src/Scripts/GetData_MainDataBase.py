
def getAccountNumList(MainDirectory):
    MainDataBaseFile = MainDirectory + 'DataBase/SMIP_Bank_MainDataBase_V01.csv'

    readFile = open(MainDataBaseFile, 'r')
    readLine = readFile.readlines()
    CusList = []

    for eachLine in readLine:
        if eachLine.split(',')[1] != 'CusName':
            CusList.append((eachLine.split(',')[7]).split('\n')[0])
    return CusList



def getUserName_by_AccNum(MainDirectory, CusAccNum):
    MainDirectory  = str(MainDirectory)
    DataBaseFilePath = MainDirectory + 'DataBase/SMIP_Bank_MainDataBase_V01.csv'
    CusAccNum = str(CusAccNum)
    
    openFile = open(DataBaseFilePath, 'r')
    readLines = openFile.readlines()
    
    for eachLine in readLines:
        if eachLine.__contains__(str(CusAccNum)) == True :
            CusName = str(eachLine.split(',')[1])
            
    return CusName


def getUserPassword_by_AccNum(MainDirectory, CusAccNum):
    MainDirectory  = str(MainDirectory)
    DataBaseFilePath = MainDirectory + 'DataBase/SMIP_Bank_MainDataBase_V01.csv'
    CusAccNum = str(CusAccNum)
    
    openFile = open(DataBaseFilePath, 'r')
    readLines = openFile.readlines()
    
    for eachLine in readLines:
        if eachLine.__contains__(str(CusAccNum)) == True :
            CusPassword = str(eachLine.split(',')[4])
            
    return CusPassword



def getData_by_AccNum(MainDirectory, CusAccNum, part):
    MainDirectory  = str(MainDirectory)
    DataBaseFilePath = MainDirectory + 'DataBase/SMIP_Bank_MainDataBase_V01.csv'
    CusAccNum = str(CusAccNum)
    part = int(part)
    
    openFile = open(DataBaseFilePath, 'r')
    readLines = openFile.readlines()
    
    for eachLine in readLines:
        if eachLine.__contains__(str(CusAccNum)) == True :
            CusData = str(eachLine.split(',')[int(part)])
            
    return CusData




