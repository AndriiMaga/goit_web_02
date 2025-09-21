from abc import ABC, abstractmethod

class BaseView(ABC):
    @abstractmethod
    def show_message(self, text: str) -> None:
        pass

    @abstractmethod
    def show_error(self, text: str) -> None:
        pass

    @abstractmethod
    def prompt(self, prompt_text: str) -> str:
        pass

    @abstractmethod
    def show_contact(self, record) -> None:
        pass

    @abstractmethod
    def show_contacts(self, records) -> None:
        pass

    @abstractmethod
    def show_commands(self, help_text: str) -> None:
        pass


class ConsoleView(BaseView):

    def show_message(self, text: str) -> None:
        print(text)

    def show_error(self, text: str) -> None:
        print(f"ERROR: {text}")

    def prompt(self, prompt_text: str) -> str:
        return input(prompt_text + " ")

    def show_contact(self, record) -> None:
        print(record)

    def show_contacts(self, records) -> None:
            if not records:
                print("Address book is empty")
                return
            for r in records:
                self.show_contact(r)

    def show_commands(self, help_text: str) -> None:
        print(help_text)