import yaml


def main():
    data = {
        "user": "master",
        "role": "root",
        "hash": "12345dsfgh66789",
        "code": 200,
        "active": True,
    }
    file_data = {
        "info": "File for python save tests",
        "data": data,
    }
    file_path = r"d:/test_config.yaml"

    msg = """Input KEY: 
        [r] for read file, 
        [i] for read file info, 
        [f] to change info, 
        [w] to write file,
        [x] to exit
        """

    while True:
        key = input(msg)
        if key == "r":
            with open(file_path, "r", encoding="UTF-8") as file:
                file_data = yaml.load(file, Loader=yaml.Loader)
        elif key == "i":
            print(file_data["info"])
        elif key == "f":
            new_info = input("Input new info:\n").strip()
            file_data["info"] = new_info
        elif key == "w":
            with open(file_path, "w", encoding="UTF-8") as file:
                yaml.dump(file_data, file)
        elif key == "x":
            break


if __name__ == '__main__':
    main()
