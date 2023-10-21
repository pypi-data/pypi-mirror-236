from sqlalchemy import text

from output.database.database_base import engine

if __name__ == '__main__':
    change_column_name_to_directory_name = \
        text("alter table EquipmentsDir RENAME COLUMN name TO directory_name;")
    add_name_equipment_directory_to_equipment_dir = text(
        "alter table EquipmentsDir add column name_equipment_directory VARCHAR (50);")
    add_directory_path_to_equipment_dir = text("alter table EquipmentsDir add column directory_path VARCHAR (50);")
    add_server_host_to_equipment_dir = text("alter table EquipmentsDir add column server_host VARCHAR (50);")
    add_server_user_to_equipment_dir = text("alter table EquipmentsDir add column server_user VARCHAR (50);")
    # add_server_password_to_equipment_dir = text("alter table EquipmentsDir add column server_password VARCHAR (50);")

    with engine.begin() as conn:
        conn.execute(change_column_name_to_directory_name)
        conn.execute(add_name_equipment_directory_to_equipment_dir)
        conn.execute(add_directory_path_to_equipment_dir)
        conn.execute(add_server_host_to_equipment_dir)
        conn.execute(add_server_user_to_equipment_dir)
        # conn.execute(add_server_password_to_equipment_dir)
