""" The database of the entire app """


class Database():
    """ The database model """

    def __init__(self, table):
        self.table = table

        self.tables = {
            "users": [],
            "parties": [],
            "offices": [],
            "candidates": [],
            "votes": []
        }

    def get_items(self):
        return self.tables[self.table]

    def clear(self):
        # clears the entire database
        for key in self.tables.items:
            self.tables[key] = []
