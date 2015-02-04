"""Script to list the wining movies of the Academy Awards along with their budget"""
import sys
import requests
import logging
import urllib.parse as urlparse
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# create a file handler
handler = logging.FileHandler('hello.log')
handler.setLevel(logging.DEBUG)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

WIKI_URL = "http://en.wikipedia.org/"
AA_URL = "http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture" 

def main():
    """Main entry point for the script."""
    movies = get_winning_movies(AA_URL)
    logger.debug(movies)

def printKeys():
    movies = get_winning_movies(AA_URL) 

    logger.debug(movies)

    for title, data in movies.items():
        logger.debug("Title: " + title + " - budget " + data['budget'])

def get_winning_movies(url):
    """Get the list of Movie Titles, the year of the award and the URL of the wikipedia permalink"""
    response = requests.get(url)
    movies = {}
    #logger.debug(response)

    k = 0
    for table in BeautifulSoup(response.text).select('.wikitable'):
      #if k == 0:
      #Extract year of the award
      years = table.find('caption').find('big').findChildren('a', recursive=False)
      logger.debug(years)
      award_year = formatYear(years)

      #logger.debug(award_year)



      #Extract Movie URL
      line = table.select('tr')[1].select('a')
      #logger.debug(line)
      movie_url = line[0]['href']
      movie_title = line[0]['title']
      #logger.debug(movie_url)
      logger.debug(movie_title)

      budget = get_budget(absolutePath(movie_url))

      movies[movie_title] = {}
      movies[movie_title]['url'] = movie_url
      movies[movie_title]['title'] = movie_title
      movies[movie_title]['year'] = award_year
      movies[movie_title]['budget'] = budget

      #logger.debug(s_movies)
      k += 1
    return movies

def get_budget(movie_url):
    """Get the budget for each movie, based on wikipedia permalink"""
    response = requests.get(movie_url)
    #logger.debug(response)

    box =  BeautifulSoup(response.text).select('.infobox')[0]
    #logger.debug(box)
    if box.find('th', text='Budget'):
        budget_tag = box.find('th', text='Budget').parent()[1]
        logger.debug(budget_tag)
        budget = budget_tag.text
    else:
        budget = 'NO BUDGET'
    #logger.debug(budget)

    return str(budget)

    #for elem in BeautifulSoup(response.text).select('.infobox')[0].select('tr'):

    #    logger.debug('ELEM')
    #    logger.debug(elem)

    #    if elem.select('th').contents == 'Budget':
    #        budget = elem.find('td').findChildren('a', recursive= False)
    ##        logger.debug(budget)



    pass

def average_budget(movies):
    """Calculates the average buget spent on winning movies since the creation"""
    pass

def formatYear(years):
    result = ""
    if len(years) == 1:
        result = years[0] 
    else:
        k = 0
        for year in years:
            if k == 0:
                result += str(year.contents)
            else:
                result += " - " + str(year.contents)
            k += 1

    return result

def absolutePath(relative_path, domain = WIKI_URL):
    url = urlparse.urljoin(domain, relative_path)
    logger.debug(url)
    return url

if __name__ == '__main__':
    #get_budget(absolutePath('/wiki/Wings_(1927_film)'))
    #main()
    printKeys()
