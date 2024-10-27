import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from constants import DB_NAME, DB_HOST, DB_USER, DB_PORT, DB_PASSWORD, DAILY_DATA_FOLDER, ARCHIVE_FOLDER
import shutil

def load_daily_data_to_db():
    # Database connection settings
    db_params = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'host': DB_HOST,
        'port': DB_PORT,
        'password': DB_PASSWORD  # Add password if necessary
    }

    # Ensure the archive folder exists
    if not os.path.exists(ARCHIVE_FOLDER):
        os.makedirs(ARCHIVE_FOLDER)

    # Connect to the PostgreSQL database
    def connect_db():
        try:
            conn = psycopg2.connect(**db_params)
            print("Database connected successfully")
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    # Delete existing data for the quote date
    def delete_existing_data(conn, quote_date):
        try:
            cursor = conn.cursor()
            delete_query = sql.SQL("DELETE FROM options_data WHERE quote_date = %s")
            cursor.execute(delete_query, [quote_date])
            conn.commit()
            print(f"Deleted existing data for quote date: {quote_date}")
        except Exception as e:
            print(f"Error deleting data for quote date {quote_date}: {e}")
            conn.rollback()

    # Process and insert new data into the database in bulk
    def process_and_insert_data_bulk(conn, csv_file):
        try:
            # Extract the quote date from the file name
            file_name = os.path.basename(csv_file)
            date_part = file_name.split('_')[-2:]
            month = date_part[0]
            day = date_part[1].replace('.csv', '')
            quote_date_str = f"2024-{month}-{day}"  # Assuming the year is 2024
            quote_date = pd.to_datetime(quote_date_str)

            print(f"Processing file: {csv_file} with quote date: {quote_date}")

            # Delete existing data for the quote date before inserting new data
            delete_existing_data(conn, quote_date)

            # Read the file lines to get the UNDERLYING_LAST value from the second line
            with open(csv_file, 'r') as f:
                lines = f.readlines()

            quote_line = lines[1]
            # Extract the UNDERLYING_LAST from the 'Last: 5503.4102' part of the line
            underlying_last_str = quote_line.split(',')[1].replace('Last: ', '').strip()
            underlying_last = float(underlying_last_str)

            # Load the actual option data starting from row 5 (skipping the first 4 rows)
            df = pd.read_csv(csv_file, delimiter=',', skiprows=4, low_memory=False)

            # Rename the first column dynamically to 'expire_date'
            df.rename(columns={df.columns[0]: 'expire_date'}, inplace=True)

            # Rename other columns for easier access, including greeks and open interest
            df.columns = [
                'expire_date', 'Calls', 'C_Last Sale', 'C_Net', 'C_Bid', 'C_Ask', 'C_Volume', 'C_IV', 'C_Delta',
                'C_Gamma', 'C_Open Interest', 'Strike', 'Puts', 'P_Last Sale', 'P_Net', 'P_Bid', 'P_Ask', 'P_Volume',
                'P_IV', 'P_Delta', 'P_Gamma', 'P_Open Interest'
            ]

            # Add error handling for invalid date formats in 'expire_date'
            def parse_expiration_date(expire_date):
                try:
                    return pd.to_datetime(expire_date, errors='coerce')
                except Exception as e:
                    print(f"Error parsing expiration date: {expire_date} - {e}")
                    return pd.NaT

            # Apply date parsing with error handling to the 'expire_date' column
            df['expire_date'] = df['expire_date'].apply(parse_expiration_date)

            # Calculate Days to Expiry (DTE), skip rows with invalid expiration dates
            df['DTE'] = (df['expire_date'] - quote_date).dt.days

            # Add the Quote Date and Underlying Last (extracted from the second line)
            df['QUOTE_DATE'] = quote_date
            df['UNDERLYING_LAST'] = underlying_last

            # Select and reorder columns to match the database schema (including the new greeks and open interest)
            df_cleaned = df[[
                'QUOTE_DATE', 'UNDERLYING_LAST', 'expire_date', 'DTE', 'C_Volume', 'C_Bid', 'C_Ask', 'C_IV', 'C_Delta',
                'C_Gamma', 'C_Open Interest', 'Strike', 'P_Bid', 'P_Ask', 'P_Volume', 'P_IV', 'P_Delta', 'P_Gamma', 'P_Open Interest'
            ]]

            # Drop rows where expire_date is NaT (invalid expiration dates)
            df_cleaned = df_cleaned.dropna(subset=['expire_date']).copy()

            # Sort by quote_date and then by strike
            df_cleaned = df_cleaned.sort_values(by=['QUOTE_DATE', 'expire_date', 'Strike'])

            # Ensure there are no missing or invalid rows (rows with required columns missing)
            valid_rows_count = len(
                df_cleaned.dropna(subset=['QUOTE_DATE', 'expire_date', 'C_Bid', 'C_Ask', 'P_Bid', 'P_Ask']))

            # Ensure the number of valid rows matches the number of data rows in the file
            expected_row_count = len(df) - len(df[df.isnull().all(axis=1)])  # Removing blank rows from count

            if valid_rows_count != expected_row_count:
                print(f"Row count mismatch in {csv_file}. Expected {expected_row_count}, found {valid_rows_count}. Skipping insert.")
                return False

            # Insert data into the database, including new greeks and open interest columns
            cursor = conn.cursor()

            insert_query = sql.SQL("""
                INSERT INTO options_data (quote_date, 
                underlying_last, 
                expire_date, 
                dte, 
                c_volume, 
                c_bid, 
                c_ask, 
                c_iv, 
                c_delta, 
                c_gamma, 
                c_open_interest,
                strike, 
                p_bid, 
                p_ask, 
                p_volume, 
                p_iv, 
                p_delta, 
                p_gamma, 
                p_open_interest)
                VALUES %s
                ON CONFLICT DO NOTHING
            """)

            rows = [
                (row['QUOTE_DATE'], row['UNDERLYING_LAST'], row['expire_date'], row['DTE'], row['C_Volume'],
                 row['C_Bid'], row['C_Ask'], row['C_IV'], row['C_Delta'], row['C_Gamma'], row['C_Open Interest'],
                 row['Strike'], row['P_Bid'], row['P_Ask'], row['P_Volume'], row['P_IV'], row['P_Delta'], row['P_Gamma'], row['P_Open Interest'])
                for _, row in df_cleaned.iterrows()
            ]

            from psycopg2.extras import execute_values
            execute_values(cursor, insert_query, rows)

            conn.commit()
            print(f"Data from {csv_file} inserted successfully. {valid_rows_count} rows added.")

            return True

        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            return False

    # Main function to handle new file processing
    def process_new_files():
        conn = connect_db()
        if not conn:
            return

        # Check if the daily data folder exists and has files
        files_to_process = [f for f in os.listdir(DAILY_DATA_FOLDER) if f.endswith(".csv")]

        if not files_to_process:
            print("No new files to process.")
            return

        # Process each new CSV file in the folder
        for csv_file in files_to_process:
            csv_path = os.path.join(DAILY_DATA_FOLDER, csv_file)
            success = process_and_insert_data_bulk(conn, csv_path)

            # If the processing was successful, move the file to the archive folder
            if success:
                shutil.move(csv_path, os.path.join(ARCHIVE_FOLDER, os.path.basename(csv_file)))
                print(f"File {csv_file} moved to archive folder.")
        conn.close()

    process_new_files()


# Automatically run the function to load daily data into the DB
if __name__ == "__main__":
    load_daily_data_to_db()
