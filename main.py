from classes.menu import Menu
from classes.library import Library


def main():
    # Создание экземпляра класса Library для работы с базой данных книг
    library = Library("database/books.db")

    # Запуск контроллера меню для управления приложением
    Menu.start_controller(library)


if __name__ == "__main__":
    main()
