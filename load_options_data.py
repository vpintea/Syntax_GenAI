import psycopg2
import pandas as pd
from datetime import datetime
from constants import DB_NAME, DB_HOST, DB_USER, DB_PORT, DB_PASSWORD

def load_options_data_from_db(start_date, end_date=None):
    global connection

    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )

        # Create a query to fetch data between start and end dates
        query = (f"""
            SELECT quote_date, expire_date, dte, strike, c_bid, c_ask, p_bid, p_ask, c_volume, p_volume
            FROM options_data
            WHERE quote_date >= '{start_date}' AND quote_date <= '{end_date}'
            """)

        # Load data into a pandas DataFrame
        df = pd.read_sql(query, connection)

        return df

    except Exception as e:
        print(f"Error loading data: {e}")

    finally:
        if connection:
            connection.close()