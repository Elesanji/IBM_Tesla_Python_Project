import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True),
                             y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True),
                             y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
                      height=900,
                      title=stock,
                      xaxis_rangeslider_visible=True)
    fig.show()

#Question 1: Use yfinance to Extract Stock Data

tesla = yf.Ticker('TSLA')
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()
print(tesla_data.head(8))

#Question 2: Use Webscraping to Extract Tesla Revenue Data

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue?utm_medium=Exinfluencer&utm_source=Exinfluencer" \
      "&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel" \
      "-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork23455606-2022-01-01 "
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, 'html5lib')
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if 'Tesla Quarterly Revenue' in table.find('th').text:
        rows = table.find_all('tr')

        for row in rows:
            col = row.find_all('td')

            if col:
                date = col[0].text
                revenue = col[1].text.replace(',', '').replace('$', '')

                tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index=True)

print(tesla_revenue)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'].astype(bool)]
print(tesla_revenue.tail())

#Question 3: Use yfinance to Extract Stock Data

gme = yf.Ticker('GME')
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)
print(gme_data.head())

#Question 4: Use Webscraping to Extract GME Revenue Data
url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html5lib")
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if 'GameStop Quarterly Revenue' in table.find('th').text:
        rows = table.find_all('tr')

        for row in rows:
            col = row.find_all('td')

            if col:
                date = col[0].text
                revenue = col[1].text.replace(',', '').replace('$', '')

                gme_revenue = gme_revenue.append({"Date": date, "Revenue": revenue}, ignore_index=True)

print(gme_revenue.tail())

#Question 5: Plot Tesla Stock Graph

make_graph(tesla_data[['Date','Close']], tesla_revenue, 'Tesla')

#Question 6: Plot GameStop Stock Graph

make_graph(gme_data[['Date','Close']], gme_revenue, 'GameStop')

