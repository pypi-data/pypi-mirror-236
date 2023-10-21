from sqlalchemy import text

from output.database.database_base import engine

if __name__ == '__main__':
    # SQLAlchemy V1.4.45
    engine.execute('alter table User add column last_name VARCHAR (50);')
    engine.execute('alter table User add column first_name VARCHAR (50);')
    # SQLAlchemy V2.0.16
    # add_last_name_to_user = text("alter table User add column last_name VARCHAR (50);")
    # add_first_name_to_user = text("alter table User add column first_name VARCHAR (50);")
    # with engine.begin() as conn:
    #    conn.execute(add_last_name_to_user)
    #    conn.execute(add_first_name_to_user)
