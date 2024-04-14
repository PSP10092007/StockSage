import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import requests

# Set page width
st.set_page_config(layout="wide", page_title="StockSage", page_icon="📈")

# Create a tuple of stock tickers from which the user can select
stocks = ("AAPL", "ABBV", "ABT", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEP", 
        "AES", "AFL", "AIG", "AIV", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALK", 
        "ALL", "ALLE", "ALXN", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", 
        "AMZN", "ANET", "ANSS", "ANTM", "AON", "AOS", "APA", "APD", "APH", "APTV", 
           "ARE", "ATO", "ATVI", "AVB", "AVGO", "AVY", "AWK", "AXP", "AZO", "BA", "BAC", 
            "BAX", "BBY", "BDX", "BEN", "BF.B", "BIIB", "BK", "BKNG", "BKR", "BLK", "BLL", 
            "BMY", "BR", "BRK.B", "BSX", "BWA", "BXP", "C", "CAG", "CAH", "CARR", "CAT", 
            "CB", "CBOE", "CBRE", "CCI", "CCL", "CDNS", "CDW", "CE", "CERN", "CF", "CFG", 
            "CHD", "CHRW", "CHTR", "CI", "CINF", "CL", "CLX", "CMA", "CMCSA", "CME", "CMG", 
            "CMI", "CMS", "CNC", "CNP", "COF", "COG", "COO", "COP", "COST", "CPB", "CPRT", 
            "CRM", "CSCO", "CSX", "CTAS", "CTL", "CTSH", "CTVA", "CTXS", "CVS", "CVX", "CZR", 
            "D", "DAL", "DD", "DE", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DISCA", "DISCK", 
            "DISH", "DLR", "DLTR", "DOV", "DOW", "DPZ", "DRE", "DRI", "DTE", "DUK", "DVA", "DVN", 
            "DXC", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EIX", "EL", "EMN", "EMR", "ENPH", 
            "EOG", "EQIX", "EQR", "ES", "ESS", "ETFC", "ETN", "ETR", "ETSY", "EVRG", "EW", "EXC", 
            "EXPD", "EXPE", "EXR", "F", "FANG", "FAST", "FB", "FBHS", "FCX", "FDX", "FE", "FFIV", 
            "FIS", "FISV", "FITB", "FLIR", "FLS", "FLT", "FMC", "FOX", "FOXA", "FRC", "FRT", "FTNT", 
            "FTV", "GD", "GE", "GILD", "GIS", "GL", "GLW", "GM", "GOOG", "GOOGL", "GPC", "GPN", "GPS", 
            "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HBI", "HCA", "HD", "HES", "HFC", "HIG", "HII", 
            "HLT", "HOG", "HOLX", "HON", "HP", "HPE", "HPQ", "HRB", "HRL", "HSIC", "HST", "HSY", "HUM", 
            "HWM", "IBM", "ICE", "IDXX", "IEX", "IFF", "ILMN", "INCY", "INFO", "INTC", "INTU", "IP", "IPG", 
            "IPGP", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JCI", "JKHY", "JNJ", 
            "JNPR", "JPM", "K", "KEY", "KEYS", "KHC", "KIM", "KLAC", "KMB", "KMI", "KMX", "KO", "KR", "KSU", 
            "L", "LB", "LDOS", "LEG", "LEN", "LH", "LHX", "LIN", "LKQ", "LLY", "LMT", "LNC", "LNT", "LOW", 
            "LRCX", "LUV", "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", 
            "MDLZ", "MDT", "MET", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM", "MNST", "MO", "MOS", "MPC", 
            "MRK", "MRO", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTD", "MU", "MXIM", "NCLH", "NDAQ", "NEE", "NEM", 
            "NFLX", "NI", "NKE", "NLOK", "NLSN", "NOC", "NOV", "NOW", "NRG", "NUE", "NVDA", "NVR", "NWL", "NWS", 
            "NWSA", "NXPI", "O", "ODFL", "OKE", "OMC", "ORCL", "ORLY", "OTIS", "OXY", "PAYC", "PAYX", "PBCT", "PCAR", 
            "PEAK", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PKI", "PLD", "PM", "PNC", "PNR", 
            "PNW", "POOL", "PPG", "PPL", "PRGO", "PRU", "PSA", "PSX", "PVH", "PWR", "PXD", "PYPL", "QCOM", "QRVO", 
            "RCL", "RE", "REG", "REGN", "RF", "RHI", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", 
            "SBAC", "SBUX", "SCHW", "SEE", "SHW", "SIVB", "SJM", "SLB", "SNA", "SNPS", "SO", "SPG", "SPGI", "SRE", 
            "STE", "STT", "STX", "STZ", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TEL", "TER", 
            "TFC", "TFX", "TGT", "TIF", "TJX", "TMO", "TMUS", "TPR", "TROW", "TRV", "TSCO", "TSN", "TSLA", "TT", "TTWO", 
            "TWTR", "TXN", "TXT", "TYL", "UA", "UAA", "UAL", "UDR", "UHS", "ULTA", "UNH", "UNM", "UNP", "UPS", "URI", 
            "USB", "V", "VAR", "VFC", "VIAC", "VLO", "VMC", "VNO", "VRSK", "VRSN", "VRTX", "VTR", "VTRS", "VZ", "WAB", 
            "WAT", "WBA", "WDC", "WEC", "WELL", "WFC", "WHR", "WLTW", "WM", "WMB", "WMT", "WRB", "WRK", "WST", "WU", "WY", 
            "WYNN", "XEL", "XLNX", "XOM", "XRAY", "XRX", "XYL", "YUM", "ZBH", "ZBRA", "ZION", "ZTS")

# Create start date for when we should start getting our data
historical_start = "2015-01-01"
forecast_start = "2019-01-01"
# Create end date as today (current date)
today = datetime.now()
accToday = today.strftime('%Y-%m-%d')

# Sidebar content
st.sidebar.image('your_logo.png', width=50, use_column_width=True)
st.sidebar.write(
    "StockSage is an advanced stock analysis tool that provides comprehensive data and forecasts for selected stocks."
)

with st.sidebar:
    selected = option_menu(
        "Pages",
        ["Home", "Comparative Analysis"]
    )

# Load in data from Yahoo Finance
def load_data_historical(ticker):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=750)).strftime('%Y-%m-%d')
    data = yf.download(ticker, start_date, end_date)
    data.reset_index(inplace=True)
    return data[::-1]  # Reverse the order of rows


def load_data_forecast(ticker):
    data = yf.download(ticker, forecast_start, accToday)
    data.reset_index(inplace=True)
    return data

def get_news(ticker, api_key):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()['articles'][:6]  # Limit to 6 articles
        return articles
    else:
        return []

n_years = st.sidebar.slider("Prediction length (years)", 1, 4)
time = n_years * 365

if selected == "Home":
    #Title
    st.title("📊 StockSage")
    st.write(
        "Welcome to StockSage! This app provides historical data and forecasts for selected stocks."
    )

    # Create drop-down select box for user to select stock
    selected_stock = st.sidebar.selectbox("Choose stock for forecasts", stocks)

    # While data is loading, display that data is loading
    with st.spinner("Loading stock data..."):
        # Load the data
        historical_data = load_data_historical(selected_stock)
        forecast_data = load_data_forecast(selected_stock)
        news_api_key = "68173a718b8c473ba88903a2288496a0"  # Replace 'YOUR_NEWS_API_KEY' with your actual API key
        news_articles = get_news(selected_stock, news_api_key)

    # Once the data is loaded, display a message indicating completion
    st.text("Loading stock data... Complete!")

    c1, c2 = st.columns(2)
    # Create a table for historical data
    with c1:
        st.subheader('Historical Data')
        historical_data = historical_data.round(2)
        st.write(historical_data.tail(750))

    # Graph historical data using Plotly
    with c2:
        def historicalDataGraph():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['Open'], name='Stock Close'))
            fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['High'], name='Stock High'))
            fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['Low'], name='Stock Low'))
            # Create a slider under the graph for graphs to be interactive with the user
            fig.layout.update(title_text="Historical Data", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig, use_container_width=True)

        # Call historical data graph function
        historicalDataGraph()

    # Forecasting
    # Create DataFrame for predicted data
    df_train = forecast_data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    # Create a Prophet model for forecasting
    predictModel = Prophet()
    predictModel.fit(df_train)
    future = predictModel.make_future_dataframe(periods=time)
    forecast = predictModel.predict(future)

    # Caluclate additional useful metrics for user to analyze and round each metric to two decimal places
    forecast['Predicted Open'] = forecast['yhat'].shift(1).round(2)
    forecast['Predicted Change'] = (forecast['yhat'] - forecast['Predicted Open']).round(2)
    forecast['Predicted Change %'] = ((forecast['Predicted Change'] / forecast['Predicted Open']) * 100).round(2)
    forecast['Moving Average'] = forecast['yhat'].rolling(window=10).mean().round(2)
    forecast['yhat'] = forecast['yhat'].round(2)
    forecast['yhat_lower'] = forecast['yhat_lower'].round(2)
    forecast['yhat_upper'] = forecast['yhat_upper'].round(2)

    # Filter the forecasted data for future dates
    future_forecast = forecast[forecast['ds'].dt.date > today.date()]

    # Create a table for forecasted data
    st.subheader('Forecasted data')
    forecast_table = future_forecast[['ds', 'Predicted Open', 'yhat', 'yhat_lower', 'yhat_upper', 'Predicted Change', 'Predicted Change %', 'Moving Average']].rename(columns={'ds': "Date", "yhat": "Predicted Close", "yhat_lower": "Predicted Lower", "yhat_upper": "Predicted Upper"})
    st.write(forecast_table)

    # Create graph with forecasted data using Prophet and Plotly
    st.write('Forecast Graph')

    # Customize the axis on the forecasted graph
    fig1 = plot_plotly(predictModel, forecast)
    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="Stock Price"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Display recent news articles
    st.subheader("Recent News Articles")

    # Create two rows with three columns each for news articles
    c1, c2 = st.columns(2)

    i=0
    for article in news_articles:
        if 'urlToImage' in article:
            if i < 3:
                with c1:
                    st.markdown(
                        f"<a href='{article['url']}' target='_blank' style='text-decoration: none; color: #000000;'>"
                        f"<div style='display: flex; align-items: center;'>"
                        f"<img src='{article['urlToImage']}' style='max-width: 200px; border-radius: 5px; transition: transform 0.2s; margin-bottom: 10px;'>"
                        f"<h3>{article['title']}</h3>"
                        f"</div>"
                        f"</a>",
                        unsafe_allow_html=True
                    )
            else:
                with c2:
                    st.markdown(
                        f"<a href='{article['url']}' target='_blank' style='text-decoration: none; color: #000000;'>"
                        f"<div style='display: flex; align-items: center;'>"
                        f"<img src='{article['urlToImage']}' style='max-width: 200px; border-radius: 5px; transition: transform 0.2s; margin-bottom: 10px;'>"
                        f"<h3>{article['title']}</h3>"
                        f"</div>"
                        f"</a>",
                        unsafe_allow_html=True
                    )

            i = i + 1

if selected == "Comparative Analysis":
    st.title("Comparative Analysis")

    available_metrics = ("Stock Close", "Stock Open", "Stock High", "Stock Low")

    c3, c4 = st.columns(2)
    # Comparative Analysis
    with c3:
        compare_stocks = st.multiselect("Select stocks for comparison", stocks)
        metric = st.selectbox("Select the metric for comparison between the selected stocks", available_metrics)
        if compare_stocks and metric:
            comparison_data = pd.DataFrame()
            for stock in compare_stocks:
                if metric == "Stock Close":
                    comparison_data[stock] = yf.download(stock, historical_start, accToday)["Close"]
                elif metric == "Stock Open":
                    comparison_data[stock] = yf.download(stock, historical_start, accToday)["Open"]
                elif metric == "Stock High":
                    comparison_data[stock] = yf.download(stock, historical_start, accToday)["High"]
                elif metric == "Stock Low":
                    comparison_data[stock] = yf.download(stock, historical_start, accToday)["Low"]
            with c4:
                st.line_chart(comparison_data)

    if compare_stocks:
        fig = go.Figure()

        for stock in compare_stocks:
            historical_data = yf.download(stock, historical_start, accToday)["Close"]
            historical_data.index = pd.to_datetime(historical_data.index)  # Convert index to datetime

            # Load forecast data
            forecast_data = load_data_forecast(stock)
            df_train = forecast_data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

            # Create and fit Prophet model
            predictModel = Prophet()
            predictModel.fit(df_train)

            # Make future dataframe for forecasting
            future = predictModel.make_future_dataframe(periods=time)
            forecast = predictModel.predict(future)

            # Plot historical data
            #fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data.values, mode='lines', name=f'{stock} Historical'))

            # Plot forecasted data
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name=f'{stock} Forecast'))

        # Update layout of the graph
        fig.update_layout(
            title="Comparative Analysis of Stock Forecasts",
            xaxis_title="Date",
            yaxis_title="Stock Price"
        )

        fig.layout.update(title_text="Forecast Comparisons", xaxis_rangeslider_visible=True)

        # Show the graph
        st.plotly_chart(fig, use_container_width=True)
