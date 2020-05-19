'''
Created on Sep 20, 2013

@author: ARJUN PRASAD NAMDEO
@version: v01
'''

import os
import sys
import csv
import fnmatch
import re
from PyQt4 import QtCore, QtGui, uic

MainDirectory  = os.path.dirname(__file__).replace("\\", "/") + "/"
UIFilePath = MainDirectory + 'SMIP_Bank_UI_V01.ui'
sys.path.append(MainDirectory)

#from QDarkStyle import qdarkstyle

import Scripts.GenerateCustData as mod_GenCusDb
import Scripts.UpdateCustomerDataBase as mod_UpCusDb
import Scripts.GetData_MainDataBase as mod_getDataMainDb
import Scripts.qtMessageMod as mod_winMessage
import Scripts.encode as mod_encd
import Scripts.sendEmail as mod_sendMail

for mod in [mod_GenCusDb, mod_UpCusDb, mod_getDataMainDb, mod_winMessage, mod_encd, mod_sendMail]:
    reload(mod)

class DbMakerUI(QtGui.QMainWindow):
    '''
    Comments
    '''

    def __init__(self):
        '''
        constructor
        '''

        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi(UIFilePath)

        
        self.ui.show()
        self.startupSetup()
        
        
  
    def startupSetup(self):
        #self.applyStyleSheet()
        self.ui.showMaximized()
        self.ui.Bank_NewAcc_DOB_date.clear()
        self.ui.Bank_NewAcc_DOB_year.clear()
        self.ui.Bank_NewAcc_DOB_date.addItem(str(''))
        self.ui.Bank_NewAcc_DOB_year.addItem(str(''))
        for i in range(1,32):
            self.ui.Bank_NewAcc_DOB_date.addItem(str(i))
        for i in range(1948, 2003):
            self.ui.Bank_NewAcc_DOB_year.addItem(str(i))
        self.actionPackage()
            
    
    def actionPackage_NewAccount(self):
        self.ui.Bank_NewAcc_SubmitButton.clicked.connect(lambda:self.CreateNewAccount_CheckList())        
        self.ui.actionMenu_CreateNewAccount.triggered.connect(lambda:self.emptyNewAccount())
        self.ui.Bank_NewAcc_Done.clicked.connect(lambda:self.emptyNewAccount())
        
        
    def actionPackage(self):
        
        self.actionPackage_NewAccount()


        self.ui.MoneyDeposit_AccNum.currentIndexChanged.connect(lambda:self.getCurrentActiveCusName())
        self.ui.MoneyWithdrawl_AccNum.currentIndexChanged.connect(lambda:self.getCurrentActiveCusName())
        self.ui.MoneyTransfer_AccNum_Src.currentIndexChanged.connect(lambda:self.getCurrentActiveCusName())
        self.ui.MoneyTransfer_AccNum_Dest.currentIndexChanged.connect(lambda:self.getCurrentActiveCusName())
        self.ui.CheckAccBalance_AccNum.currentIndexChanged.connect(lambda:self.getCurrentActiveCusName())
        self.ui.MoneyTransfer_AccNum_Src.currentIndexChanged.connect(lambda:self.getBenificiaryAccList())

        self.ui.MoneyDeposit_DepositeButton.clicked.connect(lambda:self.Deposite_Money())
        self.ui.MoneyWithdrawl_WithdrawButton.clicked.connect(lambda:self.Withdrawl_Money())
        self.ui.MoneyTransfer_TransferMoney_PushButton.clicked.connect(lambda:self.TransferMoney())
        self.ui.CheckAccBalance_PushButton.clicked.connect(lambda:self.getBalaceInfo())
        self.ui.CheckStatements_GoPushButton.clicked.connect(lambda:self.ShowBankStatments())
        
        self.ui.Bank_NewAcc_HelpSecQ.clicked.connect(lambda:self.newAcc_SecurityHelp())
        
        
        
        
    def applyStyleSheet(self):
        styleFile= ("E:/AD_Lab_World/Python/PyQt/Bank/darkorange.stylesheet")
        with open(styleFile,"r") as fh:
            self.ui.setStyleSheet(fh.read())
            
    def newAcc_SecurityHelp(self):
        showMessageWindow( title="Message", msg = "Security Question is for your Help in further..\n\nIt will be asked to you When you lost your Password or Delete Account..", icon="Info")
        
        

    def emptyNewAccount(self):
        self.ui.Bank_NewAcc_Name.clear()
        self.ui.Bank_NewAcc_Balance.clear()
        self.ui.Bank_NewAcc_Password.clear()
        self.ui.Bank_NewAcc_RePassword.clear()
        self.ui.Bank_NewAcc_CusAccNum.clear()
        self.ui.Bank_NewAcc_CusID.clear()
        self.ui.Bank_NewAcc_Email.clear()
        self.ui.Bank_NewAcc_SqA_A.clear()
        self.ui.Bank_NewAcc_SqA_B.clear()
        
        self.ui.Bank_NewAccDone_Group.setMaximumSize (0, 0)
        self.ui.Bank_NewAccDone_Group.setMinimumSize (0, 0)
        
        self.ui.Bank_NewAcc_DOB_date.setCurrentIndex (0)
        self.ui.Bank_NewAcc_DOB_month.setCurrentIndex (0)
        self.ui.Bank_NewAcc_DOB_year.setCurrentIndex (0)
        self.ui.Bank_NewAcc_Sex.setCurrentIndex (0)
        self.ui.Bank_NewAcc_SqQ_A.setCurrentIndex (0)
        self.ui.Bank_NewAcc_SqQ_B.setCurrentIndex (1)
        self.clearAccNumList()
        self.getAccNumList()
        
        
    def errorOnIncompleteInput(self):
        showMessageWindow( title="Message", msg = "Error ... !!! All the fields are Mandatory. Please Ensure to give us Correct Information Detail, \n\nThese will Let You Help in Further Banking...!!!", icon="Error")

                
    def CreateNewAccount_CheckList(self):
        if len(str(self.ui.Bank_NewAcc_Name.text())) == 0 or len(str(self.ui.Bank_NewAcc_Balance.text())) == 0 or len(str(self.ui.Bank_NewAcc_Password.text())) == 0:
            self.errorOnIncompleteInput()
            return False
        
        if (str(self.ui.Bank_NewAcc_Balance.text())).isdigit() == False :
            self.errorOnIncompleteInput()
            return False
        
        if (str(self.ui.Bank_NewAcc_Password.text())) != (str(self.ui.Bank_NewAcc_RePassword.text())):
            self.errorOnIncompleteInput()
            return False
        
        if str(self.ui.Bank_NewAcc_DOB_date.currentText()) == "" or str(self.ui.Bank_NewAcc_DOB_month.currentText()) == "" or str(self.ui.Bank_NewAcc_DOB_year.currentText()) == "":
            self.errorOnIncompleteInput()
            return False
        
        if str(self.ui.Bank_NewAcc_SqA_A.text()) == "" or str(self.ui.Bank_NewAcc_SqA_A.text()) == "" or str(self.ui.Bank_NewAcc_Email.text()) == "":
            self.errorOnIncompleteInput()
            return False
        
        if str(self.ui.Bank_NewAcc_SqQ_A.currentText()) ==  str(self.ui.Bank_NewAcc_SqQ_B.currentText()):
            showMessageWindow( title="Message", msg = "Error ... !!! Select Difference Questions, You Cannot choose same question twise...!!!", icon="Error")
            return False
            
        validMailId = self.checkVaildMailAddress(str(self.ui.Bank_NewAcc_Email.text()))
        if not validMailId:
            showMessageWindow( title="Message", msg = "Error ... !!! Email Id seems to be incorrect..!!!\n\nPlease Enter a valid Mail Id of your, It will Help you in Further Banking with us...", icon="Error")
            return False
            
        
        self.CreateNewAccount_UpdateGlobalDataBase()
            
            

    
    def checkVaildMailAddress(self, emailId):
        reCheck = re.match("[a-zA-Z0-9_.-]+@[a-z]+\.[a-z]+", emailId)
        if not reCheck:
            return False
        
        if not emailId.endswith(".com") and not emailId.endswith(".in") and not emailId.endswith(".co.in") and not emailId.endswith(".net") and not emailId.endswith(".org"):
            return False
        
        return True
    
        

    def CreateNewAccount_UpdateGlobalDataBase(self):
        NewCusData = mod_GenCusDb.GenerateData_Cus(MainDirectory)               # Gets New Customer ID and Account Number
        MainDataBaseFile = MainDirectory + 'DataBase/SMIP_Bank_MainDataBase_V01.csv'

        readfile = open(MainDataBaseFile, 'r')
        readLine = readfile.readlines()
        readfile.close()

        CusNo = str(len(readLine))
        CusName = str(self.ui.Bank_NewAcc_Name.text())
        CusDOB = " ".join([str(self.ui.Bank_NewAcc_DOB_date.currentText()), str(self.ui.Bank_NewAcc_DOB_month.currentText()), str(self.ui.Bank_NewAcc_DOB_year.currentText())])
        CusSex = str(self.ui.Bank_NewAcc_Sex.currentText())
        CusPassword = str(mod_encd.encrypt(str(self.ui.Bank_NewAcc_Password.text())))
        CusEmail = str(self.ui.Bank_NewAcc_Email.text())
        CusBalance = str(self.ui.Bank_NewAcc_Balance.text())
        CusID = str(NewCusData[0])
        CusAccNo = str(NewCusData[1])
        CusQs_A = str(self.ui.Bank_NewAcc_SqQ_A.currentText())
        CusAn_A = str(self.ui.Bank_NewAcc_SqA_A.text())
        CusQs_B = str(self.ui.Bank_NewAcc_SqQ_B.currentText())
        CusAn_B = str(self.ui.Bank_NewAcc_SqA_B.text())
        
        
        CusDataInfo = [CusNo, CusName, CusDOB, CusSex, CusPassword, CusEmail, CusBalance, CusID, CusAccNo, CusQs_A, CusAn_A, CusQs_B, CusAn_B ]

        sendMail = mod_sendMail.welcome_mail(CusDataInfo)
        if not sendMail:
            showMessageWindow( title="Message", msg = "Your Email Id or Your Internet Connection seems to have some Problem..\n\nProvide a Valid Email Id and Cross Check Internet Connection...!!!", icon="Alert")
            return False


        writeFile = csv.writer(open(MainDataBaseFile, 'a'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writeFile.writerow(CusDataInfo)
        

    
        self.ui.Bank_NewAccDone_Group.setMaximumSize (471, 401)
        self.ui.Bank_NewAccDone_Group.setMinimumSize (471, 401)
        self.ui.Bank_NewAcc_CusAccName.setText(CusName)
        self.ui.Bank_NewAcc_CusAccNum.setText(CusAccNo)
        self.ui.Bank_NewAcc_CusID.setText(CusID)
        self.ui.Bank_NewAcc_CusAccEmail.setText(CusEmail)
        self.ui.Bank_NewAcc_CusAccBalance.setText(CusBalance)       

        
        self.ui.Bank_NewAccCongoText.setText("Congratulation..!!!")
        self.ui.Bank_NewAccCongoTextData.setText("Here is Your Account Information, \nThis information has been sent to your Mail Also.")
        self.ui.Bank_NewAccCongoImage.setPixmap(QtGui.QPixmap( MainDirectory + "/icons/Happy-Minion-Icon.png"))
        mod_UpCusDb.UpdateCustomerDataBase(MainDirectory,CusID,CusName,CusBalance,CusBalance,'Deposit','')
        
        
        showMessageWindow( title="Message", msg = "Done ... !!! Your Account has been successfully opened in Our Bank... \n\nWelcome to Horizon Financial Bank...!!!", icon="Info")

        
        self.clearAccNumList()
        self.getAccNumList()
        
        
    def getAccNumList(self):
        CusList = mod_getDataMainDb.getAccountNumList(MainDirectory)
        for AccNum in CusList:
            self.ui.MoneyDeposit_AccNum.addItem(AccNum, 0)
            self.ui.MoneyWithdrawl_AccNum.addItem(AccNum, 0)    
            self.ui.CheckAccBalance_AccNum.addItem(AccNum, 0)
            self.ui.MoneyTransfer_AccNum_Src.addItem(AccNum, 0)
            self.ui.CheckStatements_AccNum.addItem(AccNum, 0)
            


    def getBenificiaryAccList(self):
        CusList = mod_getDataMainDb.getAccountNumList(MainDirectory)
        self.ui.MoneyTransfer_AccNum_Dest.clear()
        for AccNum in CusList:
            if str(AccNum) != str(self.ui.MoneyTransfer_AccNum_Src.currentText()):
                self.ui.MoneyTransfer_AccNum_Dest.addItem(AccNum,0)


    def getBalaceInfo(self):
        CusAccNum = str(self.ui.CheckAccBalance_AccNum.currentText())
        CusPassword = str(self.ui.CheckAccBalance_AccPassword.text())

        if len(str(CusPassword)) > 0:
            DataBasePassword = mod_getDataMainDb.getData_by_AccNum(MainDirectory,CusAccNum,4)
            if str(DataBasePassword) ==  str(CusPassword):
                CusBalance = mod_getDataMainDb.getData_by_AccNum(MainDirectory,CusAccNum,5)
                CusIDNum = mod_getDataMainDb.getData_by_AccNum(MainDirectory,CusAccNum,6)
                self.ui.CheckAccBalance_ShowAccNum.setText(str(CusAccNum))
                self.ui.CheckAccBalance_ShowCIDNum.setText(str(CusIDNum))
                self.ui.CheckAccBalance_ShowAccBalance.setText(str(CusBalance))
                self.ui.CheckAccInfo_ErrorLabel.setText(str(''))
            else:
                self.ui.CheckAccInfo_ErrorLabel.setText(str('Error !!! Password is not matching with DataBase.'))



    def ShowBankStatments(self):
        CusAccNum = str(self.ui.CheckStatements_AccNum.currentText())
        CusPassword = str(self.ui.CheckStatements_AccPassword.text())

        Cus_DB_Password = str(mod_getDataMainDb.getData_by_AccNum(MainDirectory,CusAccNum,4))

        if str(CusPassword) == str(Cus_DB_Password):
            CusName = str(mod_getDataMainDb.getData_by_AccNum(MainDirectory,CusAccNum,1))
            CusSex = str(mod_getDataMainDb.getData_by_AccNum(MainDirectory,CusAccNum,3))
            CusID = str(mod_getDataMainDb.getData_by_AccNum(MainDirectory,CusAccNum,6))

            CustomerDataBaseFilePath = str(MainDirectory) + 'DataBase/SMIP_Bank_CustomerDataBase/' +  str(CusID) + '__' + str(CusName) + '.csv'

            openFile = open(CustomerDataBaseFilePath, 'r')
            readLines = openFile.readlines()

            index = 0
            self.ui.CheckStatements_TableWidget.clear()
            
            self.ui.CheckStatements_TableWidget.setHorizontalHeaderItem ( 0, (QtGui.QTableWidgetItem(' Balance ')))
            self.ui.CheckStatements_TableWidget.setHorizontalHeaderItem ( 1, (QtGui.QTableWidgetItem(' Amount ')))
            self.ui.CheckStatements_TableWidget.setHorizontalHeaderItem ( 2, (QtGui.QTableWidgetItem(' Type ')))
            self.ui.CheckStatements_TableWidget.setHorizontalHeaderItem ( 3, (QtGui.QTableWidgetItem(' Date ')))
            self.ui.CheckStatements_TableWidget.setHorizontalHeaderItem ( 4, (QtGui.QTableWidgetItem(' Comment ')))

            for eachLine in readLines:

                if int(index) > 0 :
                    self.ui.CheckStatements_TableWidget.setItem(int(index-1), 0, (QtGui.QTableWidgetItem(eachLine.split(',')[1])))
                    self.ui.CheckStatements_TableWidget.setItem(int(index-1), 1, (QtGui.QTableWidgetItem(eachLine.split(',')[2])))
                    self.ui.CheckStatements_TableWidget.setItem(int(index-1), 2, (QtGui.QTableWidgetItem(eachLine.split(',')[3])))
                    self.ui.CheckStatements_TableWidget.setItem(int(index-1), 3, (QtGui.QTableWidgetItem(eachLine.split(',')[4])))
                    self.ui.CheckStatements_TableWidget.setItem(int(index-1), 4, (QtGui.QTableWidgetItem(eachLine.split(',')[5])))

                    
                self.ui.CheckStatements_TableWidget.insertRow(index+1)
                index += 1 

    
            
            if str(CusSex) == 'Male':
                self.ui.CheckStatements_ErrorLabel.setText(str('Welcome     Mr. ') + str(CusName) + '            Have a Good Day. ')
            else :
                self.ui.CheckStatements_ErrorLabel.setText(str('Welcome     Miss./Smt. ') + str(CusName) + '            Have a Good Day. ')

            
        else :
            self.ui.CheckStatements_ErrorLabel.setText('Error...!!!       Incorrect Password.')
             

        

        
            
        
                
                


    def Deposite_Money(self):
        CusAccNum = str(self.ui.MoneyDeposit_AccNum.currentText())
        CusPassword = str(self.ui.MoneyDeposit_AccPassword.text())
        CusComment = str(self.ui.MoneyDeposit_AccComment.text())
        Amount = str(self.ui.MoneyDeposit_AccAmount.text())
        TransectionType = 'Deposit'
        if len(CusAccNum) == 0 or len(CusPassword) == 0 or len(Amount) == 0:
            self.ui.MoneyDeposit_ErrorLabel.setText(str('Error !!! All Above Fields are Mandatory.'))
        else:
            if (str(Amount)).isdigit() == True:
                Deposite_Result = mod_UpCusDb.MakeMoneyDW(MainDirectory,CusAccNum,CusPassword,Amount,TransectionType,CusComment)
                self.ui.MoneyDeposit_ErrorLabel.setText(str(Deposite_Result))
                if str(Deposite_Result) == '':
                    self.ui.MoneyDeposit_AccNum.setEnabled(False)
                    self.ui.MoneyDeposit_AccPassword.setEnabled(False)
                    self.ui.MoneyDeposit_AccAmount.setEnabled(False)
                    self.ui.MoneyDeposit_AccAmount.setEnabled(False)
                    self.ui.MoneyDeposit_AccName.setEnabled(False)
                    self.ui.MoneyDeposit_AccComment.setEnabled(False)
                    self.ui.MoneyDeposit_DepositeButton.setEnabled(False)
                    self.ui.MoneyDeposit_ErrorLabel.setText(str(''))
                    self.ui.MoneyDeposit_CongoLabel.setText(str('Your Transection of Depositing Money has been Done Succesfully.\n\nYou Can Check Your Balance in Check Account Information Tab.'))
                    
                
            else:
                self.ui.MoneyDeposit_ErrorLabel.setText(str('Error !!!  Money Amount Should be a Numeric Input(0-9).'))


    def Withdrawl_Money(self):
        CusAccNum = str(self.ui.MoneyWithdrawl_AccNum.currentText())
        CusPassword = str(self.ui.MoneyWithdrawl_AccPassword.text())
        CusComment = str(self.ui.MoneyWithdrawl_AccComment.text())
        Amount = str(self.ui.MoneyWithdrawl_AccAmount.text())
        TransectionType = 'Withdrawl'
        if len(CusAccNum) == 0 or len(CusPassword) == 0 or len(Amount) == 0:
            self.ui.MoneyWithdrawl_ErrorLabel.setText(str('Error !!! All Above Fields are Mandatory.'))
        else:
            if (str(Amount)).isdigit() == True:
                Withdrawl_Result = mod_UpCusDb.MakeMoneyDW(MainDirectory,CusAccNum,CusPassword,Amount,TransectionType,CusComment)
                self.ui.MoneyWithdrawl_ErrorLabel.setText(str(Withdrawl_Result))
                if str(Withdrawl_Result) == '':
                    self.ui.MoneyWithdrawl_AccNum.setEnabled(False)
                    self.ui.MoneyWithdrawl_AccPassword.setEnabled(False)
                    self.ui.MoneyWithdrawl_AccAmount.setEnabled(False)
                    self.ui.MoneyWithdrawl_AccAmount.setEnabled(False)
                    self.ui.MoneyWithdrawl_AccName.setEnabled(False)
                    self.ui.MoneyWithdrawl_AccComment.setEnabled(False)
                    self.ui.MoneyWithdrawl_WithdrawButton.setEnabled(False)
                    
                    self.ui.MoneyWithdrawl_ErrorLabel.setText(str(''))
                    self.ui.MoneyWithdrawl_CongoLabel.setText(str('Your Transection of Withdrawl Money has been Done Succesfully .\n\nYou Can Check Your Balance in Check Account Information Tab.'))
                    
                
            else:
                self.ui.MoneyWithdrawl_ErrorLabel.setText(str('Error !!!  Money Amount Should be a Numeric Input(0-9).'))

    def TransferMoney(self):
        CusAccNum = str(self.ui.MoneyTransfer_AccNum_Src.currentText())
        CusPassword = str(self.ui.MoneyTransfer_Password.text())
        CusComment = str(self.ui.MoneyTransfer_Comment.text())
        Amount = str(self.ui.MoneyTransfer_Amount.text())
        TransectionType = 'Withdrawl'

        CusB_AccNum = str(self.ui.MoneyTransfer_AccNum_Dest.currentText())
        CusB_Password = str(mod_getDataMainDb.getUserPassword_by_AccNum(MainDirectory,CusB_AccNum))

        if len(CusAccNum) == 0 or len(CusPassword) == 0 or len(Amount) == 0:
            self.ui.MoneyTransfer_ErrorLabel.setText(str('Error !!! All Above Fields are Mandatory.'))
        else:
            if (str(Amount)).isdigit() == True:
                Trans_Withdrawl_Result = mod_UpCusDb.MakeMoneyDW(MainDirectory,CusAccNum,CusPassword,Amount,TransectionType,CusComment)
                self.ui.MoneyTransfer_ErrorLabel.setText(str(Trans_Withdrawl_Result))
                if str(Trans_Withdrawl_Result) == "":
                    Trans_Deposit_Result = mod_UpCusDb.MakeMoneyDW(MainDirectory,CusB_AccNum,CusB_Password,Amount,'Deposit',CusComment)
                    if str(Trans_Deposit_Result) == "":
                        self.ui.MoneyTransfer_AccNum_Src.setEnabled(False)
                        self.ui.MoneyTransfer_AccName_Src.setEnabled(False)
                        self.ui.MoneyTransfer_AccNum_Dest.setEnabled(False)
                        self.ui.MoneyTransfer_AccName_Dest.setEnabled(False)
                        self.ui.MoneyTransfer_Password.setEnabled(False)
                        self.ui.MoneyTransfer_Amount.setEnabled(False)
                        self.ui.MoneyTransfer_Comment.setEnabled(False)
                        self.ui.MoneyTransfer_TransferMoney_PushButton.setEnabled(False)
                        self.ui.MoneyTransfer_ErrorLabel.setText(str(''))
                        self.ui.MoneyTransfer_CongoLabel.setText(str('Your Transection of Transfer Money  has been Done Succesfully.\n\nYou Can Check Your Balance in Check Account Information Tab.'))
                        

            else:
                self.ui.MoneyTransfer_ErrorLabel.setText(str('Error !!!  Money Amount Should be a Numeric Input(0-9).'))

    


    def getCurrentActiveCusName(self):
        CusAccNumA = str(self.ui.MoneyDeposit_AccNum.currentText())
        GetCusNameA = mod_getDataMainDb.getUserName_by_AccNum(MainDirectory, CusAccNumA)
        self.ui.MoneyDeposit_AccName.setText(str(GetCusNameA))

        CusAccNumB = str(self.ui.MoneyWithdrawl_AccNum.currentText())
        GetCusNameB = mod_getDataMainDb.getUserName_by_AccNum(MainDirectory, CusAccNumB)
        self.ui.MoneyWithdrawl_AccName.setText(str(GetCusNameB))

        CusAccNumC = str(self.ui.MoneyTransfer_AccNum_Src.currentText())
        GetCusNameC = mod_getDataMainDb.getUserName_by_AccNum(MainDirectory, CusAccNumC)
        self.ui.MoneyTransfer_AccName_Src.setText(str(GetCusNameC))

        CusAccNumD = str(self.ui.MoneyTransfer_AccNum_Dest.currentText())
        GetCusNameD= mod_getDataMainDb.getUserName_by_AccNum(MainDirectory, CusAccNumD)
        self.ui.MoneyTransfer_AccName_Dest.setText(str(GetCusNameD))

        CusAccNumE = str(self.ui.CheckAccBalance_AccNum.currentText())
        GetCusNameE= mod_getDataMainDb.getUserName_by_AccNum(MainDirectory, CusAccNumE)
        self.ui.CheckAccBalance_AccName.setText(str(GetCusNameE))

        
    def clearAccNumList(self):
        self.ui.MoneyDeposit_AccNum.clear()
        self.ui.MoneyWithdrawl_AccNum.clear()

        self.ui.MoneyTransfer_AccNum_Src.clear()
            

    
            


def main():
    app = QtGui.QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    app.setStyleSheet("plastique")
    winApp = DbMakerUI()
    winApp.getAccNumList()
        
    sys.exit(app.exec_())








        
        
  


def showMessageWindow( title="Message", msg = "Here paste the text", icon="Info"):
    icoPath = "E:/AD_Lab_World/Python/PyQt/Bank/icons"
    winMsgApp = uic.loadUi(MainDirectory + 'qtMsg.ui')
    winMsgApp.setStyleSheet(qdarkstyle.load_stylesheet())
    winMsgApp.show()
     
    winMsgApp.iconLabel.setPixmap(QtGui.QPixmap(("/".join([icoPath, str(icon) + ".ico"]))))
    winMsgApp.messageText.setText(str(msg))
    winMsgApp.setWindowTitle(str(title))
    winMsgApp.button.clicked.connect(lambda:(winMsgApp.close()))
    

main()