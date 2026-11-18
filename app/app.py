from .menu.main import main_menu


def run():
    try:
        main_menu()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D -> keluar rapi, tanpa error panjang
        print("\nSampai jumpa!")


if __name__ == "__main__":
    run()
