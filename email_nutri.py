import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

def Send(TO, MSG):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login('NutriTeamADA@gmail.com', 'MOTDEPASSE')
	server.sendmail('NutriTeamADA@gmail.com', TO, MSG)
	server.quit()


def Send_rec(TO, text):
	msg = MIMEMultipart()
	msg['From'] = 'NutriTeamADA@gmail.com'
	msg['To'] = TO
	#msg['Cc'] = 'NutriTeamADA@gmail.com'
	msg['Subject'] = "NutriTeamADA : Report"
	msg.attach((MIMEText(str(text), 'html')))
	#Send(['NutriTeamADA@gmail.com', TO], msg.as_string())
	Send([TO], msg.as_string())