import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

if len(sys.argv) != 4 and len(sys.argv) != 5:
    print("Usage: mail.py <recipient email> <title> <template name> <Optional user_id>")
    exit(1)
else:
    recipient = sys.argv[1]
    title = sys.argv[2]
    templateName=sys.argv[3]
    if(len(sys.argv)==5):
        user_id=sys.argv[4]
        
    

file = open("email_templates/"+templateName, "r")
html_content = file.read()

# Update Content if {ID}  are in the email content
if "{ID}" in html_content:
    html_content = html_content.replace("{ID}", f"{int(user_id):02d}")

message = Mail(
    from_email="Your new important friend {SENDER_EMAIL}",
    to_emails= recipient,
    subject=title,
    html_content=html_content
)
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
