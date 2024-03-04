# Database Expiration Date Checker and Updater

This script allows you to check and update the expiration date of databases in a PostgreSQL instance. It includes two main functions:

1. `get_all_databases`: Retrieves a list of databases in the specified PostgreSQL instance, excluding the system databases (`postgres` and `template` databases).

2. `check_and_update_expiration_date`: Checks if the expiration date parameter (`database.expiration_date`) needs updating in each database and updates it if necessary.

## Usage

1. Ensure you have Python installed on your system.

2. Install the required dependencies using pip: pip install psycopg2

3. Modify the following parameters in the script according to your PostgreSQL setup:
   - `database_name`: Name of the initial Odoo database used to connect with the host.
   - `host`: Name of the host where PostgreSQL is running.
   - `user_name`: Username with admin privileges in the host.
   - `passwd`: Password of the specified user.
   - `db_port`: Database port.
