class Movie:
    title = ''
    budget = ''
    link = ''

    def __init__(self, title, budget, link):
        #TODO: Add class tests.
        self.title = title
        self.budget = budget
        self.link = link

    def __str__(self):
        return "Title: %s, Budget: %s" % (self.title, self.budget)