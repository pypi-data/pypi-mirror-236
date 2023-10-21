from sqlalchemy import inspect

from output.database.database_base import engine

if __name__ == '__main__':
    inspector = inspect(engine.connect())
    equipment_dir_table = inspector.get_columns('EquipmentsDir')
    print("\033[1m\033[32mEquipmentsDir\033[0m")
    for column in equipment_dir_table:
        print('\t', column["name"], column["type"])
