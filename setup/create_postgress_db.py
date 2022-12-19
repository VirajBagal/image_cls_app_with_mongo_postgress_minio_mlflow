################################################################################
# File: create_postgress_db.py                                                 #
# Project: Spindle                                                             #
# Created Date: Sunday, 18th December 2022 11:23:28 am                         #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Sunday, 18th December 2022 6:56:02 pm                         #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2022 Synapsica                                                 #
################################################################################
import psycopg2
from time import sleep

DATABASE_NAME = "mlflow"
POSTGRESS_PASSWORD = "root"
POSTGRESS_USER = "root"
POSTGRESS_HOST = "127.0.0.1"
# establishing the connection
sleep(5)
try:
    conn = psycopg2.connect(
        database=f"{DATABASE_NAME}",
        user=f"{POSTGRESS_USER}",
        password=f"{POSTGRESS_PASSWORD}",
        host=f"{POSTGRESS_HOST}",
        port="5432",
    )
    print("Database already exists")
except psycopg2.OperationalError:
    conn = psycopg2.connect(
        database="postgres",
        user=f"{POSTGRESS_USER}",
        password=f"{POSTGRESS_PASSWORD}",
        host=f"{POSTGRESS_HOST}",
        port="5432",
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing query to create a database
    sql = f"""CREATE database {DATABASE_NAME}"""

    # Creating a database
    cursor.execute(sql)
    print("Database created successfully........")

    # Closing the connection
    conn.close()
