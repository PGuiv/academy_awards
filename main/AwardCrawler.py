"""Script to list the wining movies of the Academy Awards along with their budget"""
import sys
import requests
import urllib.parse as urlparse
import re
from bs4 import BeautifulSoup

from Movie import  Movie
from Amount import Amount
from Budget import Budget
from Award import Award

import CustomLog
logger = CustomLog.setup_custom_logger('root', 'INFO')

class AwardCrawler:
    
    def __init__(self, top_domain = "http://en.wikipedia.org/", main_url = "http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"):
        self.awards = []
        self.top_domain = top_domain
        self.main_url = main_url
    
    def main(self):
        """Main entry point for the script."""
        self.awards = self.get_awards(self.main_url)
        self.calculateAverageBudgets()
        logger.info(str(self))
    
    def get_awards(self, url):
        """Get the list of Movie Titles, the year of the award and the URL of the wikipedia permalink"""
        awards = []
        try:
            response = requests.get(url)
        except:
            logger.warning("Error with the URL: " + url)
    
        for table in BeautifulSoup(response.text).select('.wikitable'):
    
            #Extract Movie URL
            tr = table.select('tr')[1]
            if tr.has_key('style') and re.findall('background:#FAEB86', tr['style']):
              line = table.select('tr')[1].select('a')
              movie_url = line[0]['href']
              movie_title = line[0].text
              logger.debug(movie_title)
    
              budget = self.getBudget(self.absolutePath(movie_url))
              winning_movie = Movie(movie_title, budget, movie_url) 
              years = table.find('caption').find('big').findChildren('a', recursive=False)
              award_year = self.formatYear(years)

              if len(award_year) > 1:
                  award = Award(winning_movie, award_year[0], award_year[1])
              else:
                  award = Award(winning_movie, award_year[0])


              awards.append(award)

        return awards
    
    def getBudget(self, movie_url):
        """Get the budget for each movie, based on wikipedia permalink"""
        try:
            response = requests.get(movie_url)
        except:
            logger.warning("Problem with the URL: " + movie_url)
    
        box =  BeautifulSoup(response.text).select('.infobox')[0]
        if box.find('th', text='Budget'):
            budget_tag = box.find('th', text='Budget').parent()[1]
            logger.debug(budget_tag)
            budget = budget_tag.text
        else:
            budget = ''
        logger.debug(budget)
        
        return self.formatBudget(budget)
    
    @staticmethod
    def formatYear(years):
        """Format the year"""
        result = []
        for year in years:
            result.append(str(year.encode_contents().decode("utf-8")))
    
        logger.debug(result[0])
        return result
    
    def absolutePath(self, relative_path):
        """Builds the URL based on relative path and main domain name"""
        url = urlparse.urljoin(self.top_domain, relative_path)
        logger.debug(url)
        return url
    
    def formatBudget(self, budgetText):
        """Builds Budget based on the value and currency found in the HTML"""
        logger.debug("budgetText %s", budgetText)
        if re.match(r'.*\W*\w*\$(\d+(?:\S\d+)*(?:\,\d{0,3})*(?:\.\d{0,3})*\smillion)', budgetText):
            doll_value = self.cleanNumber(re.findall(r'\W*\w*\$(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*)', budgetText)[0]) * 1000000
            logger.debug('Match the first dollar case %s', doll_value)
        elif re.match(r'\w*\$(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText):
            doll_value = self.cleanNumber(re.findall(r'\w*\$(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText)[0])
            logger.debug('Match the second dollar case %s', doll_value)
        else:
            logger.debug('No match in dollar %s', budgetText)
            doll_value = 0 
    
        doll_amount = Amount('USD', doll_value) 
        logger.debug("Here is the doll_value %s", doll_value)

        if re.match(r'\w*£(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*\smillion)', budgetText):
            pound_value = self.cleanNumber(re.findall(r'\w*£(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*)', budgetText)[0]) * 1000000
            logger.debug('Match the first pound case %s', pound_value)
        elif re.match(r'\w*£(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText):
            pound_value = self.cleanNumber(re.findall(r'\w*£(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText)[0])
            logger.debug('Match the second pound case %s', pound_value)
        else:
            logger.debug('No match in pounds %s', budgetText)
            pound_value = 0

        pound_amount = Amount('GBP', pound_value) 
    
        if doll_value == '' and pound_value == '':
            logger.warning('NO BUDGET FOUND' + budgetText)
    
        budget = Budget(doll_amount)
        budget.addAmount(pound_amount)

        return budget
        
    @staticmethod
    def cleanNumber(string):
        """Convert String to float"""
        return float(string.strip().replace(',',''))

    def getNoBudgetMovies(self):
        """Returns the list of movies with no budget"""
        empty_movies = []
        for award in self.awards:
            logger.debug(str(award))
            if award.winner.budget.getAmount(Budget().main_currency) == 0:
                logger.debug(str(award))
                empty_movies.append(award.winner)
        return empty_movies

    def calculateAverageBudgets(self):
        self.sortAwards()
        
        k = 0
        total_budget = 0
        for award in self.awards:
            if award.winner.budget.getAmount('USD').value != 0:
                k += 1
                total_budget += award.winner.budget.getAmount('USD').value

            if k > 0:
               award.average_budget = int(total_budget / k)
            else:
               award.average_budget = 0


    def sortAwards(self):
        self.awards = sorted(self.awards, key=lambda award: award.main_year)

    def __str__(self):
        result = ''
        for award in self.awards:
            result +=  " " + str(award) + " Average Budget: " + "{:,}".format(award.average_budget) + "\n" 

        return result

if __name__ == '__main__':
      award = AwardCrawler()
      award.main()
