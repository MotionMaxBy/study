import yaml


class ReaderYAML:
    __text = None
    __file_path = None
    __errors = None

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__text = self.read()

    def read(self):
        try:
            with open(self.__file_path, "r") as f:
                res = yaml.load(f, Loader=yaml.Loader)
        except Exception as e:
            self.__errors = e
            return None
        self.__errors = None
        return res

    def write(self):
        try:
            with open(self.__file_path, "w") as f:
                yaml.dump(self.__text, f)
        except Exception as e:
            self.__errors = e
        self.__errors = None

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.write()

    @property
    def path(self):
        return self.__file_path

    @property
    def is_empty(self):
        return self.__text is None

    @property
    def errors(self):
        return self.__errors
