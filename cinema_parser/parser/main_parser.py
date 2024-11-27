from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import asyncio
import sys, os
def get_chromedriver_path():
    if getattr(sys, 'frozen', False):
        # Если приложение запущено из скомпилированного файла
        chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver.exe')
    else:
        # Если приложение запущено из интерпретатора
        chromedriver_path = os.path.join('E:\\College\\b_labu\\lab10\\cinema_parser\\parser\\driver\\chromedriver-win64\\chromedriver.exe')  # Замените на ваш путь при разработке
    return chromedriver_path

class MovieParser:
    def __init__(self):

        #service = Service(".\\cinema_parser\\parser\\driver\\chromedriver-win64\\chromedriver.exe")
        chromedriver_path = get_chromedriver_path()
        service = Service(executable_path=chromedriver_path)
        options = Options()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=service, options=options)

    
    async def wait_for_page_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.movies"))
        )

    async def parse_movie_sessions(self, url):
        self.driver.get(url)
        await self.wait_for_page_load()

        await asyncio.sleep(2)

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        movie_divs = soup.find_all("div", class_="movie")

        movies = {}
        for movie_div in movie_divs:
            # Get movie title
            movie_name_tag = movie_div.find("a", class_="movie-name")
            if not movie_name_tag:
                movie_name_tag = movie_div.find("a", class_="tablet-movie-name")
            movie_name = movie_name_tag.text.strip()
            movie_url = movie_name_tag["href"]

            # Find movie poster image link (icon link)
            movie_img_tag = movie_div.find("img", class_="poster")
            if movie_img_tag:
                movie_icon_url = movie_img_tag["srcset"].split(" ")[0]
            else:
                movie_icon_url = ""

            # Parse sessions by date and technology
            movie_info_section = movie_div.find("section", class_="movie-info")
            dates = movie_info_section.find_all("div", class_="date")
            sessions_by_date = {}

            for date_section in dates:
                date = date_section.find("div", class_="showtime-date").text.strip()
                technologies = date_section.find_all("div", class_="tech")

                tech_sessions = {}
                for tech in technologies:
                    tech_title = tech.find("span", class_="technology-title").text.strip()
                    session_buttons = tech.find_all("button", class_="chips")

                    # Collect times for sessions
                    times = [button.text.strip() for button in session_buttons if not button.has_attr("disabled")]
                    tech_sessions[tech_title] = times

                sessions_by_date[date] = tech_sessions

            # Save movie info
            movies[movie_name] = {
                "url": movie_url,
                "sessions": sessions_by_date,
                "icon_url": movie_icon_url
            }

        return movies

    def close(self):
        self.driver.quit()