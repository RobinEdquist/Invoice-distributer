#imports
import smtplib
import csv
import os
import sys
import glob
import ntpath
from os import listdir
from os.path import join, isfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#____CHANGE THESE ONLY____
subject = 'test subject'
body = 'body Entry'
#File extension of the files you want to send
fileExtension = '.txt'

#___ALSO CHANGE THESE____
#account information
loginMail = 'MyEmail@gmail.com'
loginPassword = 'myPassword'

#difference between operating systems
operatingSystem = sys.platform
if(operatingSystem == 'darwin' or operatingSystem == 'linux'):
  thisDirectory = os.path.join(os.getcwd,'src')
else:
  thisDirectory = os.getcwd() 
#find csv file of emails
mailListDirPath = os.path.join(thisDirectory, 'mail-list')
mailList = [f for f in listdir(mailListDirPath) if isfile(join(mailListDirPath, f))]
mailListFilePath = os.path.join(mailListDirPath, mailList[0])

#Open csv file
with open(mailListFilePath, 'r') as csvFile:
  reader = csv.reader(csvFile)
  emailRecList = list(reader)
emailRecList = [emailRecList[i][0] for i in range(0,len(emailRecList))]

#Load all attachments
attachmentDirPath = os.path.join(thisDirectory,'attachments')
filesToSend = [int(os.path.splitext(ntpath.basename(name))[0]) for name in glob.glob(os.path.join(attachmentDirPath,'*'+fileExtension))]
filesToSend.sort(key=int)
filesToSend = list(map(str,filesToSend))

counter = 0
for mailTo in emailRecList:
  #create text part of email
  msg = MIMEMultipart()
  msg['From'] = loginMail
  msg['To'] = mailTo
  msg['Subject'] = subject

  #read attachment
  filename = os.path.join(attachmentDirPath,filesToSend[counter]+fileExtension)
  attachment = open(filename,'rb')

  #add attachment to message
  part = MIMEBase('application', 'octet-stream')
  part.set_payload(attachment.read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition','attachment; filename= ' + filesToSend[counter] + fileExtension)

  #put all parts of the email together
  msg.attach(MIMEText(body,'plain'))
  msg.attach(part)
  email = msg.as_string()

  #server connection
  server = smtplib.SMTP('smtp.gmail.com',587)
  server.ehlo()
  server.starttls()
  server.login(loginMail, loginPassword)

  #Send email
  server.sendmail(loginMail,mailTo,email)
  server.quit

  print('Sent email to: ' + mailTo + '\t attachment: ' + filesToSend[counter] + fileExtension)
  counter = counter + 1 