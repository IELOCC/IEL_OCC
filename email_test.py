import smtplib
import email

email = 'iel.datacollection@gmail.com'
password = 'ieloffice'

content = 'Hey thomas!!'

smpt = smtplib.SMTP('smtp.gmail.com:587')
smpt.ehlo()
smpt.starttls()
smpt.ehlo()
smpt.login(email,password)
content = "\r\n".join(["From: "+email,"To: trdougherty@utexas.edu","Subject: Just a message","","Why, oh why"])
smpt.sendmail(email,'trdougherty@utexas.edu',content)
smpt.quit()
