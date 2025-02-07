#! usr/bin/python3

from bs4 import BeautifulSoup
import time
from csv import DictWriter
import pprint
import datetime
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import tweepy
api=None
disc_followers=dict()
dict_locations=dict()
dict_user_from=dict()
df = pd.DataFrame(columns= ['Date', 'Name', 'Username','Followers','Location','User_From','Tweet', 'Retweets', 'Favorito'])
def init_driver(driver_type):
    if driver_type == 1:
        driver = webdriver.Firefox()
    elif driver_type == 2:
        driver = webdriver.Chrome()
    elif driver_type == 3:
        driver = webdriver.Ie()
    elif driver_type == 4:
        driver = webdriver.Opera()
    elif driver_type == 5:
        driver = webdriver.PhantomJS()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def scroll(driver, start_date, end_date, words, lang, max_time=5):
    languages = {1: 'en', 2: 'it', 3: 'es', 4: 'fr', 5: 'de', 6: 'ru', 7: 'zh'}
    url = "https://twitter.com/search?q="
    for w in words[:-1]:
        url += "{}%20OR".format(w)
    url += "{}%20".format(words[-1])
    url += "since%3A{}%20until%3A{}&".format(start_date, end_date)
    if lang != 0:
        url += "l={}&".format(languages[lang])
    url += "src=typd"
    driver.get(url)
    start_time = time.time()  # remember when we started
    while (time.time() - start_time) < max_time:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")


def scrape_tweets(driver):
    try:
        tweet_divs = driver.page_source
        obj = BeautifulSoup(tweet_divs, "html.parser")
        content = obj.find_all("div", class_="content")
        dates = []
        names = []
        tweet_texts = []
        followers = []
        usernames= []
        retweets= []
        fav_list=[]
        locations=[]
        createds=[]
        for i in content:
            date = (i.find_all("span", class_="_timestamp")[0].string).strip()
            try:
                name = (
                    i.find_all(
                        "strong",
                        class_="fullname")[0].string).strip()
            except AttributeError:
                name = "Anonymous"
            tweets = i.find("p", class_="tweet-text").strings
            try:
                retweet=i.find('button',class_='js-actionRetweet').find('span',class_='ProfileTweet-actionCountForPresentation').strings
            except Exception as e:
                print('error retweets',e)
                retweet='0'
            try:
                fav=i.find('button',class_='js-actionFavorite').find('span',class_='ProfileTweet-actionCountForPresentation').strings
            except Exception as e:
                print('error favorite',e)
                fav='0'
            try:
                username = (
                    i.find(
                        "span",
                        class_="username").find('b').string).strip()
            except Exception:
                username = "Anonymous"
            #vamos a sacar varios datos del usuario de la api
            global api
            try:
                
                if username in disc_followers:
                    f_num= disc_followers[username]
                    f_created= dict_user_from[username]
                    f_location= dict_locations[username]
                    
                else:
                    user = api.get_user(username)
                    disc_followers[username]=user.followers_count
                    dict_locations[username]=user.location
                    dict_user_from[username]=user.created_at
                    f_num=disc_followers[username]
                    f_created=dict_user_from[username]
                    f_location=dict_locations[username]
            except Exception:
                f_num=-99
                f_created=None
                f_location=None
            print(f_num, f_location, f_created)
            tweet_text = "".join(tweets)
            # hashtags = i.find_all("a", class_="twitter-hashtag")[0].string
            dates.append(date)
            names.append(name)
            usernames.append(username)
            followers.append(f_num)
            locations.append(f_location)
            createds.append(f_created)
            tweet_texts.append(tweet_text)
            retweets.append("".join(retweet))
            fav_list.append("".join(fav))

        data = {
            "date": dates,
            "name": names,
            "username": usernames,
            "followers": followers,
            "location": locations,
            "user_from": createds,
            "tweet": tweet_texts,
            "retweets": retweets,
            "favoritos": fav_list
        }

        make_csv(data)

    except Exception:
        print("Whoops! Something went wrong!")
        driver.quit()


def make_csv(data):
    global df
    l = len(data['date'])
    print("count: %d" % l)
    fieldnames = ['Date', 'Name', 'Username','Followers','Location','User_From','Tweet', 'Retweets', 'Favorito']
#        writer = DictWriter(file, fieldnames=fieldnames)
#        writer.writeheader()
    for i in range(l):
        if data['date'][i] and data['name'][i] and data['tweet'][i]:
            dfappend=pd.DataFrame([[data['date'][i], data['name'][i], data['username'][i], data['followers'][i],data['location'][i],data['user_from'][i], data['tweet'][i], data['retweets'][i], data['favoritos'][i]]], columns=fieldnames)
            df=df.append(dfappend)
#            writer.writerow({'Date': data['date'][i],
#                             'Name': data['name'][i],
#                             'Tweets': data['tweet'][i],
#                             })


def get_all_dates(start_date, end_date):
    dates = []
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    step = timedelta(days=1)
    while start_date <= end_date:
        dates.append(str(start_date.date()))
        start_date += step

    return dates


def main():
    #Conexion a twetet
    auth = tweepy.OAuthHandler('eRebPUmyr2MTWyyy3h2Dq5Lqy', 'CvpgdkRtjqq2trUVXHzyb4p0vOMEzAdsYnlBtvVGLfIjrrin3L')
    auth.set_access_token('1308447878-dh1MOCdXDciN49xw2hdBtdgJtYfJlwsQYCKlGNa', 'Jd6xcVEhP6F9GPyWabKFfM04Wufn77fUwBmqUOfk0YTWm')
    global api
    api = tweepy.API(auth)
    driver_type = 2#int(input(
#        "1) Firefox | 2) Chrome | 3) IE | 4) Opera | 5) PhantomJS\nEnter the driver you want to use: "))
    # input("Enter the words: ").split(',')
    wordsToSearch = '%23MetroTUS'.split(',')
    for w in wordsToSearch:
        w = w.strip()
    start_date = '2018-02-01'#input("Enter the start date in (Y-M-D): ")
    end_date = '2018-02-02'#input("Enter the end date in (Y-M-D): ")
    lang = 3#int(input("0) All Languages 1) English | 2) Italian | 3) Spanish | 4) French | 5) German | 6) Russian | 7) Chinese\nEnter the language you want to use: "))
    all_dates = get_all_dates(start_date, end_date)
    print(all_dates)
    for i in range(len(all_dates) - 1):
        driver = init_driver(driver_type)
        scroll(driver, str(all_dates[i]), str(
            all_dates[i + 1]), wordsToSearch, lang)
        scrape_tweets(driver)
        time.sleep(1)
        print("The tweets for {} are ready!".format(all_dates[i]))
        driver.quit()
    writer = pd.ExcelWriter('output_con_alcance2.xlsx')
    df.to_excel(writer,'tweets')
    writer.save()


if __name__ == "__main__":
    main()


