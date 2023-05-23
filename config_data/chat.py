import os.path

_FILE_NAME = './chat_id'


def save_chat_id(chat_id: str) -> None:
    """
    Сохраняем чат айди в файл.
    Используя этот айди планировщик будет отсылать в этот чат сообщения

    :param chat_id: str
    :return: None
    """

    with open(_FILE_NAME, 'w') as file:
        file.write(chat_id)


def get_chat_id() -> int | None:
    """
    Возвращает чат айди из файла

    :return: int | None
    """

    if not os.path.isfile(_FILE_NAME):
        return
    with open(_FILE_NAME, 'r') as file:
        chat_id = file.read()
        return int(chat_id)
