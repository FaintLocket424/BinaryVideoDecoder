import requests

from BColours import BColours


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
        print(f"\t{note}")


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
                print(f"{BColours.WARNING}New major version available {latest_version}!{BColours.ENDC}")
                new_version_available(release_notes)
            elif l_maj < c_maj:
                print("You're running a newer version than latest, fancy.")
            elif l_min > c_min:
                print(f"{BColours.WARNING}New minor version available {latest_version}!{BColours.ENDC}")
                new_version_available(release_notes)
            elif l_min < c_min:
                print("You're running a newer version than the latest, fancy.")
            elif l_patch > c_patch:
                print(f"{BColours.WARNING}New patch available {latest_version}!{BColours.ENDC}")
                new_version_available(release_notes)
            elif l_patch < c_patch:
                print(f"{BColours.OKCYAN}You're running a newer version than the latest, fancy.{BColours.ENDC}")
        else:
            print("You're using the latest version!")
    else:
        print(f"Failed to fetch version info: {response.status_code}")

    print("")
