import tkinter as tk

from functools import partial
from tkinter import ttk
from typing import Callable
from config_data.config import load_config, Config
from widgets.links import Links
from widgets.menu import Menu


class App(tk.Tk):

    # ------------------------------------------------------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        config: Config = load_config()

        # set window width/heignt
        window_width = int(config.window_width)
        window_height = int(config.window_height)

        # get the screen size computer
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # gets both half the screen width/height and window width/height
        position_right = int(screen_width / 2 - window_width / 2)
        position_top = int(screen_height / 2 - window_height / 2)

        # window configure
        self.geometry('{}x{}+{}+{}'.format(window_width, window_height, position_right, position_top))
        self.title(config.window_app_title)
        self.minsize(config.window_width_min, config.window_height_min)

        # set resizable window
        self.resizable(config.window_resizable, config.window_resizable)

        # set ico
        self.iconbitmap(r'./app.ico')

        # styling widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=('Calibri', 12, 'bold'))
        style.configure("Treeview", font=('Calibri', 12), rowheight=40)
        style.configure("dropdown-label.TLabel", font=('Calibri', 12), background='#f0f0f0')

        # Set widgets
        Menu(self)
        Links(self)

    # ------------------------------------------------------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------------------------------------------------------

    def clear_window(self) -> None:
        """
        Чистим весь экран приложения кроме главного меню
        """

        for widget in self.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()

    def container_head(self, title: str) -> None:
        """
        Контейнер дла головы приложения. С выводом в него заглавия и разделителя.

        :param title: str
        """

        container = tk.Frame(self.master)
        container.pack(side="top", fill="both")
        container.grid_columnconfigure(0, weight=1)
        tk.Label(container, text=title, font=("Calibri", 16, 'bold')) \
            .grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ttk.Separator(self.master, orient='horizontal').pack(fill='x', padx=10, pady=(10, 30))

    def container_body_form(self) -> tk.Frame:
        """
        Контейнер для тело формы

        :return: tk.Frame
        """

        container = tk.Frame(self.master)
        container.pack(side="top", fill="both")
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=5)
        return container

    def treeview_table(self, columns: tuple, data: list, callbacks: dict = None) -> None:
        """
        Виджет для вывода табличных результатов

        :param columns: tuple
        :param data: list
        :param callbacks: dict
        """

        def display_menu(event):
            iid = treeview.identify_row(event.y)
            if iid:
                treeview.selection_set(iid)
                treeview.menu.post(event.x_root, event.y_root)

        # Create widgets
        scrollbar = tk.Scrollbar(self.master)
        treeview = ttk.Treeview(self.master)

        # Configure widgets
        treeview.config(columns=columns, show='headings')
        treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=treeview.yview)

        # Create menu if needed
        if callbacks is not None:
            treeview.bind("<Button-3>", display_menu)  # Bind
            treeview.menu = tk.Menu(self.master, tearoff=0)
            for k, v in callbacks.items():
                treeview.menu.add_command(label=k.capitalize(), command=partial(v, treeview))

        # Define headings and columns
        for i, item in enumerate(columns, 1):
            treeview.column(f"# {i}", width=30 if i > 1 else 150)
            treeview.heading(item, text=item.capitalize(), anchor='w')

        # Display widget
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(10, 0))
        treeview.pack(expand=True, fill='both', side='top', pady=(10, 0))

        # Filling treeview widget
        for item in data:
            item_id, *d = item
            treeview.insert(parent='', index='end', iid=item_id, values=d)

    @staticmethod
    def text_field(container: tk.Frame, row_num: int, label: str, filled: str = None, is_focus: bool = False) -> tk.Entry:
        """
        Виджет для вывода формы ввода

        :param container: tk.Frame
        :param row_num: int
        :param label: str
        :param filled: str
        :param is_focus: bool
        :return: tk.Entry
        """

        text = '' if filled is None else tk.StringVar(value=filled)
        tk.Label(container, text=label).grid(row=row_num, column=0, sticky="w", padx=10, pady=10)
        row = tk.Entry(container, textvariable=text)
        row.grid(row=row_num, column=1, sticky="we", padx=10, pady=10)
        if is_focus:
            row.focus_set()
        return row

    @staticmethod
    def button_save(container: tk.Frame, row_num: int, text: str, command: Callable) -> None:
        """
        Виджет кнопки Сабмит

        :param container: tk.Frame
        :param row_num: int
        :param text: str
        :param command: Callable
        :return: None
        """

        ttk.Button(container, style='Manage.TButton', text=text, command=command) \
            .grid(row=row_num, column=1, sticky="e", padx=15, pady=10)

    @staticmethod
    def checkbox_field(container: tk.Frame, row_num: int, label: str, checked: bool = False) -> tk.BooleanVar:
        """
        Чекбокс виджет для формы

        :param container: tk.Frame
        :param row_num: int
        :param label: str
        :param checked: bool
        :return: tk.BooleanVar
        """

        tk.Label(container, text=label).grid(row=row_num, column=0, sticky="w", padx=10, pady=10)
        var = tk.BooleanVar(value=checked)
        row = tk.Checkbutton(container, variable=var)
        row.grid(row=1, column=1, sticky='w', padx=5, pady=10)
        return var

