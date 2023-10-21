from sqlalchemy import text

from output.database.database_base import engine

if __name__ == '__main__':
    remove_directory_name_to_equipment_dir = text("alter table EquipmentsDir drop column directory_name;")

    with engine.begin() as conn:
        conn.execute(remove_directory_name_to_equipment_dir)
