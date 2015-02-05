"""Script to list the wining movies of the Academy Awards along with their budget"""
import sys
import requests
import logging
import urllib.parse as urlparse
import re
from bs4 import BeautifulSoup
from Movie import  Movie
from CustomDevise import CustomDevise
from Budget import Budget

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

    for year, data in movies.items():
        logger.debug("Year: " + year + ", Title: " + data['title'] + ", budget: [dolls:" + str(data['budget']['dollars']) + ", pounds: " + str(data['budget']['pounds']) + "]")

def get_winning_movies(url):
    """Get the list of Movie Titles, the year of the award and the URL of the wikipedia permalink"""
    response = requests.get(url)
    movies = {}
    #logger.debug(response)

    k = 0
    for table in BeautifulSoup(response.text).select('.wikitable'):
      if k < 10:
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

        movies[award_year] = {}
        movies[award_year]['url'] = movie_url
        movies[award_year]['title'] = movie_title
        movies[award_year]['budget'] = budget

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
    
    #TODO: GET CURRENCY

    return extractBudget(budget)

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
        result = years[0].encode_contents().decode("utf-8")
        logger.debug(result)
    else:
        k = 0
        for year in years:
            if k == 0:
                result += str(year.encode_contents().decode("utf-8"))
            else:
                result += " - " + str(year.encode_contents().decode("utf-8"))
            k += 1

    return result

def absolutePath(relative_path, domain = WIKI_URL):
    url = urlparse.urljoin(domain, relative_path)
    logger.debug(url)
    return url

def extractBudget(budgetText):
    #Get beginning: $, US$ or £
    #p = re.compile(r'(\d+,)*')
    #p = re.compile(r'£\d{1,3}(?:\,\d{3})+(?:\.\d{2})?')
    if re.match(r'\$(\d+(?:\,\d{0,3})*(?:\.\d{0,3})* million)', budgetText):
      dolls = cleanNumber(re.findall(r'\$(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*)', budgetText)[0]) * 1000000
    elif re.match(r'\$(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText):
      dolls = cleanNumber(re.findall(r'\$(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText)[0])
    else:
      dolls = '' 

    if re.match(r'£(\d+(?:\,\d{0,3})*(?:\.\d{0,3})* million)', budgetText):
      pounds = cleanNumber(re.findall(r'£(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*)', budgetText)[0]) * 1000000
    elif re.match(r'£(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText):
      pounds = cleanNumber(re.findall(r'£(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText)[0])
    else:
      pounds = ''

    # if re.match(r'£(\d+ million)', budgetText):
    #   pounds = cleanNumber(re.findall(r'£(\d+)', budgetText)[0]) * 1000000
    # elif re.match(r'£(\d+(?:\,\d{3})+|\d+)', budgetText):
    #   pounds = cleanNumber(re.findall(r'£(\d+(?:\,\d{3})+|\d+)', budgetText)[0])
    # else:
    #   pounds = ''

    if dolls == '' and pounds == '':
      logger.warning('NO BUDGET FOUND' + budgetText)

    budget = {'dollars': dolls, 'pounds': pounds}
    logger.debug(budget)
    #logger.debug('dolls' + dolls)
    #logger.debug('pounds' + pounds)
    return budget
    
def cleanNumber(string):
    return int(float(string.strip().replace(',','')))

if __name__ == '__main__':
    #get_budget(absolutePath('/wiki/Wings_(1927_film)'))
    #main()
    #printKeys()

    #TODO: PUT THAT IN TESTS
    budgets = [
    "$6 million[1][2]", 
    "$750,000[1]", 
    "$1,650,000", 
    "$1,985,000[1]", 
    "£8 million ($15 million)[3]", 
    "US$1,644,736 (est.)", 
    "$2,840,000.[2]", 
    "£527,530[1]", 
    "£3 million",
    "£3.1 million",
    "$3.1 million"
    ]

    #logger.debug(budgets)
    #result = []
    #for budget in budgets:
    #    result.append(extractBudget(budget))

    #logger.debug(result)
    usd = CustomDevise('USD', 1000000)
    gbp = CustomDevise('GBP', 20000)
    budget = Budget(usd)
    budget.addPrice(gbp)
    movie = Movie('My Title', budget, '/super/movie')
    logger.debug(str(movie))
