import tkinter as tk
import tkinter.messagebox as mb

from lexicon.lexicon import LEXICON_APP_RU
from logger.logger import log
from models.link_model import LinkModel
from models.link_orm import LinkOrm
from widgets._state import State


class LinkForm:

    def __init__(self, master: tk, state: State = None) -> None:
        super().__init__()
        self.master = master

        # Clear window
        self.master.clear_window()

        if state is not None:
            self._state = state
            self._state.row = LinkModel.get_one(iid=int(self._state.id))

        # Widgets
        title = LEXICON_APP_RU["Add Link"] if self._state is None else LEXICON_APP_RU["Edit Link"]
        self.master.container_head(title)
        self._container = self.master.container_body_form()
        self._link = self.master.text_field(
            container=self._container,
            row_num=0,
            label=LEXICON_APP_RU["Link"],
            filled='' if self._state is None else self._state.row.url,
            is_focus=True
        )
        self._is_active = self.master.checkbox_field(
            container=self._container,
            row_num=1,
            label=LEXICON_APP_RU["Is active"],
            checked=True if self._state is None else self._state.row.is_active,
        )
        self.master.button_save(self._container, 2, LEXICON_APP_RU["Save"], self._save_button_clicked)

    # ------------------------------------------------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------------------------------------------------

    def _save_button_clicked(self) -> None:
        """
        Коллбэк метод для срабатывания клика по кнопке.
        Сохраняем изменения

        :return: None
        """

        url = self._link.get().strip()
        is_active = self._is_active.get()
        try:
            # Validate input data
            if not url:
                raise ValueError(LEXICON_APP_RU["Field Link is required"])

            if self._state is not None and self._state.row:
                self._state.row.url = url
                self._state.row.is_active = is_active
                result = LinkModel(self._state.row).save()
            else:
                result = LinkModel(
                    LinkOrm(url=url, is_active=is_active)
                ).save()
            if result:
                log().info(result)
                mb.showinfo(LEXICON_APP_RU["Info"], LEXICON_APP_RU["Link saved successfully"].format(result.url))
                self._link.delete(0, len(url))
                if self._state is not None and self._state.back == State.STATE_LIST:
                    from widgets.links import Links
                    Links(self.master)

        except ValueError as e:
            mb.showerror(LEXICON_APP_RU["Value Error"], str(e))
        except Exception as e:
            mb.showerror(LEXICON_APP_RU["Internal error"], str(e))
            log().error(str(e))
