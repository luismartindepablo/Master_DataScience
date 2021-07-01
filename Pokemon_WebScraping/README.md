# Pokémon Web Scraping

This repository has been created under the context of the subject Typology and Data Life Cycle, belonging to the Master in Data Science at the Open University of Catalonia. In it, web scraping techniques are applied using Python programming language to extract data from the web https://pokemondb.net and generate a dataset holding the main information from the National Pokédex.

This project has been done individualy by **Luis Martin de Pablo**

## Performance and requirements

The main program is *PokemonScraper.py*. When executing it will start the web scraping process. It is build on top of *Crawler.py*, which is the program in charge of downloading the web via http requests. 

The requested libraries are:
- os
- csv
- time
- requests 
- BeautifulSoup4

The output files are the CSV dataset, aswell as the images and icons folders where all the .jpg and .png are stored.

## Dataset 

The dataset brings together the main characteristics of the 893 Pokémon present until the 8th generation, as well as all their forms and variations, for a total of 1045 entries. These data include the type and base stats of each Pokémon. It also includes other information such as the height, weight or the species.

**Content**:

- **Number:** Pokédex number. 
- **Name:** Pokémon name.
- **Type1:** Main Pokémon type.
- **Type2:** Secondary Pokémon type.
- **Total:** Sum of all the base stats.
- **HP:** Base HP stat.
- **Atk:** Base attack stat.
- **Def:** Base defense stat.
- **SpAtk:** Base special attack stat.
- **SpDef:** Base special defense stat.
- **Spd:** Base speed stat.
- **Species:** Pokémon species.
- **Height:** Height of the Pokémon in meters.
- **Weight:** Weight of the Pokémon in kilograms. 

This dataset can be also found at Zenodo under the **DOI: 10.5281/zenodo.4665380**

## License

This project can be used under the License CC BY-NC-SA 4.0  
All art and design belongs to ©1995-2021 Nintendo/Game Freak 
