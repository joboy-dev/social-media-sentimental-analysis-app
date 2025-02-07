from typing import Any, Dict, List
import streamlit as st

from database.conn import conn


class DBHandler:
    
    def __init__(self):
        self.conn = conn
     
    def execute(self, query, params=()):
        with self.conn.session as s:
            s.execute(query, dict(params))
            s.commit()
            # self.conn.close()
     
    def create_table(self, table_name: str, columns: Dict[str, Dict[str, Any]]):
        """
        Create a table with advanced column definitions.

        Args:
            table_name (str): Name of the table to create.
            columns (Dict[str, Dict[str, Any]]): Column definitions with additional attributes.
            
            Example usage:
            columns = {
                "id": {"type": "VARCHAR", "primary_key": True, "not_null": True},
                "name": {"type": "TEXT", "not_null": True, "unique": True},
                "email": {"type": "TEXT", "default": "unknown@example.com"},
                "age": {"type": "INTEGER", "default": 18},
                "created_at": {"type": "DATETIME", "default": "CURRENT_TIMESTAMP"}
            }
        """
        column_definitions = []
        
        for column_name, attributes in columns.items():
            column_def = [column_name]
            column_def.append(attributes.get("type", "TEXT"))  # Default type is TEXT
            
            if attributes.get("primary_key"):
                column_def.append("PRIMARY KEY")
            if attributes.get("not_null"):
                column_def.append("NOT NULL")
            if attributes.get("unique"):
                column_def.append("UNIQUE")
            if "default" in attributes:
                default_value = attributes["default"]
                # Handle default values properly for strings vs numbers
                default_value = f"'{default_value}'" if isinstance(default_value, str) else default_value
                column_def.append(f"DEFAULT {default_value}")
            
            column_definitions.append(" ".join(column_def))
        
        column_definitions_str = ", ".join(column_definitions)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions_str})"
        self.execute(query)
     
    def create_index(self, table_name: str, column_names: List[str]):
        """
        Create an index on a table column.

        Args:
            table_name (str): Name of the table.
            column_names (str): Name of the column to create the index on.
        """
        for column in column_names:
            query = f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{column} ON {table_name} ({column})"
            self.execute(query)
 
    def insert_row(self, table_name: str, data: Dict):
        column_names = ', '.join(data.keys())
        placeholder_values = ', '.join(['?' for _ in data.values()])
        query = f"INSERT OR IGNORE INTO {table_name} ({column_names}) VALUES ({placeholder_values})"
        self.execute(query, tuple(data.values()))
     
    def update_row(self, table_name, data: Dict, filter_field: str = 'id'):
        set_values = ', '.join([f"{column} =?" for column in data.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE {filter_field} =?"
        self.execute(query, tuple(data.values()) + (data[filter_field],))
 
    def delete_row(self, table_name, id: int):
        query = f"DELETE FROM {table_name} WHERE id =?"
        self.execute(query, (id,))
     
    def select(self, table_name: str, columns: str = "*", condition: str = None, params: tuple = ()):
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        data = self.conn.query(query)
        return st.dataframe(data)

    def drop_table(self, table_name: str):
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.execute(query)
 
 
handler = DBHandler()
