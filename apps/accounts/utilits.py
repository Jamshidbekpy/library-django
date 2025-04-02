import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import random

class EmailThreating(threading.Thread):
    def __init__(self, subject, body, to_email, content_type):
        self.subject = subject
        self.body = body
        self.to_email = to_email
        self.content_type = content_type
        threading.Thread.__init__(self)
        
    def run(self):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            to=[self.to_email]
                    )
        if self.content_type == "html":
            email.content_subtype = "html"
        email.send()
        
    
def send_mail_code(email, password):
    html_content = render_to_string(
        template_name="accounts/password_reset_email.html",
        context={
            'password':password
        }
    )
    subject ="Parol yangilandi"
    body = html_content
    to_email = email
    content_type = 'html'
    EmailThreating(subject, body, to_email, content_type).start()

    
CODE_LENGTH = 8


class GenerateNewPassword:
    def __init__(self):
        self.SIGN =['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    def new_password(self):
        random_code=random.sample(self.SIGN, k=CODE_LENGTH)
    
        result=''.join(random_code)
        return result


        