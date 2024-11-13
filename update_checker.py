import requests

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def split_version(_version: str) -> (int, int, int):
    s = _version[1:].split('.')

    major: int = int(s[0])
    minor: int = int(s[1])
    patch: int = int(s[2])

    return major, minor, patch


def new_version_available(_release_notes: str):
    print("Download at https://github.com/FaintLocket424/BinaryVideoDecoder/releases/latest")
    print("Release notes:")

    for note in _release_notes.split('\n'):
        print(f"\t- {note}")


def check_latest_version(_current_verison):
    url = f"https://api.github.com/repos/FaintLocket424/BinaryVideoDecoder/releases/latest"
    response = requests.get(url)

    if response.status_code == 200:
        latest_version: str = response.json().get("tag_name")
        if latest_version and latest_version != _current_verison:
            l_maj, l_min, l_patch = split_version(latest_version)
            c_maj, c_min, c_patch = split_version(_current_verison)

            release_notes = response.json().get("body")

            if l_maj > c_maj:
                print(f"{BColors.WARNING}New major version available {latest_version}!{BColors.ENDC}")
                new_version_available(release_notes)
            elif l_maj < c_maj:
                print("You're running a newer version than latest, fancy.")
            elif l_min > c_min:
                print(f"{BColors.WARNING}New minor version available {latest_version}!{BColors.ENDC}")
                new_version_available(release_notes)
            elif l_min < c_min:
                print("You're running a newer version than the latest, fancy.")
            elif l_patch > c_patch:
                print(f"{BColors.WARNING}New patch available {latest_version}!{BColors.ENDC}")
                new_version_available(release_notes)
            elif l_patch < c_patch:
                print(f"{BColors.OKCYAN}You're running a newer version than the latest, fancy.{BColors.ENDC}")
        else:
            print("You're using the latest version!")
    else:
        print(f"Failed to fetch version info: {response.status_code}")

    print("")
