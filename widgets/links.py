import tkinter as tk
import tkinter.messagebox as mb

from lexicon.lexicon import LEXICON_APP_RU
from logger.logger import log
from models.link_model import LinkModel
from tkinter import ttk
from widgets._state import State
from widgets.link_form import LinkForm


class Links:

    def __init__(self, master: tk) -> None:
        super().__init__()
        self.master = master

        # Clear window
        self.master.clear_window()

        # Widgets
        self.master.container_head(LEXICON_APP_RU["Links"])

        # Form variables for treeview
        columns = (LEXICON_APP_RU["Link"], LEXICON_APP_RU["Is active"])
        data = []
        for link in LinkModel.get_all():
            _is_active = LEXICON_APP_RU["Yes"] if link.is_active else LEXICON_APP_RU["No"]
            data.append((link.id, link.url, _is_active))
        callbacks = {LEXICON_APP_RU["edit"]: self._treeview_menu_edit,
                     LEXICON_APP_RU["delete"]: self._treeview_menu_delete}
        self.master.treeview_table(columns, data, callbacks)

    # ------------------------------------------------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------------------------------------------------

    def _treeview_menu_edit(self, tv: ttk.Treeview) -> None:
        """
        Меню клика по списку правой кнопкой мыши - редактирование

        :param tv: ttk.Treeview
        :return: None
        """

        for iid in tv.selection():
            LinkForm(self.master, State(iid, State.STATE_LIST))

    def _treeview_menu_delete(self, tv: ttk.Treeview) -> None:
        """
        Меню клика по списку правой кнопкой мыши - удаление

        :param tv: ttk.Treeview
        :return: None
        """

        try:
            if mb.askyesno(message=LEXICON_APP_RU["Are you sure to delete this link"], title=LEXICON_APP_RU["yesno"]):
                for iid in tv.selection():
                    link = LinkModel.get_one(int(iid))
                    if link:
                        tv.delete(iid)
                        LinkModel(link).delete()
                        msg = LEXICON_APP_RU["Link deleted successfully"].format(link.url)
                        mb.showinfo(LEXICON_APP_RU["Info"], msg)
                        log().info(msg)
        except Exception as e:
            mb.showerror(LEXICON_APP_RU["Internal error"], str(e))
            log().error(str(e))
