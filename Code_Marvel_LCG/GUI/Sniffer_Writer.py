from bs4 import BeautifulSoup
import requests
import csv
import os

repo_owner = "OliBus801"
repo_name = "CardGames"
token = "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"
MAIN_URL = f"https://api.github.com/repos/OliBus801/CardGames/contents"
headers = {"Authorization": f"Bearer {token}"}


class Sniffer:
    def __init__(self, codename):

        self.codename = codename
        self.dir_of_interest = None
        self.titles_of_interest = {}

    def sniff(self):
        for d in self.dir_of_interest:
            response = requests.get(f"{MAIN_URL}/Marvel_LCG/{d}", headers=headers)
            if response.status_code == 200:
                file_titles = [item["name"] for item in response.json() if item["type"] == "file"]
                for title in file_titles:
                    try:
                        if self.codename in title:
                            self.titles_of_interest[title] = d
                    except KeyError:
                        pass
            else:
                print("Couldn't retrieve content of " + f"{MAIN_URL}/Marvel_LCG/{d}" + f" response_status_code : {response.status_code}")
        # DEBUG
        for titles in self.titles_of_interest:
            print(titles)


class VillainSniffer(Sniffer):
    def __init__(self, codename):
        super().__init__(codename)
        self.dir_of_interest = ["Main_Scheme", "Villain"]
        self.sniff()


class ModularSniffer(Sniffer):
    def __init__(self, codename):
        super().__init__(codename)
        self.dir_of_interest = ["Modular_Sets"]
        self.sniff()


class HeroSniffer(Sniffer):
    def __init__(self, codename):
        super().__init__(codename)
        self.dir_of_interest = ["Hero_Identity", "Nemesis", "Obligation", "Side_Scheme"]
        self.sniff()

    def sniff(self):
        for d in self.dir_of_interest:
            response = requests.get(f"{MAIN_URL}/Marvel_LCG/{d}", headers=headers)
            if response.status_code == 200:
                file_titles = [item["name"] for item in response.json() if item["type"] == "file"]
                for title in file_titles:
                    try:
                        # Hulk / She-Hulk Fix
                        if self.codename == "Hulk":
                            if self.codename in title and "She-Hulk" not in title:
                                self.titles_of_interest[title] = d
                        else:
                            if self.codename in title:
                                self.titles_of_interest[title] = d
                    except KeyError:
                        pass


class Writer:
    def __init__(self, write_path):
        self.write_path = write_path
        self.Hero_deck = os.path.join(write_path, "HERO.csv")
        self.Scheme_deck = os.path.join(write_path, "SCHEME.csv")
        self.Villain_deck = os.path.join(write_path, "VILLAIN.csv")
        self.Player2_Hero_deck = os.path.join(write_path, "PLAYER2_HERO.csv")

    def write(self, titles_of_interest):

        skip_titles = []

        with open(self.Hero_deck, 'w', newline='') as hero, open(self.Scheme_deck, 'w', newline='') as scheme, open(self.Villain_deck, 'w', newline='') as villain:
            hero_writer = csv.writer(hero)
            scheme_writer = csv.writer(scheme)
            villain_writer = csv.writer(villain)

            hero_writer.writerow(['label', 'front', 'back'])
            scheme_writer.writerow(['label', 'front', 'back'])
            villain_writer.writerow(['label', 'front', 'back'])

            for title, directory in titles_of_interest.items():
                if title not in skip_titles:
                    if directory in ["Villain"]:
                        if title.strip(".png")[-1] == "A":
                            card_back = title.strip(".png")[:-1] + "B.png"
                            content = [title,
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{card_back}"]

                            skip_titles.append(card_back)
                        else:
                            content = [title,
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                       "https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/marvel-encounter-back.png"]

                        villain_writer.writerow(content)

                    elif directory in ["Obligation", "Nemesis", "Modular_Sets"]:
                        content = [title,
                                   f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                   "https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/marvel-encounter-back.png"]

                        villain_writer.writerow(content)

                    elif directory in ["Main_Scheme"]:
                        card_back = title.strip(".png")
                        card_back = card_back[:-1] + "B.png"
                        content = [title,
                                   f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                   f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{card_back}"]
                        scheme_writer.writerow(content)
                        skip_titles.append(card_back)

                    elif directory in ["Hero_Identity"]:
                        if title.strip(".png")[-1] == "A":
                            card_back = title.strip(".png")
                            card_back = card_back[:-1] + "B.png"
                            content = [title,
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{card_back}"]
                            hero_writer.writerow(content)
                            skip_titles.append(card_back)
                        else:
                            content = [title,
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                       "https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/marvel-player-back.png"]

                            hero_writer.writerow(content)

                    else:
                        title = title.split('|')[0] + ".png"
                        content = [title,
                                   f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                   "https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/marvel-player-back.png"]
                        hero_writer.writerow(content)

    def hero_write(self, titles_of_interest):
        skip_titles = []

        with open(self.Player2_Hero_deck, "w", newline="") as hero, open(self.Villain_deck, "a", newline="") as villain:
            hero_writer = csv.writer(hero)
            villain_writer = csv.writer(villain)

            hero_writer.writerow(['label', 'front', 'back'])

            for title, directory in titles_of_interest.items():
                if title not in skip_titles:
                    if directory in ["Nemesis", "Obligation"]:
                        content = [title,
                                   f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                   "https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/marvel-encounter-back.png"]

                        villain_writer.writerow(content)

                    elif directory in ["Hero_Identity"]:
                        if title.strip(".png")[-1] == "A":
                            card_back = title.strip(".png")
                            card_back = card_back[:-1] + "B.png"
                            content = [title,
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{card_back}"]
                            hero_writer.writerow(content)
                            skip_titles.append(card_back)
                        else:
                            content = [title,
                                       f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                       "https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/marvel-player-back.png"]

                            hero_writer.writerow(content)
                    else:
                        title = title.split('|')[0] + ".png"
                        content = [title,
                                   f"https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/{directory}/{title}",
                                   "https://raw.githubusercontent.com/OliBus801/CardGames/main/Marvel_LCG/marvel-player-back.png"]
                        hero_writer.writerow(content)

    def read_marvelcdb_textfile(self, txt_file):
        cards_dictionary = {}

        with open(txt_file, "r") as f:
            lines = f.readlines()
            num_lines = sum(1 for line in f)

            hero = lines[2].strip().replace(" ", "_")
            rest_of_deck = lines[5:]

            # Adding the hero identity / nemesis + obligation
            hero_dictionary = HeroSniffer(hero).titles_of_interest
            cards_dictionary.update(hero_dictionary)

            # Adding the rest of the deck
            directory = None
            for line in rest_of_deck:
                if line.strip() == "":
                    pass
                elif line.strip() in ["Upgrades", "Events", "Supports", "Resources", "Allies"]:
                    directory = line.strip()
                else:
                    line = line.split()
                    number_of_cards = int(line[0].strip('x'))
                    index_of_set_specifier = -2
                    for i in range(len(line)):
                        if line[i].startswith('('):
                            index_of_set_specifier = i
                            break
                    name_of_card = line[1:index_of_set_specifier]
                    name_of_card = "_".join(name_of_card)

                    # Stupid fix for hawkeye having two cards with the same fucking name
                    if name_of_card == "Hawkeye":
                        if line[index_of_set_specifier:] == "(Core Set)":
                            name_of_card = name_of_card + "_CoreSet"
                        elif line[index_of_set_specifier:] == "(The Rise of Red Skull)":
                            name_of_card = name_of_card + "_TheRiseofRedSkull"


                    for i in range(number_of_cards):
                        cards_dictionary[f"{name_of_card}|{i+1}"] = directory

        return cards_dictionary


    def main(self, villain, modular, path_to_txt_file, second_hero_path_to_txt_file=None):
        villain_dict = VillainSniffer(villain).titles_of_interest
        hero_dict = self.read_marvelcdb_textfile(path_to_txt_file)
        master_dict = {}

        master_dict.update(villain_dict)

        for mod in modular:
            modular_dict = ModularSniffer(mod).titles_of_interest
            master_dict.update(modular_dict)

        master_dict.update(hero_dict)

        self.write(master_dict)

        if second_hero_path_to_txt_file is not None:
            self.hero_only(second_hero_path_to_txt_file)


    def hero_only(self, path_to_txt_file):
        self.hero_write(self.read_marvelcdb_textfile(path_to_txt_file))


if __name__ == "__main__":
    print("main")