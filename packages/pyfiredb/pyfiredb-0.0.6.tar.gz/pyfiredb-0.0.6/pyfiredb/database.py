class Database:

    def __init__(self, database) -> None:
        self.bd = database

    def update(self, data: dict) -> None:

        database = self.bd
        if data is not None:
            database.db.update(data, database.login['idToken'])

    def update_batch(self, path: str, input: list, index: int) -> None:

        if input is []:
            return

        data: dict = {}

        for i, value in enumerate(input, index):
            value["id_list"] = i + 1
            data[f"{path}/{value['id']}"] = value

        self.update(data)

    def get(self, path: str) -> tuple:

        database = self.bd
        result = database.db.child(path).get(database.login['idToken']).val()
        return tuple(dict(result).values())

    def equal(self, path: str, param: str, equal_to: str | int) -> dict:

        database = self.bd
        result = database.db.child(path).order_by_child(param).equal_to(
            equal_to).get(database.login['idToken']).val()

        if result:
            return list(dict(result).values())[0]

    def between(self, path: str, param: str, start: int, end: int) -> tuple:

        database = self.bd
        result = database.db.child(path).order_by_child(param).start_at(
            start).end_at(end).get(database.login['idToken']).val()

        return tuple(dict(result).values())

    def max(self, path, param: str, equal_to: bool = False) -> dict:

        database = self.bd

        if equal_to:
            result = database.db.child(path).order_by_child(param).equal_to(
                equal_to).limit_to_last(1).get(database.login['idToken']).val()
        else:
            result = database.db.child(path).order_by_child(
                param).limit_to_last(1).get(database.login['idToken']).val()

        if result:
            return list(dict(result).values())[0]
        return {}
