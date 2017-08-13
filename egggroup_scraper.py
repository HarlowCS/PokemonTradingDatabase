from __future__ import print_function
import requests
from lxml import html
import re
import sys

url = "https://pokemondb.net/pokedex/game/sun-moon"

if __name__ == "__main__":
    pokemon = []
    group = ['Monster', 'Human-Like', 'Water 1', 'Water 2', 'Water 3', 'Bug', 'Mineral', 'Flying', 'Amorphous', 'Field', 'Fairy', 'Ditto', 'Dragon', 'Undiscovered']
    mainpage = requests.get(url)
    webtree = html.fromstring(mainpage.content)

    pokemonlinks = webtree.xpath('//a/@href')
   
    pattern = re.compile("/pokedex/(.)+")
    index = 1
    for poke in pokemonlinks:
        if pattern.match(poke) and poke not in pokemon:
            pokemon.append(poke)

    pokemon = pokemon[5:-2]

    f = open('insert_eggroup.sql', 'w')
    sys.stdout = f

    dex = 1
    for item in pokemon:
        url = "https://pokemondb.net" + item
        pokepage = requests.get(url)
        poketree = html.fromstring(pokepage.content)
        newlinks = poketree.xpath('//div[@class="colset"]//div[@class="col desk-span-4 lap-span-6"]//table[@class="vitals-table"]//tbody//tr//td//a/text()')
        guy = [0] * 15
        guy[0] = dex
        for index, item in enumerate(group):
            if item == newlinks[-1]:
                guy[index+1] = 1
            if item == newlinks[-2]:
                guy[index+1] = 1

        print("INSERT INTO EGGGROUP (PokedexNumber, Monster, HumanLike, Water1, Water2, Water3, Bug, Mineral, Flying, Amorphous, Field, Fairy, Ditto, Dragon, Undiscovered)\n VALUES (", guy[0], ', ', guy[1], ', ', guy[2], ', ', guy[3], ', ', guy[4], ', ', guy[5], ', ', guy[6], ', ', guy[7], ', ', guy[8], ', ', guy[9], ', ', guy[10], ', ', guy[11], ', ', guy[12], ', ', guy[13], ', ', guy[14], '); ', sep='', end='\n\n')   
        dex += 1
