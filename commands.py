from library import Library


def main():
    first_text = """Для удобства, хранилище книг будет находиться в файле library.json.
Если хотите использовать другое хранилище - введите название файла в формате имя.json.
Если этого не требуется, нажмите Enter """
    print("Добро пожаловать в систему управления библиотекой:")
    filename = input(first_text)
    if filename != "":
        library = Library(filename)
    else:
        library = Library("library.json")

    while True:
        print("\nМеню действий:")
        print("1. Добавить книгу")
        print("2. Вывести список всех книг")
        print("3. Поиск книги")
        print("4. Удалить книгу")
        print("5. Изменить статус книги")
        print("0. Выйти")

        choice = input(
            "Введите номер действия, которое необходимо выполнить: "
        )
        print("")
        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)

        elif choice == "2":
            library.get_all_books()

        elif choice == "3":
            query = input("Введите название, автора или год для поиска: ")
            library.search_books(query)

        elif choice == "4":
            idx = int(
                input("Введите идентификатор книги, которую нужно удалить: ")
            )
            library.remove_book(idx)

        elif choice == "5":
            idx = int(input("Введите идентификатор книги: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            library.change_status(idx, new_status)

        elif choice == "0":
            break

        else:
            print("Такой команды не существует. Попробуйте еще раз.")
