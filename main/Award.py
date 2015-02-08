class Award(object):

    def __init__(self, winner, main_year, extra_year = ''):
        self.winner = winner
        self.main_year = main_year
        self.extra_year = extra_year

        self.average_budget = 0

    def __str__(self):
        if self.extra_year:
            return "Year: %s - %s, Movie: [%s]" % (self.main_year, self.extra_year, self.winner)
        else:
            return "Year: %s, Movie: [%s]" % (self.main_year, self.winner)
