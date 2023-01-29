from colorama import Fore, Back, Style

def print_normal(message, disable_print=False):
    if disable_print:
        return

    print(message)

def print_error(message, disable_print=False):
    if disable_print:
        return

    print(Fore.LIGHTRED_EX + message + Fore.RESET)

def print_warning(message, disable_print=False):
    if disable_print:
        return

    print(Fore.LIGHTYELLOW_EX + message + Fore.RESET)

def print_success(message, disable_print=False):
    if disable_print:
        return

    print(Fore.LIGHTGREEN_EX + message + Fore.RESET)

def print_alert(message, disable_print=False):
    if disable_print:
        return

    print(Fore.YELLOW + message + Fore.RESET)

def print_high_alert(message, disable_print=False):
    if disable_print:
        return
        
    print(Fore.RED + message + Fore.RESET)

def print_info(message, disable_print=False):
    if disable_print:
        return

    print(Back.LIGHTBLACK_EX + message + Fore.RESET)

# print_error("test")
# print_warning("test")
# print_success("test")
# print_alert("test")
# print_info("test")