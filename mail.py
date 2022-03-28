import smtplib, ssl
import os
import json
from email.message import EmailMessage


class SendMail:
   #For SSL
   port = 465

   SENDER_EMAIL = os.environ.get("MAIL_NAME")
   PASSWORD = os.environ.get("MAIL_PASS")

   message = EmailMessage()

   def __init__(self) -> None:
      with open("settings.json", "r", encoding="utf-8") as settings:
         setting = json.load(settings)
      self.RECEIVER_EMAIL = setting["receiver_mail"]

   def setMessage(self, title: str, link, subject="New Announcement From Eru"):
      self.message["subject"] = subject
      self.message["From"] = self.SENDER_EMAIL
      self.message["To"] = self.RECEIVER_EMAIL
      plain_text = f"Yeni bir duyuru var: {title} {link}"
      self.message.set_content(plain_text)

   #Create a secure SSL context
   context = ssl.create_default_context()

   def send(self):
      
         with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            try:
               server.login(self.SENDER_EMAIL, self.PASSWORD)
               server.send_message(self.message)
            except Exception as e:
               print(e) #Fix here shouldn't seen on cmd.
            finally:
               server.quit()
               del self.message["To"], self.message["subject"], self.message["From"]


def test():
   mail = SendMail()
   title = "test title"
   link = "https://www.google.com"
   mail.setMessage(title=title, link=link)
   mail.send()

if __name__ == "__main__":
   test()