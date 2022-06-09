from cgi import print_exception
from unicodedata import name


class Product():
    def init(self, name, price, description, opinions):
        self.name=name
        self.price=price
        self.description=description
        self.opinions=opinions
        pass