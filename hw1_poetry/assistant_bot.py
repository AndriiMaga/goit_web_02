from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:  # base class for all fields (name, phone, birthday)
    def __init__(self, value):
        self.value = value

    def __str__(self):  # return field value as string
        return str(self.value)

class Name(Field):  # class for contact name
    def __init__(self, value):
        if not value:
            raise ValueError('Name cannot be empty')
        super().__init__(value)

class Phone(Field):  # class for phone number
    def __init__(self, value):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits")

class Birthday(Field): # class for storing birthday
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    def __str__(self):
        return self.value

class Record:  # class for storing single contact info
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):  # add new phone
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def edit_phone(self, old_phone, new_phone):  # replace old phone with new
        new_phone_digits = Phone(new_phone)
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone_digits.value
                return
        raise ValueError("Old phone number not found")

    def find_phone(self, phone):  # find phone object by number
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def add_birthday(self, str_birthday):  # add birthday to contact
        self.birthday = Birthday(str_birthday)
        return f"Birthday {str_birthday} was added for contact {self.name.value}"

    def __str__(self):  # return contact info
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):  # class for managing multiple records
    def add_record(self, record):  # add contact record
        self.data[record.name.value] = record

    def find(self, name):  # find contact by name
        return self.data.get(name)

    def delete(self, name):  # delete contact by name
        if name in self.data:
            return self.data.pop(name)
        else:
            raise KeyError(name)

    def __str__(self):  # return all contacts as string
        if not self.data:
            return "Address book is empty"
        return "\n".join(map(str, self.data.values()))

    def get_upcoming_birthdays(self, days=7):  # find birthdays within given days
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday:
                birth_day = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birth_day.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if 0 <= (birthday_this_year - today).days <= days:
                    birthday_this_year = adjust_for_weekend(birthday_this_year)
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays

def adjust_for_weekend(birthday):  # move birthday to Monday if on weekend
    if birthday.weekday() == 5:
        birthday += timedelta(days=2)
    elif birthday.weekday() == 6:
        birthday += timedelta(days=1)
    return birthday

def input_error(func): # decorator for handling errors
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            contact_name = e.args[0]
            return f"Contact {contact_name} not found."
        except ValueError as e:
            if "not enough values to unpack" in str(e):
                return "Not enough arguments. Please check the correctness of the entered data."
            return str(e)
        except IndexError:
            return "Not enough arguments."
        except AttributeError:
            return "Contact not found. Please add the contact before setting a birthday"
    return inner

@input_error
def parse_input(user_input):  # split command and arguments
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):  # add new contact with phone
    name, phone = args
    record = book.get(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f"Contact name: {name} added with phone number: {phone}."

@input_error
def change_contact(args, book):  # change contact's phone number
    name, old_phone, new_phone = args
    record = book.get(name)
    if not record:
        raise KeyError(name)
    record.edit_phone(old_phone, new_phone)
    return f"Updated: {old_phone} was changed to {new_phone} for {name}."

@input_error
def delete_contact(args, book): # delete contact with phone
    name, = args
    book.delete(name)
    return f"Contact name: {name} deleted."


@input_error
def show_phone(args, book):  # show phone numbers for contact
    name, = args
    record = book.data[name]
    phones = ", ".join(str(p) for p in record.phones)
    return f"{name}: {phones}"


@input_error
def add_birthday(args, book):  # add birthday to contact
    name, birthday = args
    record = book.data.get(name)
    return record.add_birthday(birthday)

@input_error
def show_birthday(args, book):  # show contact's birthday
    name, = args
    record = book.data[name]
    return f"{name}: {record.birthday}" if record.birthday else f"{name} has no birthday set"

@input_error
def birthdays(args, book): # show upcoming birthdays in book
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days=days)
    if upcoming:
        return "\n".join([f"{item['name']}: {item['birthday']}" for item in upcoming])
    else:
        return "No upcoming birthdays."

def show_all(book):  # show all contacts with phones and birthdays
    if not book.data:
        return "Address book is empty"
    result = []
    for record in book.data.values():
        phones = ", ".join(str(p) for p in record.phones)
        birthday = f", Birthday: {record.birthday}" if record.birthday else ""
        result.append(f"{record.name.value}: {phones}{birthday}")
    return "\n".join(result)

def save_data(book, filename = "addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)

def load_data(filename = "addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()



def main():  # main loop for command input
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")  # exit program
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")  # greeting
        elif command == "add":
            print(add_contact(args, book))  # add contact
        elif command == "change":
            print(change_contact(args, book))  # change phone
        elif command == "phone":
            print(show_phone(args, book))  # find phone
        elif command == "delete":
            print(delete_contact(args, book)) # delete contact
        elif command == "all":
            print(show_all(book))  # show all contacts
        elif command == "add-birthday":
            print(add_birthday(args, book))  # add birthday
        elif command == "show-birthday":
            print(show_birthday(args, book))  # show birthday
        elif command == "birthdays":
            print(birthdays(args, book))  # show upcoming birthdays
        else:
            print("Invalid command.")

if __name__ == "__main__":  # program entry point
    main()