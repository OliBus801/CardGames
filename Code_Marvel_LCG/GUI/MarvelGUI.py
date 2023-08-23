from tkinter import *
from tkinter import ttk, filedialog
import Sniffer_Writer

MODULARS = [
    "Standard",
    "Expert",
    "Bomb_Scare",
    "Legions_Of_Hydra",
    "The_Doomsday_Chair",
    "The_Masters_Of_Evil",
    "Under_Attack",
    "Goblin_Gimmicks",
    "A_Mess_Of_Things",
    "Power_Drain",
    "Running_Interference",
    "Agent_of_Hydra",
    "Criminal_Meetup",
    "Hulk_Rampage",
    "Red_Hood",
    "Experimental_Weapons",
    "Hydra_Assault",
    "Hydra_Patrol",
    "Weapon_Master",
    "Temporal",
    "Anachronauts",
    "Master_of_Time" 
]


class MarvelGUI(Tk):
    def __init__(self):
        super().__init__()

        self.title("Marvel Champions - GUI")
        self.geometry("600x400")

        csv_path = filedialog.askdirectory(title="Select a folder to save .csv files")
        self.writer = Sniffer_Writer.Writer(csv_path)

        self.deck_path = filedialog.askdirectory(title="Select the folder with your MarvelCDB decks")

        # Label Acceuil
        acceuil = Frame(self, width=600, height=50)
        acceuil.grid(row=0, column=0)
        label_acceuil = Label(acceuil, text="Quickly Create Your Deck With Marvel GUI")
        label_acceuil.place(x=300, y=25, anchor="center")

        # Frame pour les différentes sélections
        self.panneau_selection = Frame(self)
        self.panneau_selection.grid(row=1, column=0)

        # Villain Scenario Selection
        label_villain = Label(self.panneau_selection, text="Choose a scenario: ")
        label_villain.grid(row=0, column=0)
        self.selection_villain = ttk.Combobox(self.panneau_selection, values=[
            "Rhino",
            "Klaw",
            "Ultron",
            "Risky_Business",
            "Mutagen_Formula",
            "Wrecking_Crew",
            "Mole_Man",
            "Absorbing_Man",
            "Crossbones",
            "Taskmaster",
            "Zola",
            "Red_Skull",
            "Kang"
        ])
        self.selection_villain.grid(row=0, column=1)

        # 2-Player Selection
        self.nb_players = IntVar()
        players = Checkbutton(self.panneau_selection, text="2-Player", variable=self.nb_players, command=self.second_hero_toggle)
        players.grid(row=0, column=2)

        # Modular Sets Selection
        label_modular = Label(self.panneau_selection, text="Choose a modular set: ", pady=25)
        label_modular.grid(row=1, column=0)
        self.selection_modular = Listbox(self.panneau_selection, selectmode="multiple")
        self.selection_modular.grid(row=1, column=1)

        for mod in range(len(MODULARS)):
            self.selection_modular.insert(END, MODULARS[mod])

        # Deck Import
        label_hero = Label(self.panneau_selection, text="Import a deck:", pady=25)
        label_hero.grid(row=2, column=0)

        button_hero = Button(self.panneau_selection, text="Select a file", command=self.browse_files)
        button_hero.grid(row=2, column=1)

        self.label_file = Label(self.panneau_selection, text="")
        self.label_file.grid(row=2, column=2)

        # Optional Second Hero
        self.label_second_hero = Label(self.panneau_selection, text="Player 2 - Import a deck:", pady=25)

        self.button_second_hero = Button(self.panneau_selection, text="Select a file", command=self.second_browse_files)

        self.second_label_success = Label(self.panneau_selection, text="")

        # Confirm Button
        confirm_button = Button(self.panneau_selection, text="Confirm / Create .csv files", pady=25, command=self.process)
        confirm_button.grid(row=4, column=1)

        # Success Label
        self.label_success = Label(self.panneau_selection, text="")
        self.label_success.grid(row=5, column=1)

    def browse_files(self):
            file_browser = filedialog.askopenfilename(initialdir=self.deck_path,
                                                       title="Select a txt deck file from MarvelCDB",
                                                       filetypes=[('Text files', '*.txt')])
            if file_browser != "":
                self.hero1_filepath = file_browser

            self.label_file.configure(text=f"SUCCESS")

    def second_browse_files(self):
            file_browser = filedialog.askopenfilename(initialdir=self.deck_path,
                                                       title="Select a txt deck file from MarvelCDB",
                                                       filetypes=[('Text files', '*.txt')])
            if file_browser != "":
                self.hero2_filepath = file_browser

            self.second_label_success.configure(text=f"SUCCESS")

    def second_hero_toggle(self):
        if self.nb_players.get() == 1:
            self.label_second_hero.grid(row=3, column=0)
            self.button_second_hero.grid(row=3, column=1)
            self.second_label_success.grid(row=3, column=2)
        else:
            self.label_second_hero.grid_forget()
            self.button_second_hero.grid_forget()

    def process(self):
        self.label_success.configure(text="Loading...")
        self.update_idletasks()

        villain = self.selection_villain.get()
        modular = self.selection_modular.curselection()
        modulars = []

        for mod in modular:
            modulars.append(MODULARS[mod])

        if self.nb_players.get() == 1:
            self.writer.main(villain, modulars, self.hero1_filepath, self.hero2_filepath)
        else:
            self.writer.main(villain, modulars, self.hero1_filepath)

        # Create label with "Success!"
        self.label_success.configure(text="Success!")


if __name__ == "__main__":
    main_app = MarvelGUI()
    main_app.mainloop()