from newsapi import NewsApiClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import re
import datetime

def update(event, context):
    # Init
    newsapi = NewsApiClient(api_key='62e182bf047f419aa6e34e7461af8c55')
    #This chunk gets the top 100 articles from all sources by date (max allowed by developer keys)
    
    article_list = []
    for i in range(1,6):
        # /v2/everything
        all_articles = newsapi.get_everything(q='distillery sanitizer',
                                          language='en',
                                          sort_by='publishedAt',
                                          page = i)
        article_list = article_list + all_articles['articles']
        if all_articles.get('totalResults') == 0: break
    
    
    #Load in the list of distilleries not yet added to the list by gsheets
    
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name('first-cascade-249214-20fe169d5a4f.json', scope)
    
    gc = gspread.authorize(credentials)
    
    wks = gc.open("Distilleries").sheet1
    distilleries = wks.col_values(1)
    distilleries = distilleries[1:]
    
    unlisted_producers = []
    namedArticles = []
    for article in article_list:
        for distiller in distilleries:
            if distiller == '' or not distiller or not article.get('content') or not article.get('description'): continue
            if re.search(distiller, ' '.join([article.get('title'), article.get('description'), article.get('content')]), re.IGNORECASE):
                unlisted_producers.append(distiller)
                namedArticles.append(article)
    
    #Update the producers sheet, and remove each found distiller from the master list
    producers_sheet = gc.open_by_key("1iAzOOs4YL1N2LYIZycCF8uBGAFyQ8-3LL17OxRVJLfY").sheet1
    for producer in unlisted_producers:
        row = wks.find(producer).row
        info = wks.row_values(row=row)
        wks.delete_row(row)
        producers_sheet.append_row(info)
    producers_sheet.update('H1', f"Updated {datetime.datetime.now()}")
    wks.update('H1', f"Updated {datetime.datetime.now()}")

if __name__ == '__main__':
    update("", "")