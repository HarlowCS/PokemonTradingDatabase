from __future__ import print_function
import requests
from lxml import html
import re
import sys

url = "https://pokemondb.net/pokedex/game/sun-moon"

if __name__ == "__main__":
    pokemon = []
    mainpage = requests.get(url)
    webtree = html.fromstring(mainpage.content)

    pokemonlinks = webtree.xpath('//a/@href')
   
    pattern = re.compile("/pokedex/(.)+")
    index = 1
    for poke in pokemonlinks:
        if pattern.match(poke) and poke not in pokemon:
            pokemon.append(poke)

    pokemon = pokemon[5:-2]

    f = open('insert_pokedex.sql', 'w')
    sys.stdout = f

    dex = 1
    for item in pokemon:
        url = "https://pokemondb.net" + item
        pokepage = requests.get(url)
        poketree = html.fromstring(pokepage.content)
        newlinks = poketree.xpath('//article[@class="main-content grid-wrapper"]/h1/text()')
        guy = [0] * 4
        guy[0] = dex
        guy[1] = newlinks[0]
        newlinks = poketree.xpath('//a[@class="sprite-share-link "]/@href') #FUCKING TRAILING WHITESPACE, SHITTY WEB DESIGN Ughhh
        #how the fuck do i grab and store images?
        guy[2] = newlinks[0]
        guy[3] = newlinks[1]

        print("INSERT INTO POKEDEX (DexNumber, Species, RegImage, ShinyImage)\n VALUES (", guy[0], ', \"', guy[1], '\", \"', guy[2], '\", \"', guy[3], '\"); ', sep='', end='\n\n')       
        dex += 1
