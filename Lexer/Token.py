class Token:
    def __init__(self, coord, type, code, value):
        self.coord = coord
        self.type = type
        self.code = code
        self.value = value

    def get_str(self):
        tab = "\t" * 2
        return f"{self.coord}{tab}" \
               f"{self.type}{tab}" \
               f"{self.code}{tab}" \
               f"{self.value}"

    def get_type(self):
        return self.type

    def get_coord(self):
        return self.coord

    def get_code(self):
        return self.code

    def get_value(self):
        return self.value
