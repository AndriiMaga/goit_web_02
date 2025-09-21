from views import ConsoleView
from handlers import add_contact, change_contact, show_phone, delete_contact, add_birthday, show_birthday, birthdays, load_data, parse_input, save_data


def main():  # main loop for command input
    help_commands = ['hello', 'add', 'change', 'phone', 'delete', 'all', 'add-birthday', 'show-birthday', 'birthdays',
                     'help', 'exit', 'close']
    view = ConsoleView()
    view.show_message("Welcome to the assistant bot!")
    book = load_data()
    while True:
        user_input = view.prompt("Enter a command: ")
        command, *args = parse_input(user_input)
        if not command:
            continue

        if command in ["close", "exit"]:
            view.show_message("Good bye!")  # exit program
            save_data(book)
            break

        elif command == "help":
            help_text = "\n".join(f"- {cmd}" for cmd in help_commands)
            view.show_commands(help_text)
            continue

        elif command == "hello":
            view.show_message("How can I help you?")  # greeting
        elif command == "add":
            result = add_contact(args, book)
            if result:
                view.show_message(result)  # add contact
        elif command == "change":
            result = change_contact(args, book)
            if result:
                view.show_message(result)  # change phone
        elif command == "phone":
            result = show_phone(args, book)
            if result:
                view.show_message(result)  # find phone
        elif command == "delete":
            result = delete_contact(args, book)
            if result:
                view.show_message(result) # delete contact
        elif command == "all":
            records = book.data if isinstance(book.data, list) else list(book.data.values())
            view.show_contacts(records) # show all contacts
        elif command == "add-birthday":
            result = add_birthday(args, book)
            if result:
                view.show_message(result)  # add birthday
        elif command == "show-birthday":
            result = show_birthday(args, book)
            if result:
                view.show_message(result)  # show birthday
        elif command == "birthdays":
            result = birthdays(args, book)
            if result:
                view.show_message(result)
            # show upcoming birthdays
        else:
            view.show_error("Invalid command.")

if __name__ == "__main__":  # program entry point
    main()