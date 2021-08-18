from scrapper import Scrapper

URL = "https://habr.com/ru/all/"
KEYWORDS = ['дизайн', 'фото', 'web', 'python', '5']

if __name__ == "__main__":
    scrap = Scrapper(URL)

    [print(p) for p in scrap.posts if p.is_content_words(KEYWORDS)]
