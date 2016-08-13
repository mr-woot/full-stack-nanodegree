from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "ACf686c75dd5aa91404c150c59dee0d938" 
AUTH_TOKEN = "aaaa97b43b961e2c0e61563653b968ce" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(    
) 
