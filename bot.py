#!/usr/bin/python
# -*- coding: utf-8 -*-

import Skype4Py
import time
import random

import sys
from PyQt4 import QtGui


""" 
CONFIGURE THE BOT BELOW 
"""

# TARGET USERNAMES (Skype-names of persons you don't want to chat with)
# put your set of target Skype-names into the square brackets like this:
# each answer into quotes, followed by a comma, exept in the end 
targets = ['yourfirsttarget1991', 'yoursecondtarget59', 'andSoOn']

# LIST OF ANSWERS to chose from if the incoming message ends with a question mark: "?"
# be careful when using single/double quotation marks resp. apostrophes! If you want to use them, 
# wrap the respective response with double-quotes, like this: ["that's true", 'another response without apostrophe']
question_answers = ['uhm', 'dunno', 'maybe try googling', 'have you asked sb else?', 'sorry, cant help you there', 'good question', 'mom']

# LIST OF ANSWERS to chose from if the message didn't end on an question mark
answers = ['yes', 'right', 'mhm', '[YOUR AD HERE!]', 'k', 'kk', "yes, that's common"]


# PROBABILTY TO RESPOND to a non-question-message – it's your choice. 
# 100 ==> everytime, smaller or equal to 0 ==> never
probability = 70

# TIME SPAN TO WAIT with your answer after you received a message (in seconds)
wait_min = 3
wait_max = 9

"""
END OF CONFIGURATION SECTION. If you don't know what you're doing, you should not change the below part. 
"""





# we need these two globals to prevent returning multiple answers in a row
# When we are waiting to send an answer, 
# we will answer no other messages that will receive us before our answer has been sent


def cur_millis():
	return int(round(time.time() * 1000))



def OnMessageStatus(Message, Status):
	
	# allow us to modify this list's content later on
	global last_answers
	
	# extract the skype-name of our beloved contact
	contact = Message._GetFromHandle()
	
	if Status == 'RECEIVED' and contact in targets:
		# we have just received a message from a person we have chosen to bot-chat with
		
		# the position of the target-skype-name in the configured array is the position of his entry in the "last_answers"-list
		target_index = targets.index(contact)

		# the content of the message we have just received
		content = Message._GetBody()
		
		# the pseudo-millisecond timestamp of the message
		msg_timestamp = int(round(Message._GetTimestamp()*1000))
		
		# print some information into the console, maybe someone wants to know
		print ("")
		print ("Received a message:             %s" % (content))
		print ("From the annoying user:         %s" % (contact))
		print ("His index in our target list:   %s" % (target_index))
		print ("Last answered at:               %s" % (last_answers[target_index]))
		print ("Timestamp of current msg:       %s" % (msg_timestamp))
		
		
		if (msg_timestamp-last_answers[target_index]) <= 0:
			# the message who triggered this function call has been sent before our last answer
			print ("We are already waiting to send an answer, so ignore this meanwhile received message.")
		
		else: 
			# fine! we have just received a message from a valid user and are not waiting to send another one
			answer = ""
			
			# if we have received a statement (no quoation mark in the end), we are not necessarily replying
			# p has to be above 0 to answer in this case
			# note: the random int goes only up to 99, as otherwise zero-result would be possible even if probability=100
			p = probability - random.randint(0, 99)
			
			#if content[-1:] == "?":
			if '?' in content:
				# it's a question, we are gonna respond in any case
				answer = question_answers[random.randint(0, (len(question_answers)-1))]
				print ("Answering a question:           %s" % (answer))
			
			elif p > 0:
				# it was no question, but the dice decided to send an answer
				answer = answers[random.randint(0, (len(answers)-1))]
				print ("Answering a statement:          %s" % (answer))
			
			else:
				# it was no question and the random calculation didn't work out. do nothing
				print ("Randomly calculated value based on chosen probability was too low: %s" % (p))
			
			
			if not answer == "": 
				# one of the above conditions was true, so we want to send an answer
				
				waiting_time = random.randint(wait_min, wait_max)
				target_labels[target_index].setText(contact+" [waiting %s seconds to reply]" % (waiting_time))
				print ("Waiting for %s seconds." % (waiting_time))
				time.sleep(waiting_time)
				
				s.SendMessage(contact, answer)
								
				last_answers[target_index] = cur_millis()
				print ("Sent this answer at millis:     %s" % (last_answers[target_index]))
				print ("Done.")
				
				target_labels[target_index].setText(contact)
				
				
# declare up the Qt-Application
app = QtGui.QApplication(sys.argv)

# set up the Skype-interface
s = Skype4Py.Skype()
s.Attach()
s.OnMessageStatus = OnMessageStatus

# this list will hold the last answer we have sent, for each target respectively
last_answers = []
for t in targets:
	last_answers.append(0)
	
	

# design the window, show it
widget = QtGui.QWidget()
widget.setWindowTitle('Skype Autoresponse Bot')
widget.setGeometry(200, 200, 400, 100)


grid = QtGui.QGridLayout()

# standard line of information
head_label = QtGui.QLabel('Skype-Bot is running on these contacts:\n\n', widget)
grid.addWidget(head_label, 0, 0)

# list all the targeted skype-names
i = 0
target_labels = []
for t in targets:
	i += 1
	target_labels.append(QtGui.QLabel(t, widget))
	grid.addWidget(target_labels[-1], i, 0)
	
# standard line ofinformation
bottom_label = QtGui.QLabel('\n\nClose window to quit the bot.', widget)
grid.addWidget(bottom_label, i+1, 0)

# complete the window
widget.setLayout(grid)
widget.show()



# quit application when window is closed
sys.exit(app.exec_())