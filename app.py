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

table = soup.find("table",attrs={"class":"table table-striped table-hover table-hover-solid-row table-simple history-data"})
tablebody = table.find("tbody")
tr = tablebody.find_all("tr",attrs={"class":""})

temp = [] #initiating a tuple

for i in range(1, len(tr)):
#insert the scrapping process here

	row = table.find_all("tr",attrs={"class":""})[i]
        
    #scrapping process
    
    #getDate
	date = row.find_all("td")[0].text
	date = date.strip()
        
    	#getDayName
	dayName = row.find_all("td")[1].text
	dayName = dayName.strip()
    
    	#getKurs
	kurs = row.find_all("td")[2].text
	kurs = kurs.replace("IDR","")
	kurs = kurs.replace(',','')
    
	temp.append((date,dayName,kurs)) 

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ("tanggal","hari","kurs"))


#insert data wrangling here

data["tanggal"]=data["tanggal"].astype('datetime64')
data["hari"]=data["hari"].astype('category')
data["kurs"]=data["kurs"].astype('float64')
data.set_index('tanggal')

print(data)


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {data.mean().round(2)}'

	# generate plot
	ax = data[["hari","kurs"]].plot(figsize = (20,9),title='Harga kurs setiap hari')
	ax.set_xlabel("Hari")
	ax.set_ylabel("Kurs")
	
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
