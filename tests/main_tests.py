#/wiki/The_Broadway_Melody -> No budget
from Amount import Amount
from Award import Award
from AwardCrawler import AwardCrawler
from Budget import Budget
from Movie import Movie

class TestAwardCrawler:
    
    def test_amount_conversion(self):
        usd = Amount('USD', 1000000)
        converted = usd.getConvertedValue('GBP') 

        assert int(converted) == 650000

    def test_bugdget_add_amount_gbp(self):
        budget = Budget(Amount('USD', 0))
        budget.addAmount(Amount('GBP', 100))

        assert int(budget.getAmount('USD').value) == 153
        assert int(budget.getAmount('GBP').value) == 100

    def test_bugdget_add_amount_gbp_not_null_usd(self):
        budget = Budget(Amount('USD', 200))
        budget.addAmount(Amount('GBP', 100))

        assert int(budget.getAmount('USD').value) == 200
        assert int(budget.getAmount('GBP').value) == 100

    def test_bugdget_update_amount(self):
        budget = Budget(Amount('USD', 0))
        budget.addAmount(Amount('GBP', 100))

        budget.updateAmount(Amount('GBP', 200))

        assert int(budget.getAmount('USD').value) == 153
        assert int(budget.getAmount('GBP').value) == 200

    def test_bugdget_update_amount_not_set(self):
        budget = Budget(Amount('USD', 0))

        budget.updateAmount(Amount('GBP', 200))

        assert int(budget.getAmount('USD').value) == 306
        assert int(budget.getAmount('GBP').value) == 200

    def test_budget_regex(self):
          
        budgets = [
                  "$6 million[1][2]", 
                  "$750,000[1]", 
                  "$1,650,000", 
                  "$1,985,000[1]", 
                  "US$1,644,736 (est.)", 
                  "$2,840,000.[2]", 
                  "$3.1 million",
                  "US$2 million[4]",
                  "$2.183 million",
                  "$55 million",
                  "$6-7 million",
                  "$6–7 million[1][2]",
                  "£8 million ($15 million)[3]", 
                  "£527,530[1]", 
                  "£3 million",
                  "£3.1 million"
                  ]


        budgetgbp1 = Budget(Amount('USD', 15000000))
        budgetgbp1.addAmount(Amount('GBP', 8000000))

        budgetgbp2 = Budget(Amount('USD', 0))
        budgetgbp2.addAmount(Amount('GBP', 527530))
      
        budgetgbp3 = Budget(Amount('USD', 0))
        budgetgbp3.addAmount(Amount('GBP', 3000000))

        budgetgbp4 = Budget(Amount('USD', 0))
        budgetgbp4.addAmount(Amount('GBP', 3100000))
          
        expected_results = [
                  Budget(Amount('USD', "6000000")),
                  Budget(Amount('USD', "750000")),
                  Budget(Amount('USD', "1650000")),
                  Budget(Amount('USD', "1985000")),
                  Budget(Amount('USD', "1644736")),
                  Budget(Amount('USD', "2840000")),
                  Budget(Amount('USD', "3100000")),
                  Budget(Amount('USD', "2000000")),
                  Budget(Amount('USD', "2183000")),
                  Budget(Amount('USD', "55000000")),
                  Budget(Amount('USD', "6000000")),
                  Budget(Amount('USD', "6000000")),
                  budgetgbp1,
                  budgetgbp2,
                  budgetgbp3,
                  budgetgbp4
                  ]

        for idx, budget in enumerate(budgets):

            assert int(AwardCrawler().formatBudget(budget).getAmount('USD').value) == int(expected_results[idx].getAmount('USD').value)
            assert AwardCrawler().formatBudget(budget).getAmount('USD').currency == expected_results[idx].getAmount('USD').currency


    def test_amount_available_currencies(self):
        assert  Amount.AVAILABLE_CURRENCIES == ['USD', 'GBP']

    def test_crawl_sort_awards(self):

        budget = Budget(Amount('USD', 1000000))
        award1 = Award(Movie('title1', budget, '/link1'), 2014)
        award2 = Award(Movie('title2', budget, '/link2'), 2012)
        award3 = Award(Movie('title3', budget, '/link3'), 2015)

        crawl = AwardCrawler()

        crawl.awards.append(award1)
        crawl.awards.append(award2)
        crawl.awards.append(award3)

        assert crawl.awards == [award1, award2, award3]

        crawl.sortAwards()

        assert crawl.awards == [award2, award1, award3]

    def test_get_budgets(self):
        forrest = AwardCrawler().getBudget('http://en.wikipedia.org/wiki/Forrest_Gump')
        assert int(forrest.getAmount('USD').value)  == 55000000

        godfather = AwardCrawler().getBudget('http://en.wikipedia.org/wiki/The_Godfather')
        assert int(godfather.getAmount('USD').value)  == 6000000
        
        king = AwardCrawler().getBudget('http://en.wikipedia.org/wiki/The_King%27s_Speech')
        assert int(king.getAmount('GBP').value)  == 8000000
        assert int(king.getAmount('USD').value)  == 15000000
