contacts = []


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"

    return inner


@input_error
def add_contact(args, contacts):
    try:
        name, phone = args
        contacts[name] = phone
    except ValueError:
        raise ValueError("Give me name and phone please.")

    return "Contact added."


@input_error
def change_username_phone(args, contacts):
    try:
        name, phone = args
    except ValueError:
        raise ValueError("Give me name and phone please.")

    if name in contacts:
        contacts[name] = phone
        return "Contact changed."
    else:
        raise IndexError(f"Unknown contact {name}")


def render_contacts(contacts):
    for name, phone in contacts.items():
        print(f"{name} : {phone}")
    return


def phone_username(args, contacts):
    name = args[0]
    if name in contacts:
        return f"Phone: {contacts[name]}."
    else:
        raise IndexError(f"Unknown contact {name}")


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_username_phone(args, contacts))
        elif command == "phone":
            print(phone_username(args, contacts))
        elif command == "all":
            render_contacts(contacts)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
