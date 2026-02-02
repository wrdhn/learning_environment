def list_menu(items):
    if isinstance(items, dict):
        items = list(items.keys())

    for i in range(len(items)):
        print(f"{i + 1}. {items[i]}")

    user_input = int(input("Select an option by number: "))
    return user_input - 1