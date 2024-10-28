import pandas as pd
from constants import GENAI_API_KEY
from return_calculator import ReturnCalculator
from plotter import Plotter
from typing import List
from openai import OpenAI

def main() -> None:
    API_KEY = GENAI_API_KEY

    # Check if the key is successfully loaded
    if API_KEY is None:
        raise ValueError("API key not found. Please check if your key is set up correctly.")

    tickers: List[str] = ["^SPX"]  # S&P 500 index
    start_date: str = '1990-01-01'  # Adjust the start date as needed

    return_calculator = ReturnCalculator(tickers, start_date)
    plotter = Plotter(return_calculator)

    df = pd.read_csv('demo_data.csv', parse_dates=['Date'])
    plotter.plot_skewness_entropy_and_returns(tickers[0], df, demo=True)

    # Filter data for COVID time (Sept 2019 - June 2020) and 2024 (Jan - July 31)
    covid_data = df[(df['Date'] >= '2019-09-01') & (df['Date'] <= '2020-06-30')]
    current_data = df[(df['Date'] >= '2024-01-01') & (df['Date'] <= '2024-07-31')]

    # Convert DataFrames to strings for ChatGPT prompts
    covid_data_text = covid_data.to_string(index=False)
    current_data_text = current_data.to_string(index=False)

    # Initial prompt with both datasets and training context
    initial_prompt = f"""
        You are a financial market analyst. Based on the provided data, issue a **Market Expectation** statement focused on the next 2-4 weeks.

        Below are daily data from two distinct periods: the COVID period (Sept 2019 to June 2020) and Jan 2024 to July 2024.

        COVID Data (Sept 2019 - June 2020):
        {covid_data_text}

        Current Data (Jan 2024 - July 30, 2024):
        {current_data_text}

        Key Insight:
        - A **sharp dip** in entropy means a quick and prolonged downtrend in entropy values over several days or weeks or if entropy values have declined and not stabilized at a trough.
        - Issue a cautious outlook if there a sharp dip in entropy occurred within the past 3-4 weeks.
        - If a sharp dip in entropy is detected, warn that SPX prices may decline within the next 4 weeks, and suggest risk mitigation.
        - For all other cases, indicate that the current entropy trend does not suggest imminent SPX decrease.
        - Format the response as a single, short **Market Expectation** statement.
        """

    # Set up initial messages for ChatGPT
    messages = [
        {"role": "system", "content": "You are a financial market analyst."},
        {"role": "user", "content": initial_prompt}
    ]
    client = OpenAI(api_key=API_KEY)
    print("Interactive financial insights chatbot. Type 'exit' or press Ctrl+C to quit.")

    start_chatGPT(client, messages)


def start_chatGPT(client, messages):
    try:
        while True:
            # Get user input for each question
            user_input = input("Enter your question: ")

            if user_input.lower() == "exit":
                print("Exiting the chatbot.")
                break

            # Append user question to messages
            messages.append({"role": "user", "content": user_input})

            # Debugging: Print that we are about to call the API
            print("Calling OpenAI API...")

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.2,
                    max_tokens=250,
                )

                # Print the generated message from GPT-4
                assistant_response = response.choices[0].message.content
                print("Assistant:", assistant_response)

                # Append assistant's response to messages for context in future questions
                messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                print(f"An error occurred while calling the OpenAI API: {e}")

    except KeyboardInterrupt:
        print("\nExited the chatbot using Ctrl+C.")

if __name__ == "__main__":
    main()
