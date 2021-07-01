# -------------------
# Import packages
# -------------------
import os
import csv
import time
import requests 
from Crawler import download
from bs4 import BeautifulSoup
from urllib import robotparser

# -----------------------
# Create needed folders
# -----------------------
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
create_folder("icons")
create_folder("images")


# -------------------
# Scraping
# -------------------
# Webs
web_url = "https://pokemondb.net"
pokedex_url = "https://pokemondb.net/pokedex/all"

# Robot Parser
rp = robotparser.RobotFileParser()
rp.set_url(web_url + "/robots.txt")
rp.read()

# Crawl Main Web
html = download(pokedex_url)

# Select Inf we want
soup = BeautifulSoup(html.content, 'html.parser')
pokedex = soup.body.main.tbody.find_all("tr")
del soup

# Open CSV
df_pokedex = open('National_Pokedex.csv', mode='w')
pokedex_writer = csv.writer(df_pokedex, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
pokedex_writer.writerow(["ID", "Number", "Name", "Type1", "Type2", "Total", "HP", "Atk", "Def", "SpAtk", "SpDef", "Spd", "Species", "Height", "Weight"])

# Initialize ID
id_num = 0

# Harvest Inf
for pokemon in pokedex:
    # Avoid server saturation
    t0 = time.time()

    # ID
    id_num += 1

    try:
        # ---------------
        # Main Page Inf
        # ---------------
        main_inf = pokemon.find_all("td")
        Number = main_inf[0].find("span", {"class": "infocard-cell-data"}).string
        Name = main_inf[1].a.string
        try:
            Form = main_inf[1].find("small").string
            Form_to_write = "(" + Form + ")"
        except:
            Form = ""
            Form_to_write = ""
        Stats = [x.string for x in main_inf[3:]]
        types_list = main_inf[2].find_all("a")
        Type1 = types_list[0].string
        if len(types_list) == 2:
            Type2 = types_list[1].string
        else:
            Type2 = None

        # ---------------
        # Deeper Inf
        # ---------------
        pokemon_link = web_url + main_inf[1].a["href"]
        pokemon_html = download(pokemon_link)
        soup = BeautifulSoup(pokemon_html.content, 'html.parser')
        
        # Select inf
        tab_id_list = soup.body.main.find("div", {"class": "sv-tabs-tab-list"})
        if Form == "":
            tab_id = tab_id_list.find("a", text = Name).get("href").strip("#")
        if Form != "":
            tab_id = tab_id_list.find("a", text = Form).get("href").strip("#")
        
        
        vitals_table = soup.body.main.find("div", {"id": tab_id}).find("table", {"class": "vitals-table"}).find_all("tr")
        Species = vitals_table[2].td.string
        Height = vitals_table[3].td.text.split()[0] + " m"
        Weight = vitals_table[4].td.text.split()[0] + " kg"
        
        # Write CSV
        pokedex_writer.writerow([id_num, Number, Name + Form_to_write, Type1, Type2, *Stats, Species, Height, Weight])
        
        # ---------------
        # Images
        # ---------------
        try:
            # Get Icon
            icon_link = main_inf[0].find("span", {"class": "img-fixed icon-pkmn"}).get("data-src")
            icon = download(icon_link)
            ruta = os.getcwd() + "/icons/" + str(id_num) + icon_link.split("/")[-1]
            output = open(ruta, "wb")
            output.write(icon.content)
            output.close()

            # Get Image
            try:
                img_link = soup.body.main.find("div", {"id": tab_id}).find("a", {"rel" : "lightbox"}).get("href")
            except AttributeError as e:
                img_link = soup.body.main.find("div", {"id": tab_id}).find("img").get("src")
            img = download(img_link)
            ruta = os.getcwd() + "/images/" + str(id_num) + img_link.split("/")[-1]
            output = open(ruta, "wb")
            output.write(img.content)
            output.close() 
            
        except Exception as e:
            print("Downloading image error:", e)
            
    except Exception as e: 
        print("Download error:", e)
        print("Jump to next Pokemon")

    # Automatic delay
    response_delay = time.time() - t0
    time.sleep(2 * response_delay)

# Close CSV
df_pokedex.close()