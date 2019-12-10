import smtplib
from getpass import getpass
from email.mime.text import MIMEText
import datetime

def sendEmail():

    x = datetime.datetime.now()
    dateDay = x.strftime("%x")
    dateTime = x.strftime("%X")
    time_stamp = dateDay+' '+dateTime

    sender = 'deanrivers2@gmail.com'
    receiver = 'deanrivers2@gmail.com'

    content = 'Your bot experienced an error at: '+time_stamp
    password = 'Jogabonita!22'

    msg = MIMEText(content)

    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Twitterbot error notification at '+time_stamp

    print (msg)

    smtp_server_name = 'smtp.gmail.com'
    #port = '465' # for secure messages
    port = '587' # for normal messages

    if port == '465':
        server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
    else :
        server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
        server.starttls() # this is for secure reason

    server.login(sender, password)
    #server.login(sender, getpass(password))
    #server.send_message(msg)
    server.sendmail(sender,receiver,msg.as_string())
    server.quit()
    print ('Error message sent to '+receiver)