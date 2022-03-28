from bs4 import BeautifulSoup
import requests
import json

BASE_URL = "https://ogrisl.erciyes.edu.tr/"

class Announcement(dict):
    """
    There is just one difference between Announcement and dict classes: name.
    """
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

class News:

    def __init__(self) -> None:
        pass

    def getData(self, url: str = BASE_URL) -> requests.models.Response:
        """
        Obtain all you need datas from the given url.
        """
        responce = requests.get(url)
        return responce

    def parseData(self, text: str) -> Announcement:
        announcements = dict()

        soup = BeautifulSoup(text, "html.parser")
        news_ul = soup.find("div", {"class": "DuyuruSatirlar"}).find("ul")
        news = news_ul.find_all("li")

        for nmr, li in enumerate(news, start=1):
            announcements[nmr] = {"date": li.i.get_text(), 
                                "title": li.a.get_text(),
                                "link":li.a.get("href")}
            
        return Announcement(announcements)

    def saveAsJson(self, news: Announcement | dict):
        """
        Save as json all the just obtained the new news.
        """
        def swapJsons():
            """
            Before save the new datas save the old datas in old_news.json
            """
            with open("new_news.json", "r", encoding="utf-8") as n_outfile:
                data = json.load(n_outfile)
                data = json.dumps(data, indent=4)
                with open('old_news.json', 'w', encoding="utf-8") as o_outfile:
                    o_outfile.write(data)

        def saveJson():
            data = json.dumps(news, indent=4)
            with open("new_news.json", "w", encoding="utf-8") as file:
                file.write(data)
                
        swapJsons()
        saveJson()

    @property
    def run(self) -> None:
        """
        This is where run this News
        """
        page_html = self.getData().text
        news = self.parseData(page_html)
        self.saveAsJson(news)

if __name__ == "__main__":
    new_news = News().run

    #print(type(news))
    #print(dir(news))