import smtplib, ssl
import os

from email.message import EmailMessage


class SendMail:
   #For SSL
   port = 465

   SENDER_EMAIL = os.environ.get("MAIL_NAME")
   PASSWORD = os.environ.get("MAIL_PASS")
   from settings import receiver_mail
   RECEIVER_EMAIL = receiver_mail

   message = EmailMessage()

   def __init__(self) -> None:
      pass

   def setMessage(self, title: str, link):
      self.message["subject"] = "New Announcement From Eru"
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


def test():
   mail = SendMail()
   title = "test title"
   link = "https://www.google.com"
   mail.setMessage(title=title, link=link)
   mail.send()

if __name__ == "__main__":
   test()