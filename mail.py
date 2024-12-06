import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

if len(sys.argv) != 4:
    print("Usage: mail.py <recipient email> <title> <template name>")
    exit(1)
else:
    recipient = sys.argv[1]
    title = sys.argv[2]
    templateName=sys.argv[3]

file = open("email_templates/"+templateName, "r")
html_content = file.read()

message = Mail(
    from_email="Your new important friend <gautier.leblanc@nutanix.com>",
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
