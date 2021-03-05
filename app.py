from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':"table table-striped table-hover table-hover-solid-row table-simple history-data"})
tr = table.find_all('tr', attrs={'class':""})
temp = [] #initiating a tuple

for i in range(1, len(tr)):
#insert the scrapping process here
    row = table.find_all('tr',attrs={'class':""})[i]
    
    #get tanggal
    date = row.find_all('td')[0].text
    date = date.strip()
    
    #get hari
    day = row.find_all('td')[1].text
    day = day.strip()
    
    #get nilai uang
    value = row.find_all('td')[2].text
    value = value.strip()
    
    #get tulisan
    note = row.find_all('td')[3].text
    note = note.strip()
    temp.append((date,day,value,note)) 

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('date', 'day', 'value', 'note'))
data['value'] = data['value'].replace('IDR',"",regex=True).replace(',',"",regex=True)
data['value'] = data['value'].astype('float64')

#insert data wrangling here
exchange = data[['value']].set_index(data.date)

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {round(exchange["value"].mean(),2)}'

	# generate plot
	ax = exchange.plot(figsize = (10,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
