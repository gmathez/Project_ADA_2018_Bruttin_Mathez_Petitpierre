import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

def Send(TO, MSG):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login('NutriTeamADA@gmail.com', 'BruMatPet2018#')
	server.sendmail('NutriTeamADA@gmail.com', TO, MSG)
	server.quit()

def Send_Recommandation(TO, text):
        msg = MIMEMultipart()
        msg['From'] = 'NutriTeamADA@gmail.com'
        msg['To'] = TO
        msg['Cc'] = 'NutriTeamADA@gmail.com'
        msg['Subject'] = "NutriTeamADA : Recommandation"
        msg.attach((MIMEText(str(text), 'plain')))
        Send(['NutriTeamADA@gmail.com', TO], msg.as_string())