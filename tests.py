import json
import os
import unittest
from unittest.mock import patch

from library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        """
        Test for create library objects for tests with test_library.json
        """
        self.test_filename = "test_library.json"
        self.test_library = Library(self.test_filename)

    def tearDown(self):
        """
        Remove json file for tests
        """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_book(self):
        """
        Test for added book in json file
        """
        self.test_library.add_book("Евгений Онегин", "А.С.Пушкин", "1833")
        self.assertEqual(self.test_library.books[0]["id"], 1)
        self.assertEqual(self.test_library.books[0]["title"], "Евгений Онегин")
        self.assertEqual(self.test_library.books[0]["author"], "А.С.Пушкин")
        self.assertEqual(self.test_library.books[0]["year"], 1833)
        self.assertEqual(self.test_library.books[0]["status"], "в наличии")

    def test_check_id(self):
        """
        Test add more books and check unique id
        """
        self.test_library.add_book("Русалка", "А.С.Пушкин", "1837")
        self.test_library.add_book("Мцыри", "М.Ю.Лермонтов", "1840")
        self.test_library.add_book("Темная башня", "Стивен Кинг", "1982")
        self.assertEqual(len(self.test_library.books), 3)
        for ind in range(len((self.test_library.books))):
            self.assertEqual(self.test_library.books[ind]["id"], ind + 1)

    def test_add_book_invalid_year(self):
        """
        Test for add book with invalid year
        """
        invalid_years = [
            "тысяча девятьсот второй",
            "12/25/1982",
            "сентябрь 1982",
        ]
        for year in invalid_years:
            with self.subTest():
                self.test_library.add_book("Темная башня", "Стивен Кинг", year)
                self.assertNotIn(
                    {"title": "Темная башня"}, self.test_library.books
                )

    def test_read_file(self):
        """
        Test for check read json file
        """
        self.test_library.add_book("Русалка", "А.С.Пушкин", "1837")
        expected_output = [
            {
                "id": 1,
                "title": "Русалка",
                "author": "А.С.Пушкин",
                "year": 1837,
                "status": "в наличии",
            }
        ]
        with open(self.test_filename, encoding="utf-8") as f:
            saved_books = json.load(f)
        self.assertListEqual(saved_books, expected_output)

    def test_get_all_books(self):
        """
        Test get all books
        """
        self.test_library.add_book("Русалка", "А.С.Пушкин", "1837")
        self.test_library.add_book("Мцыри", "М.Ю.Лермонтов", "1840")
        with patch("builtins.print") as mock_print:
            self.test_library.get_all_books()
            self.assertEqual(len(mock_print.call_args), 2)

    def test_get_all_books_empty(self):
        """
        Test get empty library
        """
        with patch("builtins.print") as mock_print:
            self.test_library.get_all_books()
            mock_print.assert_called_once_with("\nВ каталоге нет книг")

    def test_search_book(self):
        """
        Test for search book in catalog
        """
        self.test_library.add_book("Русалка", "А.С.Пушкин", "1837")
        self.test_library.add_book("Темная башня", "Стивен Кинг", "1982")
        self.test_library.add_book("Мцыри", "М.Ю.Лермонтов", "1840")
        expected_output = {
            "id": 1,
            "title": "Русалка",
            "author": "А.С.Пушкин",
            "year": 1837,
            "status": "в наличии",
        }
        with patch("builtins.print") as mock_print:
            self.test_library.search_books("Русалка")
            result = mock_print.call_args[0]
            self.assertEqual(result[0], expected_output)

    def test_search_books_not_exists(self):
        """
        Test for search book in catalog when book is nit exists
        """
        self.test_library.add_book("Мцыри", "М.Ю.Лермонтов", "1840")
        self.test_library.add_book("Темная башня", "Стивен Кинг", "1982")
        with patch("builtins.print") as mock_print:
            self.test_library.search_books("Русалка")
            mock_print.assert_called_once_with(
                "\nК сожалению, книги по вашему запросу не найдены. Попробуйте изменить параметры поиска"
            )

    def test_remove_book(self):
        """
        Test for remove bok in library
        """
        self.test_library.add_book("Русалка", "А.С.Пушкин", "1837")
        self.test_library.add_book("Мцыри", "М.Ю.Лермонтов", "1840")
        self.assertEqual(len(self.test_library.books), 2)

        self.test_library.remove_book(self.test_library.books[0]["id"])
        self.assertEqual(len(self.test_library.books), 1)

    def test_change_status(self):
        """
        Test for update book status
        """
        self.test_library.add_book("Евгений Онегин", "А.С.Пушкин", "1833")
        self.test_library.change_status(
            self.test_library.books[0]["id"], "выдана"
        )
        self.assertEqual(self.test_library.books[0]["status"], "выдана")

    def test_change_invalid_status(self):
        """
        Test for update book invalid status
        """
        self.test_library.add_book("Евгений Онегин", "А.С.Пушкин", "1833")
        with patch("builtins.print") as mock_print:
            self.test_library.change_status(
                self.test_library.books[0]["id"], "неизвестно"
            )
            mock_print.assert_called_once_with(
                "\nВнимание! Неккоректный ввод статуса, выберите 'в наличии' или 'выдана'"
            )

    def test_load_books(self):
        """
        Test for load from another json file
        """
        with open(self.test_filename, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {
                        "id": 1,
                        "title": "Тестовая книга",
                        "author": "Автор",
                        "year": 2023,
                        "status": "в наличии",
                    }
                ],
                f,
            )

        self.test_library.load_books()
        self.assertEqual(len(self.test_library.books), 1)
        self.assertDictEqual(
            self.test_library.books[0],
            {
                "id": 1,
                "title": "Тестовая книга",
                "author": "Автор",
                "year": 2023,
                "status": "в наличии",
            },
        )

    def test_save_books(self):
        """
        Test for check save books from json file
        """
        self.test_library.add_book("Русалка", "А.С.Пушкин", "1837")
        with open(self.test_filename, encoding="utf-8") as f:
            saved_books = json.load(f)
        self.assertListEqual(
            saved_books,
            [
                {
                    "id": 1,
                    "title": "Русалка",
                    "author": "А.С.Пушкин",
                    "year": 1837,
                    "status": "в наличии",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
