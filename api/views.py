from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import json

@api_view(['GET'])
def home(request,city):
    session=requests.Session()
    city=city.replace(' ','+')
    html_content=session.get(f'https://en.wikipedia.org/wiki/{city}').text
    soup=BeautifulSoup(html_content,'html.parser')
    if(soup.find('a',attrs={'class': 'image'})==None):
        return HttpResponse("<h1>Oops! Cannot find <br> Try using some other name<h1>")
    flaglink=soup.find('a',attrs={'class': 'image'}).find('img')['src']
    flaglink="https:"+flaglink
    table=soup.find("table",attrs={'class': 'infobox ib-country vcard'})
    capitals=[]
    largest_cities=[]
    official_languages=[]
    population=0
    tablerow=table.find_all('tr')
    gdp=0
    areatotal=0
    s=0
    for row in tablerow:
        if(row.find('th') and row.find('th').get_text()=='Capital'):
            if(row.find('ul')):
                for city in row.find('ul').find_all('li'):
                    capitals.append(city.find('a').get_text())
            else:
                capitals.append(row.find('td').find('a').get_text())        
        
        if(row.find('th') and row.find('th').get_text()=='Largest city'):
            # print(row.find('ul'))
            if(row.find('ul')):
                for city in row.find('ul').find_all('li'):
                    largest_cities.append(city.find('a').get_text())
            else:
                largest_cities.append(row.find('td').find('a').get_text()) 
        
        if(row.find('th') and row.find('th').get_text().startswith('Official')):
            if(row.find('ul')):
                for city in row.find('ul').find_all('li'):
                    official_languages.append(city.find('a').get_text())
            else:
                official_languages.append(row.find('td').find('a').get_text())
        
        if(row.find('th') and row.find('th').get_text().endswith('2022 estimate')):
            population=(row.find('td').get_text())
          
        if(row.find('th') and row.find('th').find('a') and row.find('th').find('a').get_text()==('Area ')):
            row=tablerow[tablerow.index(row)+1]
            areatotal=row.find('td').get_text()    
        
        if(row.find('th') and row.find('th').find('a') and row.find('th').find('a').get_text()==('GDP')):
            row=tablerow[tablerow.index(row)+1]
            s=s+1
            if(s==2):
                gdp=row.find('td').get_text()                         
    
    if(len(capitals)==1):
        capitals="".join(capitals)
    if(len(largest_cities)==1):
        largest_cities="".join(largest_cities)
    if(len(official_languages)==1):
        official_languages="".join(official_languages)        
    data={'flag_link':flaglink,'capital':capitals,'largest_city':largest_cities,'official_languages':official_languages,'area_total':areatotal,
          'Population':population,'GDP_nominal':gdp}
    result = '<br>'.join(f'{key}: {value}' for key, value in data.items())
    return HttpResponse("{<br>"+result+"<br>}")
    # return Response(data)    

@api_view(['GET'])
def getData(request):
    return HttpResponse("Try searching for some country")