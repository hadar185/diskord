class Queries:
    INSERT = "INSERT INTO {table_name} ({fields}) VALUES({values})"
    SELECT = "SELECT * FROM {table_name}{conditions}"
