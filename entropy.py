# http://www.rcea.org/RePEc/pdf/wp15-14.pdf - research paper on 2 entropies
# https://www.optionsdx.com/shop/ - 2023 and prior data downloaded from here
# http://www.deltaneutral.com/ - options data after 2023
# https://pages.stern.nyu.edu/~dbackus/GE_asset_pricing/disasters/Bates%20crash%20JF%2091.PDF - initial Bates paper that used quarterly options (1-4 mo out only)
# https://elsevier-ssrn-document-store-prod.s3.amazonaws.com/07/01/25/ssrn_id959547_code741880.pdf?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHIaCXVzLWVhc3QtMSJHMEUCIQDBk4CivXUsMuwDq0%2FYazNQB8rtYG2kW%2FVjQ0Q9cwdXTgIgD9UEhzMvm5xT5m8IQIR2cIGOFwD3%2BO44k3mf6KfxVw4qvQUIexAEGgwzMDg0NzUzMDEyNTciDJYabTyDi9zLjewD1CqaBd8vdyrzZ38WmaxYRHqiXsPZC1hKTxcHdf3owBsMbw37LNLcGrF5eOX9weApRU7ehTpUW4nyupsUqiCzkRngVXoRcsDpaz9g%2Fc2ydY4BwvqUAZ38nW7xWMGoxFwbvwEXagU6voJ439%2BTQHOVPMh0y9G6VsqCXOu9ETmzxsJKp%2B8Jx9QjvDVq55MvUVpryeeMeS%2FqzKsodVp2nKaxbqbeOtJALA0sABJwkgQiHw8CX73hTa6B1LhlIaHrwUCDeb3DKKngAZrvs6Rvax7jE%2FHntk0NMgMltItZVXaHZTLRc68LfjwODNZO%2Bo34g4x6sX7MgLWFFFJeZ%2F8m%2FhV3vBS8a92MEUooapsOWAFVFy0K0zk1IvatMsiC%2BPtPw0YkgjBiZkrxR0UeiLkrv2qGvMIdLJLMaMExUpcAT6cqSnQwXA7zhJYIw%2FDEthWMvs9ydXwMqfw0UgPkhKaszmKWuT0%2BGrmqYBIgUUQK%2BJqMpBhAViy45bJ1GSE2lhc11I6Ssq%2BXSv9JkeQfG6CMIdz1bgwCYmH2eXCXcWthDEPe4LTbinzNWl%2FEUM5ywepua8jLXsXQAoijxgS4CxHeJfAb9utvp5Zj%2BhUO%2BhAwwzryo6rQgLfKEb4uqlV0vr6FRL8CJ1X%2BGCK3NPEwcJgfdRzIdMaNgads26Szr471tgm7CSyZhNDhCyLV6QMHAs00LkthEIEN9M8ysi2%2B0kTrZDLX1zu7jHbi3GPBzG7ruyC%2FawuEGp3vuc2k4H0WacSoASwGFethu15gO7ul9EdNNPFACqPArhwa0XfYB7Y89YKxKemGAM5Ag7ucFFLh7czMA0U%2FtMmnpLuB42GaP5ZxGysKH2tLo9cxq1BKUfxqaMtcLXfz%2Ft7DlfGgVUNlSLCJ5jDB1pi2BjqxAVzvN%2FU0msnO7%2BuSWI0VfH%2F8Xm5cSL7ajYBYIiq%2FWMpJBYAiGJvwPPL791Xc%2BtTQTxd9n2mFnwZS%2FTZfUtwyF9i6p%2FWw9fnZW%2Ba0c2yckqO32zx4nOnVKAKJJYmUP76zTVqHZqtLNbvpzdDMzzhvbf3c4JD6c3c%2FS4akVWVnmsmH%2B5wWK275s38OJ%2BQ4U%2BjizFy6V%2FMI4%2F1vev3wpqG1cxguxi00FxVUBBXPN11hQTt0xw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240821T184814Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAUPUUPRWER6KXSCFA%2F20240821%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=bc7f0a76da27f7c7166e234ba9fb71a99acd485caaa6d5e81595ff3d58ef3f20
# daily options data for download: https://www.cboe.com/delayed_quotes/spx/quote_table

# Tsalllis entropy best for predicting 1-day crashes like 1987
# Approximate entropy best for predicting longer-slower-duration crashes like 2008

import time
import numpy as np
import pandas as pd
from load_options_data import load_options_data_from_db
from load_daily_csv_to_db import load_daily_data_to_db

pd.set_option('display.max_columns', None)
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg', depending on your preference

def get_entropy():
    WINDOW_SIZE = 50  # Window size
    DELTA = 1  # Sliding step

    start_time = time.time()  # Start timing
    start_date = "2019-05-11"
    end_date = "2024-09-18"

    load_db_start = time.time()
    load_daily_data_to_db()
    print(f"Loading daily data to DB took {time.time() - load_db_start:.2f} seconds")

    load_data_start = time.time()
    option_data_sample = load_options_data_from_db(start_date)

    print(f"Loading options data from DB took {time.time() - load_data_start:.2f} seconds")

    clean_data_start = time.time()
    option_data_sample.dropna(subset=['quote_date', 'expire_date', 'c_bid', 'c_ask', 'p_bid', 'p_ask'], inplace=True)
    # Calculate the average price for call and put options
    # Ensure that c_bid, c_ask, p_bid, and p_ask are numeric
    option_data_sample['c_bid'] = pd.to_numeric(option_data_sample['c_bid'], errors='coerce')
    option_data_sample['c_ask'] = pd.to_numeric(option_data_sample['c_ask'], errors='coerce')
    option_data_sample['p_bid'] = pd.to_numeric(option_data_sample['p_bid'], errors='coerce')
    option_data_sample['p_ask'] = pd.to_numeric(option_data_sample['p_ask'], errors='coerce')

    option_data_sample['C_Avg'] = (option_data_sample['c_bid'] + option_data_sample['c_ask']) / 2
    option_data_sample['P_Avg'] = (option_data_sample['p_bid'] + option_data_sample['p_ask']) / 2
    option_data_sample.dropna(subset=['C_Avg', 'P_Avg'], inplace=True)
    print(f"Data cleaning and preprocessing took {time.time() - clean_data_start:.2f} seconds")

    filter_data_start = time.time()
    # Ensure we're only looking at rows where C_Avg and P_Avg are not NaN
    option_data_sample = option_data_sample[(option_data_sample['C_Avg'] != 0) & (option_data_sample['P_Avg'] != 0)]

    filtered_data = option_data_sample[(option_data_sample['dte'] > 28) & (option_data_sample['dte'] < 118)]
    print(f"Filtering data took {time.time() - filter_data_start:.2f} seconds")

    skewness_calc_start = time.time()

    def calculate_average_skewness_same_strike_same_dte(df):
        """
        Calculate skewness premium using the deepest available out-of-the-money option pairs across multiple expiries for each quote_date.

        :param df: DataFrame containing options data (already filtered for DTE > 28, DTE < 200, and valid premiums).
        :return: DataFrame with skewness premium for each quote_date.
        """

        def get_deepest_available_strikes(group):
            """
            Find the deepest available strike for both calls and puts that are available across all expiries.
            """
            # Sort by strike
            group_sorted = group.sort_values(by='strike')

            # Find the deepest call (highest strike) and deepest put (lowest strike)
            deepest_call_strike = group_sorted['strike'].max()
            deepest_put_strike = group_sorted['strike'].min()

            # Get the rows for the deepest call and put across all expiries
            call_options = group[(group['strike'] == deepest_call_strike)]
            put_options = group[(group['strike'] == deepest_put_strike)]

            if call_options.empty or put_options.empty:
                return None

            # Return the average prices for both call and put, averaging across expiries
            call_avg = call_options['C_Avg'].median()
            put_avg = put_options['P_Avg'].median()
            # call_avg_ = call_options['C_Avg'].mean()
            # put_avg_ = put_options['P_Avg'].mean()

            return call_avg, put_avg

        # Group by 'quote_date'
        grouped = df.groupby('quote_date')

        def calculate_skewness_for_group(group):
            # Get the deepest available strike for this quote_date
            result = get_deepest_available_strikes(group)
            if result is None:
                return None

            call_avg, put_avg = result

            # Ensure both call and put have valid averages
            if call_avg > 0 and put_avg > 0:
                # Calculate skewness premium
                skewness_premium = (put_avg / call_avg) - 1
                return skewness_premium
            return None

        # Apply skewness calculation for each quote_date
        skewness_data = grouped.apply(calculate_skewness_for_group).reset_index()
        skewness_data.columns = ['quote_date', 'skewness_premium']
        # Filter out extreme skewness values (e.g., by limiting the skewness ratio)
        skewness_data['skewness_premium'] = skewness_data['skewness_premium'].apply(
            lambda x: x if abs(x) < 200 else 0)
        return skewness_data

    skewness_data = calculate_average_skewness_same_strike_same_dte(filtered_data)
    print(f"Skewness calculation took {time.time() - skewness_calc_start:.2f} seconds")

    avg_skew_start = time.time()

    # Drop the EXPIRE_DATE column as it's no longer relevant
    skewness_data = skewness_data.drop(columns='expire_date', errors='ignore')
    # Calculate the average skewness premium for each QUOTE_DATE
    average_skewness = skewness_data.groupby('quote_date').max().reset_index()
    # Rename the second column to 'Average Skewness'
    average_skewness.rename(columns={"skewness_premium": 'Average Skewness'}, inplace=True)

    print(f"Averaging skewness took {time.time() - avg_skew_start:.2f} seconds")

    skewness_data = average_skewness['Average Skewness']
    quote_dates = average_skewness['quote_date']

    entropy_calc_start = time.time()

    def calculate_approximate_entropy_with_skewness(skewness_data, quote_dates, window_width=WINDOW_SIZE, sliding_step=DELTA, m=2,
                                                    r=None):
        """
        Calculate Approximate Entropy (ApEn) for a given time series with aligned dates and skewness using a sliding window.

        Parameters:
        - skewness_data: The time series data (e.g., skewness premiums).
        - quote_dates: The list of corresponding quote dates.
        - window_width: The width of the sliding window.
        - sliding_step: The step size for moving the window.
        - m: The dimension of the vectors u(m)(i) used in the ApEn calculation. Default is 2.
        - r: The tolerance level. If not provided, it will be calculated as r = 0.15 * std_dev of the data.

        Returns:
        - entropy_df: A DataFrame containing the Approximate Entropy, corresponding dates, and skewness.
        """
        N = len(skewness_data)
        if N < m + 1:
            raise ValueError("Time series is too short to calculate approximate entropy.")

        # Calculate standard deviation of the time series
        std_dev = np.std(skewness_data)

        # Set tolerance r if not provided
        if r is None:
            r = 0.15 * std_dev

        # Store results
        entropy_values = []
        aligned_skewness = []
        aligned_dates = []

        # Step 1: Create m-dimensional vectors
        def create_m_dimensional_vectors(data, m):
            vectors = np.array([data[i:i + m] for i in range(len(data) - m + 1)])
            return vectors

        # Step 2: Calculate distance between vectors
        def max_distance(v1, v2):
            return np.max(np.abs(v1 - v2))

        # Step 3: Calculate C(m)(u(m)(i)|X, r)
        def calculate_C_m(vectors, r):
            N_m = len(vectors)
            C_m = np.zeros(N_m)
            for i in range(N_m):
                for j in range(N_m):
                    if max_distance(vectors[i], vectors[j]) <= r:
                        C_m[i] += 1
                C_m[i] /= N_m
            return C_m

        # Step 4: Calculate Φ(m)(r)
        def calculate_Phi(C_m):
            return np.sum(np.log(C_m)) / len(C_m)

        # Sliding window over the skewness data
        num_windows = (N - window_width) // sliding_step + 1

        for n in range(num_windows):
            start_index = n * sliding_step
            end_index = start_index + window_width
            window_data = skewness_data[start_index:end_index]

            # Create m and (m+1)-dimensional vectors for the current window
            vectors_m = create_m_dimensional_vectors(window_data, m)
            vectors_m1 = create_m_dimensional_vectors(window_data, m + 1)

            # Calculate C(m) and C(m+1)
            C_m = calculate_C_m(vectors_m, r)
            C_m1 = calculate_C_m(vectors_m1, r)

            # Calculate Φ(m) and Φ(m+1)
            Phi_m = calculate_Phi(C_m)
            Phi_m1 = calculate_Phi(C_m1)

            # Calculate Approximate Entropy (ApEn)
            ApEn = Phi_m - Phi_m1
            entropy_values.append(ApEn)

            # Align dates with the entropy calculation (date at the end of the window)
            aligned_dates.append(quote_dates[end_index - 1])

            # Align skewness data with the entropy calculation (last skewness value in the window)
            aligned_skewness.append(window_data.iloc[-1])

        # Return the results in a DataFrame
        entropy_df = pd.DataFrame({
            'Date': aligned_dates,
            'Entropy': entropy_values,
            'Skewness': aligned_skewness
        })
        entropy_df['Date'] = pd.to_datetime(entropy_df['Date'])
        return entropy_df

    entropy = calculate_approximate_entropy_with_skewness(skewness_data, quote_dates, window_width=50, m=2)

    print(f"Entropy calculation took {time.time() - entropy_calc_start:.2f} seconds")
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

    return entropy
