import psycopg2
from psycopg2 import sql
from datetime import datetime



def get_all_databases(database_name, host, user_name, passwd, db_port):
    """Get all database names form the specified host
    :param database_name: the name of the initial odoo database used to connect with the host
    :param host: the name of the host
    :param user_name: username with admin privileges in host
    :param passwd: passwd of the specified user
    :param db_port: database port
    :return final_databases: list of databases in the specified instance, excluding postgres database and template databases
    """
    # Connection parameters for the PostgreSQL instance
    instance_params = {
        'host': host,
        'database': database_name,
        'user': user_name,
        'password': passwd,
        'port': db_port,
    }

    try:
        # Establish a connection to the PostgreSQL instance
        instance_connection = psycopg2.connect(**instance_params)
        instance_cursor = instance_connection.cursor()

        # Get the list of all databases
        instance_cursor.execute("SELECT datname FROM pg_database;")
        databases = instance_cursor.fetchall()
        # Initialize final databases variable
        final_databases = []

        if databases:
            for database in databases:
                print(database)
                if database[0] == 'postgres' or database[0].startswith('template'):
                    continue
                else:
                    final_databases.append(database[0])

        return final_databases

    except psycopg2.Error as e:
        print(f"Error connecting to the PostgreSQL instance: {e}")

    finally:
        # Close the PostgreSQL instance connection
        if instance_connection:
            instance_cursor.close()

            instance_connection.close()

def check_and_update_expiration_date(database_name,host,user_name,passwd,db_port,new_expiration_date):
    """Check and update expiration date of the databases in the host, if necessary
           :param database_name: the name of the initial odoo database used to connect with the host
           :param host: the name of the host
           :param user_name: username with admin privileges in host
           :param passwd: passwd of the specified user
           :param db_port: database port
           :return final_databases: list of databases in the specified instance, excluding postgres database and template databases
    """
    db_params = {
        'host': host,
        'database': database_name,
        'user': user_name,
        'password': passwd,
        'port': db_port,
    }

    #Query to check expiration

    select_query = "SELECT * FROM ir_config_parameter WHERE key='database.expiration_date';"

    #Query to upgrade

    upgrade_query = "UPDATE ir_config_parameter SET value = %s WHERE key='database.expiration_date';"

    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute(select_query)
        result = cursor.fetchone()

        #Check if exp date need update:

        if result and result[1] != new_expiration_date:
            cursor.execute(upgrade_query,(new_expiration_date,))
            connection.commit()
            print(f"Expiration date updated successfully in database '{database_name}'.")
        else:
            print(f"No update needed or record not found in database '{database_name}'.")
    except psycopg2.Error as e:
        print(f"Error in database '{database_name}': {e}")
    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    #Database and credentials
    database_name = "postgres"
    host = "localhost"
    user_name = "postgres"
    passwd = "postgres"
    db_port = "5433"

    #Expiration date
    new_expiration_date = "2100-02-11 17:01:10"

    #List of all databases scpeificef in instance
    databases = get_all_databases(database_name,host,user_name,passwd,db_port)

    try:
        if databases:
            for databases in databases:
                check_and_update_expiration_date(databases,host,user_name,passwd,db_port,new_expiration_date)
        else:
            print(f'There is not database in selected instance.')

    except Exception as e:
        print(f'An error ocurred: {e}')
