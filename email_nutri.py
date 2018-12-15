# Imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

def Send(TO, MSG):
	''' Send a email message to the user '''
	'''
		Inputs:
		TO(str): email address of the recipient (user)
		MSG(message container): contains the text of the message to send

		Output
		None
	'''
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()

	# NB : the code won't work in the present version, because we didn't 
	# want to compromise the security by uploading the password on github
	server.login('NutriTeamADA@gmail.com', 'MOTDEPASSE')
	server.sendmail('NutriTeamADA@gmail.com', TO, MSG)
	server.quit()


def Send_rec(TO, text):
	''' '''
	'''
		Inputs:
		TO(str): email address of the recipient (user)
		text(str): text of the message to send

		Output
		None
	'''
	msg = MIMEMultipart()
	msg['From'] = 'NutriTeamADA@gmail.com'
	msg['To'] = TO
	#msg['Cc'] = 'NutriTeamADA@gmail.com'
	msg['Subject'] = "NutriTeamADA : Report"
	msg.attach((MIMEText(str(text), 'html')))
	#Send(['NutriTeamADA@gmail.com', TO], msg.as_string())
	Send([TO], msg.as_string())