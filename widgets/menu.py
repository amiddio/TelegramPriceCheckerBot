import tkinter as tk

from lexicon.lexicon import LEXICON_APP_RU
from widgets.link_form import LinkForm
from widgets.links import Links


class Menu(tk.Menu):

    def __init__(self, master: tk.Tk) -> None:
        super().__init__()
        self.master = master

        menu = tk.Menu(self.master)

        new = tk.Menu(menu, tearoff=0)
        new.add_cascade(label=LEXICON_APP_RU["Link"], command=lambda: LinkForm(self.master))
        new.add_separator()
        new.add_command(label=LEXICON_APP_RU["Exit"], command=self.master.destroy)

        view = tk.Menu(menu, tearoff=0)
        view.add_cascade(label=LEXICON_APP_RU["Links"], command=lambda: Links(self.master))

        menu.add_cascade(label=LEXICON_APP_RU["New"], menu=new)
        menu.add_cascade(label=LEXICON_APP_RU["Edit"], menu=view)

        self.master.config(menu=menu)
