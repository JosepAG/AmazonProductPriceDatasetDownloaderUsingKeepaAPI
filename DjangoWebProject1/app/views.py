"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader



import csv


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import tqdm
import asyncio
import nest_asyncio
nest_asyncio.apply()
import keepa

###function call keepa
def Create_Data_Product(entrada, place):
  
  accesskey = '5grcrbpkkeo30reskiljkn0mbn4sn26bqsmoen1u8m973sh6lgdvjmb3k8lracth' # enter real access key here
  api = keepa.Keepa(accesskey)  
  # Single ASIN query
  products = api.query(entrada,domain=place) # returns list of product data, no domain->.com; domain=ES->Spain;One of the following Amazon domains: RESERVED, US, GB, DE, FR, JP, CA, CN, IT, ES, IN, MX Defaults to US.

  # Plot result (requires matplotlib)
  #keepa.plot_product(products[0])

  #AMAZON SELLER
  name=products[0]['title']
  #lst=pd.DataFrame(list(name))
  Data_amazon_price= pd.DataFrame(products[0]['data']['AMAZON'])
  Data_amazon_timestamp= pd.DataFrame(products[0]['data']['AMAZON_time'])
  Data_amazon_timestamp
  Data_amazon_price.columns=["PRICE"]
  Data_amazon_timestamp.columns=["TIMESTAMP"]
  Data_amazon=pd.concat([Data_amazon_timestamp, Data_amazon_price], axis=1)
  Data_amazon=Data_amazon.fillna(method="ffill")
  Data_amazon.dropna(inplace=True)
  #EXTERNAL SELLER
  Data_new_price= pd.DataFrame(products[0]['data']['NEW'])
  Data_new_timestamp= pd.DataFrame(products[0]['data']['NEW_time'])
  Data_new_price.columns=["PRICE"]
  Data_new_timestamp.columns=["TIMESTAMP"]
  Data_new=pd.concat([Data_new_timestamp, Data_new_price], axis=1)
  Data_new=Data_new.fillna(method="ffill")
  Data_new.dropna(inplace=True)
  print("\n")
  return Data_amazon, Data_new, name;
####


def home(request):
    """Renders the home page."""
    #assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html')

def Send_data(request):
    asin=str(request.POST['asin'])
    website=str(request.POST['website'])
    try:
        Amazon,external,name=Create_Data_Product(asin, website)
    except:
        return render(request,'app/index.html')
    
    if 'Amazon' in request.POST:
        columna1= Amazon.TIMESTAMP
        columna2= Amazon.PRICE
        zip(columna1, columna2)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="AmazonPrice.csv"'
    if 'External' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ExternalAmazonPrice.csv"'
        columna1= external.TIMESTAMP
        columna2= external.PRICE
        zip(columna1, columna2)

    writer = csv.writer(response)
    writer.writerow([name])
    writer.writerow(["TIMESTAMP", "PRICE"])
    writer.writerows(zip(columna1,columna2))

    return response


#def plot(request):
    # Data for plotting
    #t = np.arange(0.0, 2.0, 0.01)
    #s = 1 + np.sin(2 * np.pi * t)

    #fig, ax = plt.subplots()
    #ax.plot(t, s)

    #ax.set(xlabel='time (s)', ylabel='voltage (mV)',
     #      title='About as simple as it gets, folks')
    #ax.grid()

    #response = HttpResponse(content_type = 'image/png')
    #canvas = FigureCanvasAgg(fig)
    #canvas.print_png(response)
    #return response




           



