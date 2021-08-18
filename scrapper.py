from bs4 import BeautifulSoup
import requests
import regex as re

PREFIX = "tm-article"


class Post:
    def __init__(self, header, link, date, description):
        self.header = header
        self.link = link
        self.description = description
        self.date = date
        self.text = self.__parse_post()

    def __parse_post(self):
        html = BeautifulSoup(requests.get(self.link).text, 'lxml')
        text_html = html.find('div', class_='article-formatted-body').find('div')
        return text_html.text

    def __str__(self):
        return f'{self.date} || {self.header} || {self.link}'

    def is_content_words(self, words):
        for w in words:
            pattern = re.compile(fr"\b{w}\b", re.IGNORECASE)
            if pattern.search(self.text) or pattern.search(self.description) or pattern.search(self.header):
                return True
        return False


class Scrapper:
    url_pattern = re.compile(r"([\s\S]*\.[\S]{2,5})/")

    def __init__(self, url):
        self.url = url
        self.html = BeautifulSoup(requests.get(url).text, 'lxml')
        self.posts_html = self.html.findAll('article', class_=f"{PREFIX}s-list__item")
        self.posts = self.__parse_posts()

    @staticmethod
    def __extract_base_url(url):
        base_url = Scrapper.url_pattern.match(url)
        if base_url is None:
            return ''
        return base_url.groups()[0]

    @staticmethod
    def __is_url_relative(url):
        return Scrapper.__extract_base_url(url) == ''

    def __parse_posts(self):
        posts = []
        for p in self.posts_html:
            header_html = p.find('h2', class_=f"{PREFIX}-snippet__title")
            header = header_html.find('span').text
            link = header_html.find('a', class_=f"{PREFIX}-snippet__title-link")['href']
            if Scrapper.__is_url_relative(link):
                link = f'{Scrapper.__extract_base_url(self.url)}{link}'
            date = p.find('time')['datetime']
            description = p.find('div', class_="article-formatted-body").text

            posts.append(Post(header, link, date, description))

        return posts

