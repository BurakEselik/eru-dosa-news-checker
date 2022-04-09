"""
Aim of this program: 
Get announcements and news from https://ogrisl.erciyes.edu.tr
And send mail to given e-mail address that the latest announcement.
"""

#date: 3 march 2022
#author: BurakEselik
import news
import mail
from news import BASE_URL
from time import sleep
import json
import datetime
from plyer import notification
import sys

def getDifferenceNumber() -> int:
    with open("old_news.json", "r", encoding="utf-8") as old_news, open("new_news.json", "r", encoding="utf-8") as new_news:
        old = json.load(old_news)
        new = json.load(new_news)
        for i in range(1, 11):
            if old["1"]["date"] == new[str(i)]["date"] and old["1"]["title"] == new[str(i)]["title"]:
                return i
        else:
            with open("log.txt", "a", encoding="utf-8") as log:
                log.write(f"\nLast announcements deleted or updated")
                notification.notify(
                    title="ERU NEWS",
                    message=" Last announcements deleted or updated "
                    timeout=90)
            return 0


def setContent(df_number) -> dict:
    content_dict = dict()
    with open("new_news.json", "r", encoding="utf-8") as new_news:
        new = json.load(new_news)
        for i in range(1, df_number):    
            content_dict[str(i)] = new[str(i)]
    return content_dict


def sendMail(content_dict: dict) -> None:
    for i in range(1, len(content_dict)+1):
        new_mail = mail.SendMail()
        title = content_dict[str(i)]["title"]
        link = BASE_URL[:-1] + content_dict[str(i)]["link"]
        new_mail.setMessage(title=title, link=link) 
        new_mail.send()


def main() -> None:
    new_news = news.News()
    new_news.run
    df_number = getDifferenceNumber()
    if df_number > 1:
        content_dict = setContent(df_number=df_number)
        sendMail(content_dict)
    else:
        current_time = datetime.datetime.now()
        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(f"\nThere is no new announcement: {current_time}")
            del current_time


if __name__ == "__main__":
    while 1:
        try:
            main()
            with open("settings.json", "r", encoding="utf-8") as settings:
                setting = json.load(settings)
                timer = setting["repeat_timer"]
                sleep(timer)
        except Exception as e:
            with open("log.txt", "a", encoding="utf-8") as log:
                log.write(f"\nProgram closed because of this error: {e}")
                notification.notify(
                title = "ERU NEWS STOPED",
                message=" Eru news checker program just closed! ",
                timeout=100)

            sys.exit()
