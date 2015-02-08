class Movie(object):

    def __init__(self, title, budget, link):
        self.title = title
        self.budget = budget
        self.link = link

    def __str__(self):
        return "Title: %s, Budget: %s" % (self.title, self.budget)
