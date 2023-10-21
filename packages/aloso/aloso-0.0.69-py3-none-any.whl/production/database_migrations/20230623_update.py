from sqlalchemy import text

from output.database.database_base import engine

if __name__ == '__main__':
    # SQLAlchemy V1.4.45
    engine.execute('alter table User add column matricule VARCHAR (50);')
    # SQLAlchemy V2.0.16
    # add_matricule_to_user = text("alter table User add column matricule VARCHAR (50);")
    # with engine.begin() as conn:
    #    result = conn.execute(add_matricule_to_user)
