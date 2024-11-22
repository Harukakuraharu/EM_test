import json
import os
from dataclasses import dataclass, field

from book import Book


@dataclass
class Library:
    """
    Class for creating a library object and interacting with it

    :param filename: name of the file containing the books
    :param books: all books that were created by the user
    """

    filename: str
    books: list = field(default_factory=list)

    def __post_init__(self) -> None:
        self.load_books()

    def load_books(self) -> None:
        """
        Function to load previously created books if filename exists

        :param filename: name of the file containing the books

        :raises: if it was not possible to load data from the file
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    books_data = json.load(f)
                    for book in books_data:
                        self.books.append(book)
            except json.JSONDecodeError as exc:
                raise f"Ошибка при загрузке данных из файла {self.filename}" from exc

    def save_books(self) -> None:
        """
        Uploading books to a file for data storage

        :raises: if it was not possible to load the data into the file
        """
        with open(self.filename, "w", encoding="utf-8") as f:
            try:
                json.dump(
                    self.books,
                    f,
                    ensure_ascii=False,
                    indent=4,
                )
            except Exception:
                print(f"\nОшибка записи книги в файл {self.filename}")

    def add_book(self, title: str, author: str, year: str) -> str:
        """
        Adding a book to the library - in filename.
        id is generated depending on the number of books

        :param title: book title
        :param author: author of the book
        :param year: year of publication of the book

        :raises: If it was not possible to add data to the work

        """
        if not year.isdigit():
            print(
                "\nВнимание! Год содержит недопустимые символы. Попробуйте еще раз."
            )
        else:
            try:
                book_id = (
                    max((book.get("id") for book in self.books), default=0) + 1
                )
                new_book = Book(book_id, title, author, int(year))
                new_book_dict = new_book.get_dict_format()
                self.books.append(new_book_dict)
                self.save_books()
                print(f"\nКнига {new_book_dict} добавлена в каталог")

            except AttributeError:
                print("\nОшибка чтения файла")

    def get_all_books(self):
        """
        List of all books from the catalog

        """
        if len(self.books) < 1:
            print("\nВ каталоге нет книг")
        else:
            print("Список всех книг из каталога:")
            for book in self.books:
                print(book)

    def search_books(self, item: str):
        """
        Search books by title, author or year of publication

        :params item: title, author or year of publication
        """
        books_list = [
            book
            for book in self.books
            if book["title"] == item
            or book["author"] == item
            or str(book["year"]) == item
        ]

        if not books_list:
            print(
                "\nК сожалению, книги по вашему запросу не найдены. Попробуйте изменить параметры поиска"
            )
        else:
            print("Результат найденных книг:")
            for book in books_list:
                print(book)

    def remove_book(self, book_id: int) -> str:
        """
        Remove a book by id

        :params book_id: unique identifier of the book
        """
        remove_book = [
            ind for ind, book in enumerate(self.books) if book["id"] == book_id
        ]
        if remove_book:
            self.books.pop(remove_book[0])
            self.save_books()
            print(f"Книга с ID {remove_book[0]} удалена.")
        else:
            print("\nКнига не найдена")

    def change_status(self, book_id: int, new_status: str):
        """
        Changing the status of a book

        :params book_id: unique identifier of the book
        """

        for book in self.books:
            if book["id"] == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book["status"] = new_status
                    self.save_books()
                    print(f"\nСтатус книги {book} изменён")
                else:
                    print(
                        "\nВнимание! Неккоректный ввод статуса, выберите 'в наличии' или 'выдана'"
                    )
                return
        print("\nКнига не найдена")
