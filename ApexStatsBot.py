import time
import sys
import process
import mailer

#ongoing process
while(1>0):
    
    response = process.newProcess()
    print 'Send error email?: '+str(not response)
    
    #if the process came back with an error... send email
    if response==False:
        mailer.sendEmail()
    print ('Restarting Loop in 60s')    
    print ('')
    time.sleep(60)