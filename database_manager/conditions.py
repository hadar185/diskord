from database_manager.consts import FIELD_PLACEHOLDER, WHERE, AND


class Conditions:
    def __init__(self, **conditions) -> None:
        self.values = list(conditions.values())

        self._conditions = ""
        for index, (field_name, value) in enumerate(conditions.items()):
            prefix = WHERE if index == 0 else AND
            self._conditions += f" {prefix} {field_name}={FIELD_PLACEHOLDER}"

    def __str__(self) -> str:
        return self._conditions
