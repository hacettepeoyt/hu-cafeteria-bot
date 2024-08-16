import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def parse_messages(chat_history: dict) -> dict:
    """
    Parses a chat history dictionary to extract and format daily menu information.

    This function processes the provided chat history to find messages containing
    the menu details. It extracts the date, cleans up the meal descriptions by
    removing bullet points, and retrieves the calorie information. The result is
    organized in a dictionary where the keys are formatted dates and the values
    contain the cleaned meal names and calorie count.

    Args:
        chat_history (dict): A dictionary representing the chat history.

    Returns:
        dict: A dictionary containing the menu details for the specified date.
                The dictionary is expected to have keys such as 'meals' and 'calorie'.
    """
    messages = chat_history["messages"]
    menu_list = {}

    for message in messages:
        if (not message["text"] or
                isinstance(message["text"][0], str) or
                message["text"][0]["text"] != "Günün Menüsü"):
            continue

        date_obj = datetime.fromisoformat(message["date"])
        formatted_date = date_obj.strftime("%d.%m.%Y")
        temp = message["text"][1].strip().split("\n")
        dirty_meal_list = temp[:-2]

        # Remove bullet points, extract meal names and calorie
        clean_meal_list = list(map(lambda x: x[2:], dirty_meal_list))
        calorie = temp[-1].split()[1]

        menu_list[formatted_date] = {
            "meals": clean_meal_list,
            "calorie": calorie
        }

    return menu_list


def update_database(database_path: str, menu_list: dict) -> None:
    """
    Updates the database with new menu information.

    Args:
        database_path (str): The path to the database file where the menu data
            is stored.
        menu_list (dict): A dictionary containing the new menu data to be
            added or updated in the database. The dictionary keys are dates,
            and the values are dictionaries with menu details for those dates.

    Returns:
        None: This method does not return any value. It modifies the database file
            in place by updating it with the provided menu information.
    """
    with open(database_path, "r+") as file:
        database_dict = json.load(file)
        database_dict.update(menu_list)
        file.seek(0)
        json.dump(database_dict, file, ensure_ascii=False)


def main(database_path: str, file_path: str) -> None:
    # Initialize database file if not exists with an empty dictionary
    if not os.path.exists(database_path):
        with open(database_path, "w") as file:
            json.dump({}, file)

    with open(file_path, 'r') as f:
        chat_history = json.load(f)

    menu_list = parse_messages(chat_history=chat_history)
    update_database(database_path=database_path, menu_list=menu_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populating the database with existing Telegram message history in "
                                                 "JSON format. Chat history is assumed to be taken from the Text "
                                                 "channel on Telegram. https://t.me/hacettepeyemekhaneText")
    parser.add_argument("-d", "--database",
                        type=Path,
                        help="Path to database file, written in json format",
                        required=True)
    parser.add_argument("-f", "--file",
                        type=Path,
                        help="Path to JSON file containing Telegram message history",
                        required=True)

    args = parser.parse_args()
    main(args.database, args.file)
