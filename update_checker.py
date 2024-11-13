import requests

current_version: str = "v1.0.1"

def split_version(_version: str) -> (int, int, int):
    s = _version[1:].split('.')

    major: int = int(s[0])
    minor: int = int(s[1])
    patch: int = int(s[2])

    return major, minor, patch

def check_latest_version():
    print(f"Current verison: {current_version}")
    url = f"https://api.github.com/repos/FaintLocket424/BinaryVideoDecoder/releases/latest"
    response = requests.get(url)

    if response.status_code == 200:
        latest_version: str = response.json().get("tag_name")
        if latest_version and latest_version != current_version:
            l_maj, l_min, l_patch = split_version(latest_version)
            c_maj, c_min, c_patch = split_version(current_version)

            if l_maj > c_maj:
                print(f"New major version available {latest_version}!")
                print("Download at https://github.com/FaintLocket424/BinaryVideoDecoder/releases/latest")
            elif l_maj < c_maj:
                print("You're running a newer version than latest, fancy.")
            elif l_min > c_min:
                print(f"New minor version available {latest_version}!")
                print("Download at https://github.com/FaintLocket424/BinaryVideoDecoder/releases/latest")
            elif l_min < c_min:
                print("You're running a newer version than the latest, fancy.")
            elif l_patch > c_patch:
                print(f"New patch available {latest_version}!")
                print("Download at https://github.com/FaintLocket424/BinaryVideoDecoder/releases/latest")
            elif l_patch < c_patch:
                print("You're running a newer version than the latest, fancy.")
        else:
            print("You're using the latest version!")
    else:
        print(f"Failed to fetch version info: {response.status_code}")

    print("")