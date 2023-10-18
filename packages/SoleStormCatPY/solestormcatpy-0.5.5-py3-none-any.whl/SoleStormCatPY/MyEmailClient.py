"""This Tool Sends emails through your email client. During first setup, you'll be asked to set up your account via the terminal.
To Run this, run:
import SoleStormCatPY.MyEmailClient as sscEmail
sscEmail.emailClient()
"""

"These modules are required for the app to run correctly"
import smtplib
import ssl

"This Gets The Email info from the email file"
def getEmailInfo():
	try:
		"Finds the file"
		emailfile = open('.solestormcatEmail.txt', 'x')
		
		"Runs if the email file (.solestormcatEmail.txt) is not found"
		print('The Main file for the email client does not exist. Creating file. You will be asked questions about your email info.')
		
		email = input('What is the email that you want to use?     ')
		
		password = input('What is the password to this email?   ')
		
		server = input('What is the site of the server (not including the port number)   ')

		port = input('What is the port to your email server?   ')
		
		emailfile.writelines([email,"\n",password,"\n",server,"\n",port])
		
		print('Email File Created!')
		"This then points back to the emailClient() code"
		
	except FileExistsError:
		"Runs if the file is found"
		print('Email File Found!')
		"This then points back to the emailClient() code"
		

def emailClient():
	"Makes sure that the email file exists"
	print("Reading Email File...")
	getEmailInfo()
	
	"Opens the email file, gathers info."
	emailfile = open('.solestormcatEmail.txt', 'r')
	
	def readEmailFile(file,x):
		"From https://stackoverflow.com/a/7523061"
		for index,line in enumerate(iter(file)):
			if index+1 == x: return line

		return None
    	
	myemail = readEmailFile(emailfile,1)
	mypassword = readEmailFile(emailfile,2)
	server = readEmailFile(emailfile,3)
	port = readEmailFile(emailfile,4)
	
	"Closes File, gives conformation"
	emailfile.close()
	print('Email Info has been gotten!')
	
	"Attempts to connect to server"
	context = ssl.create_default_context()
	
	try:
		smtp_server = smtplib.SMTP(server,port)
		smtp_server.connect()
		smtp_server.ehlo()
		smtp_server.starttls(context=context)
		smtp_server.ehlo()
		smtp_server.login(myemail,mypassword)
		
		"This is where the email gets created!"
		print('Connection to server secured!')
		print(' ')
		
		friend_email = input('Who is this email for?    ')
		subject = input('What is the subject of the email?    ')
		body = input('What is the body of the email?       ')
		message = """\
		Subject:""",subject,"""
		
		
		""",body
		
		print('''Here is your message info:
		''','Email being sent to: ',friend_email,'''
		''','''Subject and Body:
		''',message)
		print(' ')
		print('The message is being sent')
		
	except Exception as e:
		"This works if an error has occured"
		print('There was an error. Error info is below:')
		print(e)
