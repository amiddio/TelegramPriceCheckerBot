LEXICON_MENU_RU: dict[str, str] = {
    '/start': 'Запустить бот',
    '/help': 'Помощь',
    "/parse": "Запустить парсинг ссылок",
}

LEXICON_GENERAL_RU: dict[str, str] = {
    "/start": "Этот бот парсит различные сайты с продуктами, и сообщает когда цены изменяются.",
    "/help": "Для работы бота необходимо добавить ссылки на продукты, через соответствующее приложение.\n"
             "И настроить частоту проверок (по умолчанию проверки проходят один раз в час).\n\n"
             "На данный момент работает парсинг для сайтов: <b>amazon</b>, <b>iherb</b> и <b>rei</b>",
    "/parse": "/parse command",
    "Bot stopped": "Бот остановлен!",
    "not available": "недоступен",
    "product changed": "{title}Изменения: <s>{prev}</s>, <b>{curr}</b>\n{link}",
    "products not changed": "Цены продуктов не изменились",
    "parser class not found": "Не найден парсер класс для ссылки: '{url}'",
    "echo message": "Мне нечем ответить на этот запрос",
}

LEXICON_APP_RU: dict[str, str] = {
    "Field Link is required": "Поле 'Ссылка' обязательно для заполнения",
    "Link saved successfully": "Ссылка '{}' успешно сохранена",
    "Link deleted successfully": "Ссылка '{}' успешно удалена",
    "Info": "Информация",
    "Value Error": "Ошибка данных",
    "Internal error": "Внутренняя ошибка",
    "Add Link": "Добавить ссылку",
    "Edit Link": "Изменить ссылку",
    "Link": "Ссылка",
    "Links": "Ссылки",
    "Title": "Название",
    "Is active": "Активная?",
    "Save": "Сохранить",
    "Yes": "да",
    "No": "нет",
    "view": "Открыть",
    "edit": "Изменить",
    "delete": "Удалить",
    "Are you sure to delete this link": "Вы действительно хотите удалить эту ссылку?",
    "Edit": "Изменить",
    "New": "Новая",
    "Exit": "Выйти",
    "yesno": "Опрос",
}
