from copy import deepcopy


def get_pretty_caption(data: dict[str, str | list[str]]) -> str:
    """
    Method for formatting wb card data to pretty caption.
    Do not use for another data.
    :param data: dict with data
    :return: formatted string
    """
    exclude_keys = (
        "pictures",
        "specs",
        "description",
    )

    data_copy = deepcopy(data)
    for item in exclude_keys:
        del data_copy[item]

    data_copy["price"] = (
        f"{data_copy["price"]}"[:-2] + "." + f"{data_copy["price"]}"[-2:]
    )

    return (
        f"🔑 Артикул: {data['article']}\n"
        f"✏️ Название: {data['title']}\n"
        f"🏷 Категория: {data['category']}\n"
        f"💵 Цена: {data_copy['price']} руб.\n"
        f"⭐️ Рейтинг: {data['rating']}\n"
        f"📣 Количество отзывов: {data['feedbacks']}\n"
    )
