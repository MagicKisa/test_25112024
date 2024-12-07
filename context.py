from abc import ABC, abstractmethod
import libtools as lt


class State(ABC):
    """
        Базовый класс Состояния объявляет методы, которые должны реализовать все
        Конкретные Состояния, а также предоставляет обратную ссылку на объект
        Контекст, связанный с Состоянием. Эта обратная ссылка может использоваться
        Состояниями для передачи Контекста другому Состоянию.
        """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @property
    def lib(self):
        return

    @abstractmethod
    def proccess(self) -> None:
        pass


class Context:
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов. Он также
    хранит ссылку на экземпляр подкласса Состояния, который отображает текущее
    состояние Контекста.
    """

    _state = None
    """
    Ссылка на текущее состояние Контекста.
    """

    def __init__(self, state: State, lib: lt.Library) -> None:
        self.transition_to(state)
        self.lib = lib

    def transition_to(self, state: State):
        """
        Контекст позволяет изменять объект Состояния во время выполнения.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    Контекст делегирует часть своего поведения текущему объекту Состояния.
    """

    def request1(self):
        self._state.proccess()

    def __bool__(self):
        if self._state == EndState:
            return False
        return True


class InputState(State):
    def proccess(self) -> None:
        try:
            print("Введите следующее действие(1-7): ")
            new_state = int(input())
            if 1 <= new_state <= 7:
                self.context.transition_to(states[new_state - 1])
            else:
                print("Чуточку не то! Введите число от 1 до 7")
        except ValueError:
            print("Вы ввели не целое число, но всё в порядке. Введите целое число от 1 до 7")

class AddBookState(State):
    def proccess(self) -> None:
        print("Введите название книги: ")
        title = input()
        print("Автора книги: ")
        author = input()
        print("Год издания книги: ")
        year = input()

        self.context.lib.add_book(title, author, year)
        print("Книга добавлена! Спасибо \n")
        self.context.transition_to(InputState)

class RemoveBookState(State):
    def proccess(self) -> None:
        print("Введите уникальный id книги для удаления: ")
        try:
            id = int(input())
            try:
                self.context.lib.remove_book(id)
                print("Книга удалена, спасибо!\n")
                self.context.transition_to(InputState)
            except lt.FindError:
                print("Книга с таким id не найдена, попробуйте ещё. ")
        except ValueError:
            print("Индекс это целое число, попробуйте ещё.")

class FindBookState(State):
    def proccess(self) -> None:
        key = input("Введите категорию поиска(author, title, year): ")
        value = input("Введите автора, название или год(в зависимости от категории поиска): ")
        try:
            book_list = self.context.lib.find_book(key, value)

            if book_list is None:
                print("Книги не найдены. ")
            else:
                print("Подходящие книги: ")
                for book in book_list:
                    print(book)

            self.context.transition_to(InputState)
        except lt.FindKeyError:
            print("Вы ввели неправильную категорию поиска, введите одно из значений author, title или year")

class PrintLibState(State):
    def proccess(self) -> None:
        if self.context.lib:
            print(self.context.lib)
        else:
            print("Библиотека пуста.")
        self.context.transition_to(InputState)

class ChangeStatusState(State):
    def proccess(self) -> None:
        try:
            id = int(input("Введите id книги у которой хотите поменять статус: "))
            try:
                print("Введите новый статус (\"в наличии\", \"выдана\"): ")
                status = input()
                self.context.lib.change_status(id, status)
                print("Статус книги изменён. \n")

                self.context.transition_to(InputState)
            except ValueError:
                print("Вы ввели неправильный статус, попробуйте ещё!")
            except lt.BookIndexError:
                print("Вы ввели неправильный индекс, попробуйте ещё!")
        except ValueError:
            print("Индекс это целое число, попробуйте ещё!")

class MenuState(State):
    def proccess(self) -> None:
        print("""
                                            Чтобы добавить книгу напишите 1,
                                            Удаление книги - 2, Поиск книги - 3, 
                                            Отобразить все книги - 4, Изменение статуса - 5,
                                            Показать меню - 6,
                                            Сохранить и завершить работу - 7""")
        self.context.transition_to(InputState)

class EndState(State):
    def proccess(self) -> None:
        pass

states = [AddBookState, RemoveBookState, FindBookState, PrintLibState, ChangeStatusState, MenuState, EndState]