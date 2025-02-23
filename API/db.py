import mariadb

db_config = {
    'host': 'mariadb',
    'user': 'appuser',
    'password': 'maria-DB_Appuser',
    'database': 'betMasters',
    'pool_name': 'mypool',
    'pool_size': 5
}

def get_db_connection():
    return mariadb.connect(**db_config)