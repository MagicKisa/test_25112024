class FindError(Exception):
    """Базовый класс ошибки при поиске"""


class BookIndexError(FindError):
    """Ошибка возникающая при отсутствии книги с указанным индексом в библиотеке"""


class FindKeyError(FindError):
    """Ошибка возникающая при поиске по несуществующему ключу"""


class NotFoundError(FindError):
    """Ошибка возникающая при отсутствии результатов поиска"""

class Book:
    _BOOK_ID = 0

    @classmethod
    def get_id(cls):
        cls._BOOK_ID += 1
        return cls._BOOK_ID

    def __init__(self, title, author, year):
        self.id = Book.get_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def __str__(self):
        attr_list = [f"{key}: {getattr(self, key)}\n" for key in self.__dict__]
        return "".join(attr_list)


class Library:
    def __init__(self):
        self.book_list = []

    def add_book(self, title, author, year):
        new_book = Book(title, author, year)
        self.book_list.append(new_book)

    def find_book_index_by_id(self, id):
        book_index = None
        for index in range(len(self.book_list)):
            curr_book = self.book_list[index]
            if curr_book.id == id:
                book_index = index

        if book_index is None:
            raise BookIndexError("Книги с таким индексом нет.")

        return book_index

    def remove_book(self, id):
        book_index = None
        for index in range(len(self.book_list)):
            curr_book = self.book_list[index]
            if curr_book.id == id:
                book_index = index

        if book_index is None:
            raise BookIndexError("Книги с таким индексом нет.")

        book_to_remove = self.book_list[book_index]

        self.book_list.remove(book_to_remove)

    def find_book(self, key, value):
        if key not in ("title", "author", "year"):
            raise FindKeyError("Неподходящий ключ")

        find_list = []
        for book in self.book_list:
            if getattr(book, key, False) == value:
                find_list.append(book)

 #       if find_list is None:
 #           raise NotFoundError("Нет результатов")

        return find_list

    def __str__(self):
        books_info = [f"{str(book)}\n" for book in self.book_list]
        return "".join(books_info)

    def change_status(self, id, status):
        if status not in ("в наличии", "выдана"):
            raise ValueError("Неправильное значение статуса")


        book_index = self.find_book_index_by_id(id)
        book = self.book_list[book_index]
        book.status = status


