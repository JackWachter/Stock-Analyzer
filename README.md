# Stock Analysis Script

This Python script performs analysis on a stock using various sources such as Yahoo Finance, Reddit, insider trading data, Seeking Alpha, and technical analysis. It also includes a position sizer to help determine the appropriate position size for a trade based on risk parameters.

## How to Run

### Prerequisites

- Python 3 installed on your system.
- Chrome browser installed WITH up-to-date ChromeDrive in the same folder as stock.py.

### Installation

1. Clone or download the script from the repository.
2. Install the required dependencies using the provided `requirements.txt` file:
   
    ```bash
    pip install -r requirements.txt
    ```

## Code Explanation

The script utilizes Selenium for web scraping to gather information from different financial and social platforms. It fetches data about a specified stock ticker and provides various insights:

- **Yahoo Finance:** Fetches basic information, market cap, fair share price, and basic evaluation.
- **Reddit:** Analyzes sentiment by counting occurrences of positive and negative words related to the stock.
- **Insider Trading:** Looks for insider buying and selling actions.
- **Seeking Alpha:** Retrieves recent stock analysis and news.
- **Technicals:** Extracts technical indicators like RSI, institutional holdings, and stock performance.
- **Position Sizer:** Helps determine the appropriate position size based on risk, confidence level, and available capital.

Feel free to customize and adapt the script to suit your specific needs or preferences. 
This is not financial advice.
