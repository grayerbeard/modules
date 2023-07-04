#!/usr/bin/en7v python3
# -*- coding: utf-8 -*-

# title           :textBuffer.py
# description     :Rotating Buffer display and logging
# author          :David Torrens
# start date      :29 11 2019
# version         :25 12 2022
# python_version  :3

# Standard library imports
from datetime import datetime
from shutil import copyfile
from sys import exit as sys_exit
from time import sleep as timeSleep
import os
import json

###
#Tasks
# sort out display anomolies
# incorporate esending to influx db
# add better top of page live data display

# Local application imports
from utility import pr,makeTimeText,sendByFtp,fileExists,prd
from bufferLog import class_buffer_log
from utility import prd as debugPrint

#class class_bufXferPosn(object):

	# Rotating Buffer Posn Class
	#def __init__(self,config):


class class_text_buffer(object):
	# Rotating Buffer Class
	# Initiate with just the info in config file 
	# Get data with just a position in buffer Parameter
	def __init__(self,config,logTime):
		#initialization
		self.c = config
		self.debug = self.c.data.get("Debug",False)
		self.c.scanDelay = self.c.data["Scan"]["scanDelay"]
		self.c.textBufferLength = self.c.data["Log"]["textBufferLength"]
		self.c.headings = self.c.data["Log"]["headings"]
		self.c.addToHtmlFile = self.c.data["Log"]["addToHtmlFile"]
		self.c.localDirWww = self.c.data["Log"]["localDirWww"]
		self.c.ftp_credsFileName = self.c.data["Log"]["ftp_credsFileName"]
		self.c.logBufferFlag = self.c.data["Log"]["logBufferFlag"]
		self.c.logDirectory = self.c.data["Log"]["logDirectory"]
  
		self.debug = True

		if self.c.scanDelay > 9:
			refreshTime = self.c.scanDelay
		else:
			refreshTime = 0.9*self.c.scanDelay

		debugPrint(self.debug,f'Buffer Init for appname is {self.c.appName} and functionName of {self.c.functionName} with a size of {self.c.textBufferLength}and  width of {len(self.c.headings)}')

		if not os.path.exists('log'):
			os.makedirs('log')

		self.lineValues = {}

		for heading in self.c.headings:
			self.lineValues[heading]  =  "-"
		self.email_html = "<p> No Log yet </p>"
		self.dta = [ [ ".." for di in range(len(self.c.headings)) ] for dj in range(self.c.textBufferLength+1) ]
		self.htmlFileName = self.c.functionName + "_" + self.c.addToHtmlFile + ".html"
		self.htmlFileNameSaveAs = self.c.progPath + self.htmlFileName
		self.wwwFileName = self.c.localDirWww + "/" + self.htmlFileName
		
		if self.c.debug:
			print("HTML FileName : ",self.htmlFileName)
			print("HTML FileName save as : ",self.htmlFileNameSaveAs)
			print("WWW Web FileName : ",self.wwwFileName)

		try:
			self.ftpCreds = self.c.ftp_credsFileName
		except:
			self.ftpCreds = ""
		self.sendHtmlCount = 0
		self.logFile = ""
		if self.c.logBufferFlag:
			self.sendLogCount = 0
			self.log = class_buffer_log(self.c,logTime)
		else:
			self.semdLogCount = 0

		# Create all the Parts of the HTML File that will Create an HTML Table
		self.fileStart = """<head>
<meta http-equiv="refresh" content=""" + str(refreshTime) \
	 + """ / </head>
<caption>Rotating Buffer Display</caption>"""

		self.tblStart = """ <p><table style="float: left;" border="1">
<tbody>"""

		self.tblStartLine = """<tr>"""

		self.tblEndLine = """</tr>"""

		self.tblStartCol = """<td>"""

		self.tblEndCol= """</td>"""

		self.tblEnd = """</tbody></table>"""

		self.fileEnd = """</body></html>"""

		# Set up initial conditions for the buffer posn related
		
		self.bufferMaxSize	= self.c.textBufferLength + 1
		# where the most recent data will be after current update
		# this is also where the newset data will be
		self.mostRecentPosn = 0
		# where the oldest data will be after current update update
		self.oldestPosn = 0
		# The currect size of the buffer, always less than or equal to buffer length
		self.usedSize = 1
		###########
		self.whatShownOffset= 0

	def incrementDataPointer(self,pointer):
		# Move any pointer on one step in buffer allowing for nust go back to start if reaches the end
		if pointer < (self.bufferMaxSize - 1):
			pointer += 1
		else:
			pointer = 0
		return pointer

	def update(self,saveThis):
		if saveThis and (self.usedSize == self.bufferMaxSize):
			self.mostRecentPosn = self.incrementDataPointer(self.mostRecentPosn)
			self.oldestPosn = self.incrementDataPointer(self.oldestPosn)
			self.whatShownOffset= 1
		elif self.usedSize < self.bufferMaxSize:
			self.usedSize += 1
			self.mostRecentPosn += 1
			self.oldestPosn = 0
			self.whatShownOffset= 1
		else: #self.whatShownOffset== 1:
			self.whatShownOffset= 0


	def dataPosn(self,index):
		if self.usedSize == self.bufferMaxSize:
			# Buffer is full calculate based on position of start and end of current data
			dataPosition = self.mostRecentPosn - index
			if dataPosition < 0:
				# so item wanted is in top section
				dataPosition = self.usedSize + dataPosition
			return dataPosition
		else:
			# self.usedSize must be less than buffer size
			if index >  self.usedSize:
				print("Error in buffer index")
				print("Size is : ",self.usedSize, " Index is : ",index)
				sys_exit()
			else:
				return self.usedSize - index - 1


	def updateBuffer(self,saveThis):
		i = 0
		for heading in self.c.headings:
			self.dta[self.mostRecentPosn][i] = str(self.lineValues[heading])
			i += 1
		self.update(saveThis)

		if self.c.logBufferFlag and saveThis:
			self.log.logToFile(self.lineValues)

			if fileExists(self.wwwFileName):
				self.log.copyLogToWww(False)
			if self.sendLogCount > 10 and fileExists(self.ftpCreds):
				self.log.sendLogByFtp(False,self.c.logDirectory,self.c.ftpTimeout)
				self.send_logCount = 0
			elif fileExists(self.ftpCreds):
				self.sendLogCount += 1
			else:
				self.sendLogCount = 0

	def pr(self,saveThis,logTime):
		here = "buffer.pr for " + self.c.functionName

		forScreen = ""
		for heading in self.c.headings:
			forScreen += " " + str(self.lineValues[heading])
		print(forScreen)

		self.updateBuffer(saveThis)

		with open(self.htmlFileName,'w') as htmlFile:

			htmlFile.write(self.fileStart)

			# If we are logging to file then add info at top of file on log file
			if self.c.logBufferFlag:
				self.logFile = self.c.logDirectory + self.log.logFileName
				htmlFile.write('<p>' + self.htmlFileName + ' : ' + 
					makeTimeText(logTime)  + '      ' +
					'<a href= "' + self.logFile + 
					'" target="blank"> View CSV Log File </a></p>\n<p>')
			else:
			
			# If not then just info on HTML file
				htmlFile.write("<p>" + self.htmlFileName + " : " + 
					makeTimeText(logTime)  + "</p>\n<p>")

			# Write the start of the file
			htmlFile.write(self.tblStart + self.tblStartLine)
			self.emailHtml = self.tblStart + self.tblStartLine

			# Write the headings
			for heading in self.c.headings:
				htmlFile.write(self.tblStartCol + heading + self.tblEndCol)
				self.emailHtml = self.emailHtml + self.tblStartCol + heading + self.tblEndCol
			htmlFile.write(self.tblEndLine)
			self.emailHtml += self.tblEndLine

			# Write the data into the table
			for ind in range(self.whatShownOffset,self.usedSize+self.whatShownOffset-1):

				# get what line from the rotating buffer is required
				lineInd = self.dataPosn(ind)

				# Write one line
				htmlFile.write(self.tblStartLine)
				self.emailHtml +=  self.tblStartLine
				for i in range(len(self.c.headings)):
					
					htmlFile.write(self.tblStartCol + str(self.dta[lineInd][i]) + self.tblEndCol)
					self.emailHtml += self.tblStartCol + str(self.dta[lineInd][i]) + self.tblEndCol

				htmlFile.write(self.tblEndLine)
				self.emailHtml = self.emailHtml + self.tblEndLine

			# Write the end of the table and the file
			htmlFile.write(self.tblEnd)
			self.emailHtml = self.emailHtml + self.tblEnd
			htmlFile.write(self.fileEnd)
			self.emailHtml = self.emailHtml + self.fileEnd
		
		try:
			# Try to Copy the file to the WWW directory 
			if saveThis != True:	
				copyfile(self.htmlFileName, self.wwwFileName)
		except:
			print("Not able to copy : ",self.htmlFileName, " to ", self.wwwFileName)
				
		# Send file by FTP
		if fileExists(self.ftpCreds):
			if self.sendHtmlCount >= 3:
				# To debug FTP change end of following line to " = True"   !!!!!!!!!!!! 
				FTPdbugflag = False
				ftpresult = sendByFtp(FTPdbugflag,self.ftpcreds, self.htmlFileNamesaveas, self.htmlFileName,"",self.c.ftptimeout)
				for presind in range(0,len(ftpresult)):
					pr(FTPdbugflag,here, str(presind) + " : ", ftpresult[presind])
				self.sendhtmlcount = 0
			else:
				self.sendhtmlcount += 1
		return


# test routine run when script run direct
if __name__ == '__main__':
	from configTextBufferTest import class_config
	config = class_config("configTextBufferTest")
	self.c.scancount = 0
	logTime = datetime.now()
	logType = "log"
	logBuffer = class_text_buffer(config,logTime)
	
	saveThis = True
	message = ""
	reason = ""

	occ = 0
	twice = 0
	occCount = 0

	while (self.c.scanCount <= self.c.maxScans) or (self.c.maxScans == 0):

# Headings are:    Time,Count,Hour In Day,Position,Heading5,Heading6,Reason,Message

		# Sort out Time in Day and Day in week etc
		logTime= datetime.now()
		dayInWeek = logTime.weekday()
		hourInDay = logTime.hour + (logTime.minute/60)
		logBuffer.lineValues["Time"] = makeTimeText(logTime)
		logBuffer.lineValues["Count"] =  str(self.c.scanCount)
		logBuffer.lineValues["Hour In Day"] = round(hourInDay,2)
		logBuffer.lineValues["Position"] = str(logBuffer.mostRecentPosn)
		logBuffer.lineValues["Heading5"] = "head5"
		logBuffer.lineValues["Heading6"] = "head6"
	

		if (self.c.scanCount < 3): 
			saveThis = True
			reason += "Start "
			prd(self.c.debug,"Reason: ",reason)	

		if (self.c.scanCount > 4) and occ < 5:
			occ += 1
		elif (self.c.scanCount > 4):
			saveThis = True
			reason += "O" + str(occCount)
			occ = 0
			occCount += 1

		twice += 1
		if twice == 13:
			saveThis = True
			reason += "T1"
		elif twice == 14:
			saveThis = True
			reason += "T2"
			twice = 0

		logBuffer.lineValues["Reason"] = reason
		logBuffer.lineValues["Message"] = message


		logBuffer.pr(saveThis,logTime)
		saveThis = False
		reason = ""
		message = ""

		self.c.scanCount += 1

		timeSleep(self.c.scanDelay)	
