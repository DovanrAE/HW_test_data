import json
import csv

USERS_PATH = "users.json"
BOOKS_PATH = "books.csv"
RESULT_PATH = "result.json"


def load_users(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        raw_users = json.load(f)

    users = []
    for u in raw_users:
        users.append({
            "name": u["name"],
            "gender": u["gender"],
            "address": u["address"],
            "age": u["age"],
            "books": [],
        })

    return users


def load_books(path: str) -> list[dict]:
    books = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            book = {
                # TODO: подставь правильные имена колонок из CSV
                "title": row["Title"],
                "author": row["Author"],
                "pages": int(row["Pages"]),
                "genre": row["Genre"],
            }
            books.append(book)

    return books


def distribute_books(users: list[dict], books: list[dict]) -> None:
    n = len(users)
    user_index = 0
    for book in books:
        users[user_index]["books"].append(book)
        user_index += 1
        if user_index == n:
            user_index = 0

# Определяем "квоту" книг на пользователя. Чтобы по достижении квоты сразу просиходила запись в json
def quota_for_user(idx: int, books_count: int, users_count: int) -> int:
    base = books_count // users_count
    rem = books_count % users_count
    if idx < rem:
        return base + 1

    return base

def write_users_in_json(users: list[dict], books: list[dict], out_path: str) -> None:
    books_count = len(books)
    users_count = len(users)
    book_pos = 0

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("[\n")

        for idx, user in enumerate(users):
            quota = quota_for_user(idx, books_count, users_count)
            for _ in range(quota):
                user["books"].append(books[book_pos])
                book_pos += 1

            f.write(json.dumps(user, ensure_ascii=False, indent=4))
            if idx != users_count - 1:
                f.write(",\n")

        f.write("\n]\n")

def main():
    users = load_users(USERS_PATH)
    books = load_books(BOOKS_PATH)
    write_users_in_json(users, books, RESULT_PATH)


if __name__ == "__main__":
    main()

#этот коммент тут потому что я накосячил при создании ветки в гите и мне нужны минимальные изменения для создания PR-а

