#coding: utf-8
from bs4 import BeautifulSoup
import re
import requests
from decimal import *


ALL_HERO_NAMES_URL = "http://www.dota2.com/heroes/"

class HeroAndAdvantage:
    name = ""
    database_name = ""
    advantage = ""

    def __init__(self, name, advantage):
        self.name = name
        self.database_name = name.replace("'", "")
        self.advantage = advantage


class AdvantageDataForAHero:
    #ADVANTAGES_URL_START = "http://dotamax.com/hero/detail/match_up_comb/"
    ADVANTAGES_URL_START = "http://dotamax.com/hero/detail/match_up_anti/"
    ADVANTAGES_URL_END = ""

    name = ""
    database_name = ""
    advantages_data = []

    def __init__(self, name):
        self.name = name
        self.database_name = name.replace("'", "")

        self.load_advantages_data()

    def load_advantages_data(self):
        url = self.ADVANTAGES_URL_START + self.name_to_url_name(self.name)
        web_content = load_url(url)
        self.advantages_data = self.get_advantages_from_string(web_content, self)

    @staticmethod
    def name_to_url_name(name):
        if(name == "Shadow Fiend"):
            return "nevermore"
        if(name == "Vengeful Spirit"):
            return "vengefulspirit"
        if(name == "Windranger"):
            return "windrunner"
        if(name == "Zeus"):
            return "zuus"
        if(name == "Necrophos"):
            return "necrolyte"
        if(name == "Queen of Pain"):
            return "queenofpain"
        if(name == "Wraith King"):
            return "skeleton_king"
        if(name == "Clockwerk"):
            return "rattletrap"
        if(name == "Nature's Prophet"):
            return "furion"
        if(name == "Lifestealer"):
            return "life_stealer"
        if(name == "Doom"):
            return "doom_bringer"
        if(name == "Outworld Devourer"):
            return "obsidian_destroyer"
        if(name == "Treant Protector"):
            return "treant"
        if(name == "Io"):
            return "wisp"
        if(name == "Centaur Warrunner"):
            return "centaur"
        if(name == "Magnus"):
            return "magnataur"
        if(name == "Timbersaw"):
            return "shredder"
        if(name == "Underlord"):
            return "abyssal_underlord"
        name = name.lower()
        name = name.replace(" ", "_")
        name = name.replace("'", "")
        name = name.replace("-", "")

        return name

    @staticmethod
    def url_name_to_name(name):
        if(name == "nevermore"):
            return "Shadow Fiend"
        if(name == "vengefulspirit"):
            return "Vengeful Spirit"
        if(name == "windrunner"):
            return "Windranger"
        if(name == "zuus"):
            return "Zeus"
        if(name == "necrolyte"):
            return "Necrophos"
        if(name == "queenofpain"):
            return "Queen of Pain"
        if(name == "skeleton_king"):
            return "Wraith King"
        if(name == "rattletrap"):
            return "Clockwerk"
        if(name == "furion"):
            return "Nature's Prophet"
        if(name == "life_stealer"):
            return "Lifestealer"
        if(name == "doom_bringer"):
            return "Doom"
        if(name == "obsidian_destroyer"):
            return "Outworld Devourer"
        if(name == "treant"):
            return "Treant Protector"
        if(name == "wisp"):
            return "Io"
        if(name == "centaur"):
            return "Centaur Warrunner"
        if(name == "magnataur"):
            return "Magnus"
        if(name == "shredder"):
            return "Timbersaw"
        if(name == "abyssal_underlord"):
            return "Underlord"

        name = name.replace("_", " ")
        name = name.title()
        name = name.replace("Of", "of")
        name = name.replace("The", "the")

        return name

    @staticmethod
    def get_advantages_from_string(web_content, self):
        soup = BeautifulSoup(web_content, "html.parser")
        #soup = soup.find("table", class_="sortable")
        soup = soup.find_all("tr")

        list = []

        for row in soup:
            name = str(row.find("a"))
            name = name[22:]
            name = name.split("\"")
            name = name[0]
            name = self.url_name_to_name(name)
            presence_cell = str(row.select("div"))
            presence_cell = presence_cell[120:]
            presence_cell = presence_cell.split(">")
            if(len(presence_cell) > 1):
                new_table = presence_cell[1]
                new_table = new_table.split("%")
                if(len(new_table) > 1):
                    winning_table = str(new_table[0])
                    win_percent = AdvantageDataForAHero.get_num_from_percent(winning_table)
                    list.append(HeroAndAdvantage(name, win_percent))

        return list
        #for finding advantage/synergy percentages
        # for row in soup:
        #     name = str(row.find("a"))
        #     name = name[22:]
        #     name = name.split("\"")
        #     name = name[0]
        #     name = self.url_name_to_name(name)
        #     advantage_cell = str(row.find("div"))
        #     advantage_cell = advantage_cell[26:]
        #     advantage_cell = advantage_cell.split("%")
        #     advantage_cell = advantage_cell[0]
        #     synergy = AdvantageDataForAHero.get_num_from_percent(advantage_cell)
        #     #advantage = AdvantageDataForAHero.get_num_from_percent(advantage_cell)
        #     list.append(HeroAndAdvantage(name, synergy))



    @staticmethod
    def has_data_link_to_attr(tag):
        return tag.has_attr("data-link-to")

    @staticmethod
    def has_data_value_attr(tag):
        return tag.has_attr("data-value")

    @staticmethod
    def get_num_from_percent(string):
        string = string.replace("%", "")
        if(len(string) == 0):
            return 0
        return float(string)


def load_file(filename):
    with open(filename, "r") as content_file:
        return content_file.read()

def load_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    r = requests.get(url, headers=headers)
    return r.text

def get_hero_names_from_string(content):
    soup = BeautifulSoup(content, "html.parser")
    soup = soup.find(id="filterName")

    list = []

    for row in soup.find_all("option"):
        text = row.get_text()
        if(text != "HERO NAME" and text != "All"):
            list.append(text)

    return list

def load_all_hero_data():
    web_content = load_url(ALL_HERO_NAMES_URL)
    hero_list = get_hero_names_from_string(web_content)
    results = []
    total_loaded = 0
    for hero in hero_list:
        print("{}. Loading {}".format(total_loaded, hero))
        total_loaded += 1
        results.append(AdvantageDataForAHero(hero))

    return results
