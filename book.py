from dataclasses import dataclass


@dataclass
class Book:
    """
    Class for create book object

    :param id: unique identifier, generated automatically
    :param title: book title
    :param author: author of the book
    :param year: year of publication of the book
    :param status: book status - default value in "в наличии"

    """

    id: int
    title: str
    author: str
    year: str
    status: str = "в наличии"

    def get_dict_format(self) -> dict:
        """
        Displaying a book as a dictionary, for writing to a file and displaying for the user

        return: A dictionary containing all the attributes of a book
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }
