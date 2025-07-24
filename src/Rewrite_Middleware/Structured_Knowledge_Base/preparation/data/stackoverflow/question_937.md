# Dynamic Merging of Pandas Dataframes
[Link to question](https://stackoverflow.com/questions/51011390/dynamic-merging-of-pandas-dataframes)
**Creation Date:** 1529854576
**Score:** 2
**Tags:** python, pandas, append
## Question Body
<p>I am writing a program in python which asks the user to select 5 symbols. After the user selects five symbols the program will provide various outputs. </p>

<p>The way the program currently works it creates five uniquely named pandas dataframes and then joins them into one frame as below.</p>

<pre><code>data1 = pdr.DataReader(symbol, 'iex', start, end)
data2 = pdr.DataReader(symbol, 'iex', start, end)
data3 = pdr.DataReader(symbol, 'iex', start, end)
data4 = pdr.DataReader(symbol, 'iex', start, end)
data5 = pdr.DataReader(symbol, 'iex', start, end)
</code></pre>

<p>I want to improve the program so the user could select any number of stocks and the program would build one pandas dataframe. I am thinking it would be similar to an append query in a SQL database. For the purposes of this question I am keeping the symbol list static in size.</p>

<pre><code>import pandas
import pandas_datareader as pdr
from datetime import datetime

start = datetime(2018, 5, 1)
end = datetime(2018, 5, 31)

symbol_list = ['IVV', 'EWH', 'INDY', 'EWG', 'ENZL']
for symbols in Symbol_List:
    symbol = symbols
    data = pdr.DataReader(symbol, 'iex', start, end)
</code></pre>

<p>add something here to append the new data into a master dataframe. </p>

<p>The append would need to rewrite the column names to include the symbols, add the columns for the new data, and ensure the data index lines up.</p>

<p>I was thinking something like:</p>

<pre><code>data.rename(columns={'high': 'high' + symbol, 'low': 'low' + symbol}, inplace=True)
pd.merge(masterdata, data, on='index')
</code></pre>

## Answers
### Answer ID: 51011495
<p>I think need <a href="http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.add_suffix.html" rel="nofollow noreferrer"><code>add_suffix</code></a> with list comprehension and <a href="http://pands.pydata.org/pandas-docs/stable/generated/pandas.concat.html" rel="nofollow noreferrer"><code>concat</code></a> for join together:</p>

<pre><code>data = pd.concat([pdr.DataReader(s, 'iex', start, end).add_suffix(s) for s in symbol_list], axis=1)
</code></pre>

