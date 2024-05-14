import sqlite3

from datetime import datetime
from pydantic import BaseModel
from sqlite3 import Connection, Cursor
from typing import Type, List, Optional, Any

from database_manager.queries import Queries
from database_manager.conditions import Conditions
from database_manager.consts import FIELD_SEPARATOR, FIELD_PLACEHOLDER

sqlite3.register_adapter(datetime, lambda value: value.isoformat())


class DatabaseManager:
    _connection: Connection
    _cursor: Cursor

    def connect(self, database_name: str) -> None:
        self._connection = sqlite3.connect(database_name)
        self._cursor = self._connection.cursor()

    def close(self) -> None:
        self._cursor.close()
        self._connection.close()

    def execute(self, *args, **kwargs) -> Cursor:
        cursor = self._cursor.execute(*args, **kwargs)
        self._connection.commit()
        return cursor

    def insert(self, table_name: str, item: BaseModel) -> Cursor:
        field_names = FIELD_SEPARATOR.join(item.model_fields)
        values = FIELD_SEPARATOR.join(FIELD_PLACEHOLDER for field in item.model_fields)
        query = Queries.INSERT.format(table_name=table_name, fields=field_names, values=values)
        return self.execute(query, list(item.model_dump().values()))

    @staticmethod
    def row_to_model(row: List[Any], model_type: Type[BaseModel]) -> BaseModel:
        return model_type(**dict(zip(model_type.model_fields, row)))

    @staticmethod
    def rows_to_models(rows: List[List[Any]], model_type: Type[BaseModel]) -> List[BaseModel]:
        return [DatabaseManager.row_to_model(row, model_type) for row in rows]

    def select(self, table_name: str,
               model_type: Type[BaseModel],
               conditions: Optional[Conditions] = None,
               row_limit: int = 1) -> List[BaseModel]:
        query = Queries.SELECT.format(table_name=table_name, conditions=conditions)
        cursor = self.execute(query, conditions.values)
        rows = cursor.fetchmany(row_limit)
        return DatabaseManager.rows_to_models(rows, model_type)
