'''
Created on Jun 22, 2014

@author: ProAccount
'''


import os
import sys
import smtplib
import encode as mod_encd


					#		0		1		2		3		   4		  5			 6			7		8		9		10			11		12
# Input as CusDataInfo = [CusNo, CusName, CusDOB, CusSex, CusPassword, CusEmail, CusBalance, CusID, CusAccNo, CusQs_A, CusAn_A, CusQs_B, CusAn_B ]

def welcome_mail(CustomerData):
	
	CusName = CustomerData[1]
	CusAccNum = CustomerData[8]
	CusIdNum = CustomerData[7]
	CusPassword = CustomerData[4]
	CusMailId = CustomerData[5]
	CusBalance = CustomerData[6]
	
	decryptPassword = str(mod_encd.decrypt(CusPassword))
	
	TO = str(CusMailId)
	SUBJECT = "Account Information, Horizon Financial Bank"
	TEXT = "\n\n\n\n\n\t\t\t\t\t\t Welcome to Horizon Financial Bank\n\t\t\t\t\t\t------------------------------------------------\n\n\nHello  {name}.\
			\n\nYour Account has been activated in our Bank. This message is computer generated, Do not reply on this...\
			\nBelow is your Account Information. Please Do not share Your Security Code with anyone..!!!\n\n\n******* ACCOUNT INFO  ********\
			\n\n\tAccount Holder Name     :     {name}\
			\n\tAccount Number             :     {accNum}\
			\n\tCustomer ID Number      :     {cusIdNum}\
			\n\tAccount Password          :     {password}\
			\n\tEmail ID                          :     {email}\
			\n\tAccount Balance            :     {money}\n\n\n\nThank You,\nHorizon Financial Bank".format(name = CusName,
																											accNum = CusAccNum,
																											cusIdNum = CusIdNum,
																											password = decryptPassword,
																											email = CusMailId, 
																											money = CusBalance)



	# Gmail Account
	gmail_sender = "informer.hfbank@gmail.com"
	gmail_password = "horizonfinancialbank@12345"
	
	
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(gmail_sender, gmail_password)
	
		BODY = "\r\n".join([
				'To: %s' % TO,
				'From: %s' % gmail_sender,
				'Subject: %s' % SUBJECT,
				'',
				TEXT ])
	
	
		server.sendmail(gmail_sender, [TO], BODY)
		print ">>> email sent"
		return True

	except Exception:
		print ">>> error on sending mail\n%s" % Exception
		return False
			
		