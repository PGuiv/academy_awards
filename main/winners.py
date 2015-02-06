"""Script to list the wining movies of the Academy Awards along with their budget"""
import sys
import requests
import urllib.parse as urlparse
import re
from bs4 import BeautifulSoup
import logging

from Movie import  Movie
from Amount import Amount
from Budget import Budget
from Award import Award

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


class AwardCrawler:

  awards = []
  top_domain = ''
  main_url = ''
  
  def __init__(self, top_domain = "http://en.wikipedia.org/", main_url = "http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"):
      self.top_domain = top_domain
      self.main_url = main_url
  
  def main(self):
      """Main entry point for the script."""
      self.awards = self.get_awards(self.main_url)
      logger.debug(str(self))
  
  def printKeys():
      movies = self.get_awards(self.main_url) 
  
      logger.debug(movies)
  
      for year, data in movies.items():
          logger.debug("Year: " + year + ", Title: " + data['title'] + ", budget: [dolls:" + str(data['budget']['dollars']) + ", pounds: " + str(data['budget']['pounds']) + "]")
  
  def get_awards(self, url):
      awards = []
      """Get the list of Movie Titles, the year of the award and the URL of the wikipedia permalink"""
      try:
          response = requests.get(url)
      except:
          logger.warning("Error with the URL: " + url)
  
      #movies = {}
      #logger.debug(response)
  
      k = 0
      for table in BeautifulSoup(response.text).select('.wikitable'):
        if k < 100:
          #Extract year of the award
          years = table.find('caption').find('big').findChildren('a', recursive=False)
          award_year = self.formatYear(years)
  
          #Extract Movie URL
          line = table.select('tr')[1].select('a')
          #logger.debug(line)
          movie_url = line[0]['href']
          movie_title = line[0]['title']
          #logger.debug(movie_url)
          logger.debug(movie_title)
  
          budget = self.getBudget(self.absolutePath(movie_url))
          winning_movie = Movie(movie_title, budget, movie_url) 
          if len(award_year) > 1:
            award = Award(winning_movie, award_year[0], award_year[1])
          else:
            award = Award(winning_movie, award_year[0])


          awards.append(award)

          k += 1

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
  
  def averageBudget(movies):
      """Calculates the average buget spent on winning movies since the creation"""
      pass
  
  @staticmethod
  def formatYear(years):
      result = []
      for year in years:
          result.append(str(year.encode_contents().decode("utf-8")))
  
      logger.debug(result[0])
      return result
  
  def absolutePath(self, relative_path):
      url = urlparse.urljoin(self.top_domain, relative_path)
      logger.debug(url)
      return url
  
  def formatBudget(self, budgetText):
      if re.match(r'\$(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*\smillion)', budgetText):
        doll_value = self.cleanNumber(re.findall(r'\$(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*)', budgetText)[0]) * 1000000
      elif re.match(r'\$(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText):
        doll_value = self.cleanNumber(re.findall(r'\$(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText)[0])
      else:
        doll_value = 0 
  
      doll_amount = Amount('USD', doll_value) 

      if re.match(r'£(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*\smillion)', budgetText):
        pound_value = self.cleanNumber(re.findall(r'£(\d+(?:\,\d{0,3})*(?:\.\d{0,3})*)', budgetText)[0]) * 1000000
      elif re.match(r'£(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText):
        pound_value = self.cleanNumber(re.findall(r'£(\d+(?:\,\d{3})+(?:\.\d{0,3})*|\d+(?:\.\d{0,3})*)', budgetText)[0])
      else:
        pound_value = 0

      pound_amount = Amount('GBP', pound_value) 
  
      if doll_value == '' and pound_value == '':
        logger.warning('NO BUDGET FOUND' + budgetText)
  
      budget = Budget([doll_amount, pound_amount])

      return budget
      
  @staticmethod
  def cleanNumber(string):
      return float(string.strip().replace(',',''))

  def __str__(self):
      result = ''
      for award in self.awards:
          result +=  " " + str(award) + "\n"

      return result

    

  
if __name__ == '__main__':
      #getBudget(absolutePath('/wiki/Wings_(1927_film)'))
      #AwardCrawler().main()
      #Crawler.printKeys()
  
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
      "$3.1 million",
      "US$2 million[4]",
      "$2.183 million",
      "$55 million",
      "$6-7 million"
      ]
  
      #logger.debug(budgets)
      #result = []
      #for budget in budgets:
      #    result.append(str(AwardCrawler().formatBudget(budget)))
  
      #logger.debug(result)

      #usd = Amount('USD', 1000000)
      #gbp = Amount('GBP', 20000)
      #budget = Budget(usd)
      #budget.addAmount(gbp)
      #movie = Movie('My Title', budget, '/super/movie')
      #logger.debug('TEST')
      #logger.debug(str(movie))
      #award = Award(movie, ['2014','2015'])
      #logger.debug(str(award))



      #usd1 = Amount('USD', 1000000)
      #usd2 = Amount('USD', 2000000)

      #budget1 = Budget(usd1)
      #budget2 = Budget(usd2)

      #logger.debug(str(budget1))
      #logger.debug(str(budget2))

      logger.debug(AwardCrawler().getBudget('http://en.wikipedia.org/wiki/Forrest_Gump'))
