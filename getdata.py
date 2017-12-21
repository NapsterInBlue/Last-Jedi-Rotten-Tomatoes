from operator import add

import requests

from bs4 import BeautifulSoup


BASEPAGE = 'https://www.rottentomatoes.com/m/star_wars_the_last_jedi/reviews/?page={}&type=user'

def get_reviews_on_page(soup):
    reviews = soup.find_all('div', {'class': 'row review_table_row'})
    return reviews

def get_stars_per_review(reviews):
    ratingField = lambda x: x.find_all('span', {'class':'fl'})
    stars = lambda x: len(x.find_all('span', {'class':'glyphicon glyphicon-star'}))
    halves = []
    for review in reviews:
        notBlank = ''.join([x.text for x in ratingField(review)]).strip()
        if notBlank:
            halves.append(.5)
        else:
            halves.append(0)

    totalStars = list(map(add, [stars(x) for x in reviews], halves))
    return totalStars

for i in range(1,4):
    html = requests.get(BASEPAGE.format(str(i))).text
    soup = BeautifulSoup(html, 'lxml')
    reviews = get_reviews_on_page(soup)
    stars = get_stars_per_review(reviews)
    print(stars)