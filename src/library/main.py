import libtools as lt
import context as ct
from context import InputState



def execute_main():
    # инициализация
    # библиотеки
    lib = lt.Library()

    # смотрим был ли предыдущий сеанс
    try:
        lib.read_from_file("data.txt")
    except FileNotFoundError:
        pass

    context = ct.Context(InputState(), lib)
    while context:
        context.polling()

    # сохранение библиотеки
    context.lib.write_to_file("data.txt")


if __name__ == "__main__":
    execute_main()
