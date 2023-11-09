from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
import logging

LINK_TO_PARSE = "https://www.trustpilot.com/review/www.google.com"

logging.basicConfig(encoding='utf-8', level=logging.INFO)

@dataclass
class ReviewProcessor:
    link_to_parse: str
    soup: BeautifulSoup = None

    def init_soup(self) -> None:
        response = requests.get(self.link_to_parse)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        logging.info("Soup is initiated")

    def get_rating(self) -> dict:
        rating_element = self.soup.find('span', class_='typography_heading-m__T_L_X')
        rating_text = rating_element.text.strip()
        return {"raiting": float(rating_text)}

    def get_total_review_count(self) -> dict:
        count_element = self.soup.find('p',  attrs={'data-reviews-count-typography': True})
        total_count = re.search(r">(\d*,*\d+)<", str(count_element))
        return {"total_review_count": total_count[1].replace(",", "")}

    def get_per_star_review_count(self) -> dict:
        star_rating = ["one", "two", "three", "four", "five"]
        review_counts_per_star = {}

        for star in star_rating:
            selector = self.soup.select(f'[data-star-rating={star}]')
            review_count = re.search('(title=")(\d*,*\d+)', str(selector))[2].replace(",", "")
            review_counts_per_star[star] = review_count

        return review_counts_per_star


# proc = ReviewProcessor(LINK_TO_PARSE)
# proc.init_soup()

# print(proc.get_per_star_review_count())
# print(proc.get_total_review_count())
# print(proc.get_rating())