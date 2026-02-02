from .utils.list_menu import list_menu
from ..service.data_manager import material

def main_menu():
    option = material('r')
    print("===== Main Menu =====")
    list_menu(option)

main_menu()