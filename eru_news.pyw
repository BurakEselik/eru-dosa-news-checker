"""
Aim of this program: 
Get announcements and news from https://ogrisl.erciyes.edu.tr
And send mail to given e-mail address that the latest announcement.
"""

#date: 3 march 2022
#author: BurakEselik
import json
import news
import mail
from news import BASE_URL
from time import sleep
#import webbrowser


def getDifferenceNumber() -> int:
    with open("old_news.json", "r", encoding="utf-8") as old_news, open("new_news.json", "r", encoding="utf-8") as new_news:
        old = json.load(old_news)
        new = json.load(new_news)
        for i in range(1, 11):
            if old["1"]["date"] == new[str(i)]["date"] and old["1"]["title"] == new[str(i)]["title"]:
                return i


def setContent(df_number) -> dict:
    content_dict = dict()
    with open("new_news.json", "r", encoding="utf-8") as new_news:
        new = json.load(new_news)
        for i in range(1, df_number):    
            content_dict[str(i)] = new[str(i)]
    return content_dict


def sendMail(content_dict: dict) -> None:
    new_mail = mail.SendMail()
    for i in range(1, len(content_dict)+1):
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
        #webbrowser.open("https://youtube.com")
    else:
        #webbrowser.open("https://cleantecharticles.com")
        pass


if __name__ == "__main__":
    while 1:
        main()
        from settings import repeat_control_timer
        timer = repeat_control_timer
        sleep(timer)