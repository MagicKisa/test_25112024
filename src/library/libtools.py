class FindError(Exception):
    """Базовый класс ошибки при поиске"""


class BookIndexError(FindError):
    """Ошибка возникающая при отсутствии книги с указанным индексом в библиотеке"""


class FindKeyError(FindError):
    """Ошибка возникающая при поиске по несуществующему ключу"""


class NotFoundError(FindError):
    """Ошибка возникающая при отсутствии результатов поиска"""

class Book:
    """Класс для описания книги"""
    _BOOK_ID = 0

    @classmethod
    def get_id(cls) -> int:
        """Получает уникальный идентификатор книги"""
        cls._BOOK_ID += 1
        return cls._BOOK_ID

    def __init__(self, title: str, author: str, year: str) -> None:
        """Инициализация книги"""
        self.id = Book.get_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def __str__(self) -> str:
        """функция для форматирования вывода данных книги"""
        attr_list = [f"{key}: {getattr(self, key)}\n" for key in self.__dict__]
        return "".join(attr_list)


class Library:
    def __init__(self) -> None:
        """Инициализация библиотеки"""
        self.book_list = []

    def add_book(self, title: str, author: str, year: str) -> None:
        """Функция для добавления книги в библиотеку"""
        new_book = Book(title, author, year)
        self.book_list.append(new_book)


    def __find_book_index_by_id(self, id: int) -> int:
        """Функция позволяющая найти index книги с данным id в списке self.book_list"""
        book_index = None
        for index in range(len(self.book_list)):
            curr_book = self.book_list[index]
            if curr_book.id == id:
                book_index = index

        if book_index is None:
            raise BookIndexError("Книги с таким индексом нет.")

        return book_index

    def remove_book(self, id: int) -> None:
        """Функция для удаления книги по id из списка self.book_list"""
        book_index = self.__find_book_index_by_id(id)

        book_to_remove = self.book_list[book_index]
        self.book_list.remove(book_to_remove)

    def find_book(self, key: str, value: str) -> list:
        """Позволяет найти книгу по title, author или year"""
        if key not in ("title", "author", "year"):
            raise FindKeyError("Неподходящий ключ")

        find_list = []
        for book in self.book_list:
            if getattr(book, key, False) == value:
                find_list.append(book)

        return find_list

    def __str__(self) -> str:
        """Функция для упрощения формата вывода библиотеки"""
        books_info = [f"{str(book)}\n" for book in self.book_list]
        return "".join(books_info)

    def __bool__(self) -> bool:
        return bool(self.book_list)

    def change_status(self, id: int, status: str) -> None:
        """Позволяет поменять статус книги по её id"""
        if status not in ("в наличии", "выдана"):
            raise ValueError("Неправильное значение статуса")


        book_index = self.__find_book_index_by_id(id)
        book = self.book_list[book_index]
        book.status = status

    def read_from_file(self, filename: str) -> None:
        """Функция для чтения данных предыдущего сеанса из специального файла"""

        with open(filename, "r") as f:

            # читаем строки из файла
            strs = f.readlines()
            if strs is None:
                return

            # обрезаем \n в конце
            strs = [st.rstrip() for st in strs]
            for i in range(len(strs) // 6):

                # зная формат, извлекаем необходимые данные
                id = int(strs[i * 6].split("id: ")[1])
                title = strs[i * 6 + 1].split("title: ")[1]
                author = strs[i * 6 + 2].split("author: ")[1]
                year = strs[i * 6 + 3].split("year: ")[1]
                status = strs[i * 6 + 4].split("status: ")[1]

                # воссоздаём и добавляем книгу в библиотеку
                book = Book(title, author, year)
                book.id = id
                book.status = status
                self.book_list.append(book)

                # сохраняем уникальность id
                Book._BOOK_ID = id

    def write_to_file(self, filename: str) -> None:
        """Функция для сохранения сеанса библиотеки в файл"""
        with open(filename, "w") as f:
            f.write(str(self))



