# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 08:32:22 2018

@author: Andres
"""
import indicoio
from textblob import TextBlob
import pandas as pd
indicoio.config.api_key = '94ecf5c47df2baa0f6b49db7afcae0ef'
ruta_excel=r"C:\GITHUB - SYNC\TWEETS--py\output_con_alcance.xlsx"


# single example
#a=indicoio.sentiment(frase, language='spanish')#,'94ecf5c47df2baa0f6b49db7afcae0ef','spanish')
#print(a)
#b=indicoio.text_tags(frase,top_n=2)

# batch example
#indicoio.sentiment([
#    "I love writing code!",
#    "Alexander and the Terrible, Horrible, No Good, Very Bad Day"
#])


#
#blob = TextBlob(frase)
#translate=blob.translate(to="en")
#blob2=TextBlob(translate.raw)
#blob2.sentiment.polarity
#a=indicoio.sentiment(translate.raw, language='english')#,'94ecf5c47df2baa0f6b49db7afcae0ef','spanish')
#b=indicoio.analyze_text(translate.raw,apis=['emotion','people','organizations','places','keywords'])
#print(b)
#print(a)

#Vamos a importar todos los tweets

def traduce(frase):
    try:
        blob = TextBlob(frase)
        translate=blob.translate(to="en")
        return translate.raw
    except:
        return None
def blob_sentiment(frase):
    try:
        blob = TextBlob(frase)
        return blob.sentiment.polarity
    except:
        return None
def indico_sentiment(frase):
    try:
        a=indicoio.sentiment(frase, language='spanish')
        return a
    except:
        return None
        
test=pd.read_excel(ruta_excel,'tweets')
test.reset_index(inplace=True)
#test=datos.loc[[0,1,2,3,4,5,6,7,8,9]]
#test['Tweet_en']=test['Tweet'].apply(traduce)
#test['Sentiment_blob']=test['Tweet_en'].apply(blob_sentiment)
test['Sentiment_indico']=test['Tweet'].apply(indico_sentiment)

writer = pd.ExcelWriter('output_sentimientos.xlsx')
test.to_excel(writer,'tweets')
writer.save()