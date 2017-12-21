from operator import add
import pickle
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

def get_comments_per_review(reviews):
    allComments = []
    for review in reviews:
        try:
            comment = review.find_all('div')[4].text.split('  ')[2]
        except:
            comment = ''
        allComments.append(comment)

    return allComments


def get_all_of_the_data(numPages):
    allStars = []
    allComments = []
    for i in range(1, numPages):
        html = requests.get(BASEPAGE.format(str(i))).text
        soup = BeautifulSoup(html, 'lxml')
        reviews = get_reviews_on_page(soup)
        if len(reviews) == 0:
            print('Stopped being able to see pages on loop {}'.format(i))
            break
        allStars.extend(get_stars_per_review(reviews))
        allComments.extend(get_comments_per_review(reviews))
    return list(zip(allStars, allComments))

if __name__ == '__main__':
    data = get_all_of_the_data(1000)
    f = open('datadump.pkl', 'wb')
    pickle.dump(data, f)
    f.close()