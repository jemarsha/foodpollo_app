# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re


class AllRecipes(object):

    @staticmethod
    def search(query_dict):
        """
        Search recipes parsing the returned html data.
        """
        base_url = "https://allrecipes.com/search/results/?"
        query_url = urllib.parse.urlencode(query_dict)

        url = base_url + query_url

        req = urllib.request.Request(url)
        req.add_header('Cookie', 'euConsent=true')

        html_content = urllib.request.urlopen(req).read()

        soup = BeautifulSoup(html_content, 'html.parser')

        search_data = []
        articles = soup.findAll("article", {"class": "fixed-recipe-card"})

        iterarticles = iter(articles)
        next(iterarticles)
        for article in iterarticles:
            data = {}
            try:
                data["name"] = article.find("h3", {"class": "fixed-recipe-card__h3"}).get_text().strip(' \t\n\r')
                data["description"] = article.find("div", {"class": "fixed-recipe-card__description"}).get_text().strip(
                    ' \t\n\r')
                data["url"] = article.find("a", href=re.compile('^https://www.allrecipes.com/recipe/'))['href']
                try:
                    data["image"] = \
                        article.find("a", href=re.compile('^https://www.allrecipes.com/recipe/')).find("img")[
                            "data-original-src"]
                except Exception as e1:
                    pass
                try:
                    data["rating"] = float(
                        article.find("div", {"class": "component recipe-ratings"}).find("span")["review-star-text"])
                except ValueError:
                    data["rating"] = None
            except Exception as e2:
                pass
            if data and "image" in data:  # Do not include if no image -> its probably an add or something you do not want in your result
                search_data.append(data)

        return search_data

    @staticmethod
    def get(url):
        """
        'url' from 'search' method.
         ex. "/recipe/106349/beef-and-spinach-curry/"
        """
        # base_url = "https://allrecipes.com/"
        # url = base_url + uri
        str1 = 'prep'

        req = urllib.request.Request(url)
        req.add_header('Cookie', 'euConsent=true')

        html_content = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        try:
            rating = (soup.find("div", {"class": "component recipe-ratings"}))
            rating = rating.find("span", {"class": "review-star-text"}).get_text()
            rating = float(''.join(re.findall(r'\d.', rating)))
        except:

            rating = soup.find(itemprop="ratingValue").get("content")
        # rating= rating.find("meta").get_text()
        # rating= rating.find("")
        # rating = None

        try:
            name = soup.find("h1", {"class": "headline heading-content"}).get_text().replace("®", "")
        except:
            name = soup.find("h1", {"itemprop": "name"}).get_text()
        # name= name.find("itemprop", {"name"}).get_text()

        data = {
            "rating": rating,
            "ingredients": [],
            "steps": [],
            "name": name,
            "prep_time_and_servings": [],
            "nutrients": []
        }
