from classes.book import Book


class Menu:
    @staticmethod
    def start_controller(library):
        """
        Метод запускает контроллер меню,
        который обрабатывает пользовательские запросы.

        Args:
            library (Library): Экземпляр класса Library
            для работы с базой данных книг.
        """

        while True:
            print("\nМеню:")
            print("1. Добавить новую книгу")
            print("2. Просмотреть список книг")
            print("3. Найти книгу")
            print("4. Удалить книгу")
            print("5. Выйти")
            choice = input("\nВыберите действие: ")

            # Обработка пользовательского ввода
            match choice:
                case "1":
                    # Добавление новой книги
                    title = str(input("Введите название книги: "))
                    author = str(input("Введите автора книги: "))
                    description = input("Введите описание книги: ")
                    genre = library.prompt_genre()
                    if genre:
                        new_book = Book(title, author, description, genre)
                        library.add_book(new_book)
                        print("Книга добавлена в библиотеку.")

                case "2":
                    # Просмотр списка книг
                    library.display_books()

                case "3":
                    # Поиск книги
                    keyword = input("Введите ключевое слово для поиска: ")
                    found_books = library.search_books(keyword)
                    if found_books:
                        print("\nНайденные книги:")
                        for book in found_books:
                            print(f'Название книги: "{book[0]}"; '
                                  f'Автор: {book[1]}')
                    else:
                        print("\nКниги с данным ключевым словом не найдены.")

                case "4":
                    # Удаление книги
                    library.remove_book()

                case "5":
                    # Выход из программы
                    print("До свидания!")
                    break

                case _:
                    # Вывод сообщения об ошибке при некорректном вводе
                    print("Некорректный ввод. Попробуйте снова...")
