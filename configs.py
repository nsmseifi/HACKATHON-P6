

class Database:
    db_user ='Drepuser'
    db_pass = 'Dreppass'
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'Drep'



DATABASE_URI = 'postgres+psycopg2://{}:{}@{}:{}/{}'.format(Database.db_user, Database.db_pass,
                                                                                Database.db_host, Database.db_port,
                                                                                Database.db_name)

ADMINISTRATORS = ['Admin','nsm','kk']
SIGNUP_USER = 'signup_user'



