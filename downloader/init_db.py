from . import db

def init():
    conn = db.get_db_connection()
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS login;')
    create_logn_tbl = """CREATE TABLE login (
                                            id serial PRIMARY KEY,
                                            username varchar(50) NOT NULL,
                                            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                            action varchar(10) NOT NULL
                                            );
    """
    cur.execute(create_logn_tbl)

    conn.commit()

    cur.close()