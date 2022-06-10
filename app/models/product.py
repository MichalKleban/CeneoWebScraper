import json
import imp
import requests
from bs4 import BeautifulSoup
from app.models.opinion import Opinion
from app.routes import product
from app.utils import get_item
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from app.models.product import Product
class Product():
    def __init__(self, product_id, product_name, price, description, opinions=[]):
        self.product_name=product_name
        self.product_id=product_id
        self.price=price
        self.description=description
        self.opinions=opinions
        return self


    def extract_name(self):

        self.product_name=get_item(page, "h1.product-top__product-info__name")
        self.product_name=get_item(page,"product-top__product-info__name")
        return self
    
    def extract_opinions(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        all_opinions = []
        while(url):
            response = requests.get(url)
            page = BeautifulSoup(response.text, "html.parser")
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
                single_opinion = Opinion().extract_opinion(opinion)
                self.opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl"+get_item(page, "a.pagination__next")["href"]
            except TypeError:
                url =None
        return self

    def opinions_to_df(self):
        return pd.read_json(json.dumps([opinion.to_dict() for opinion in self.opinions]))
    def calculate_stats(self):
        opinions = 
        opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))
 
        self.opinions_count = len(opinions),
        self.pros_count = opinions["pros"].map(bool).sum()
        self.cons_count = opinions["cons"].map(bool).sum()
        self.average_score = opinions["stars"].mean().round(2)

        return self
    
    def draw_charts(self):


        if not os.path.exists("app/plots"):
            os.mkdir("app/plots")

        recommendation = opinions["recommendation"].value_counts(dropna=False).sort_index().reindex(["Nie polecam", "Polecam", None], fill_value=0)
        recommendation.plot.pie(
            label="",
            autopct= lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',
            colors = ["crimson","forestgreen","lightgrey"],
            labels=["Nie polecam","Polecam","Nie mam zdania"]

        )
        plt.title("Rekomendacje")
        plt.savefig(f"plots/{product_id}_recommendations.png")
        plt.close()

        stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
        stars.plot.bar(
            color = "#fbec5d"
        )

        plt.title("Oceny produktów")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        plt.grid(True, axis="y")
        plt.xticks(rotation=0)
        plt.savefig(f"plots/{product_id}_stars.png")
        plt.close()

        return self


    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def to_dict(self):
        pass
    def export_opinions(self):
        if not os.path.exists("app/opinions"):
            os.mkdir("app/opinions")
        
        with open(f"app/opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump(opinion.to_dict() for self.opinions, jf, indent=4, ensure_ascii=False)
            
    def export_product(self):
        pass
