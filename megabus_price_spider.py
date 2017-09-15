#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import datetime
import scrapy
import urllib
import json
import sys
import calendar

default_encoding = 'utf-8'
reload(sys)
sys.setdefaultencoding(default_encoding)

STCATHARINES = 427
TORONTO      = 145

def get_data(orig, dest, departDate):

    url = 'https://ca.megabus.com/journey-planner/api/journeys?originId={}&destinationId={}&departureDate={}&totalPassengers=1&concessionCount=0&nusCount=0&days=1'.format(orig, dest, departDate)

    price_html = urllib.urlopen(url).read().strip()

    price_json = json.loads(price_html)

    journeys = price_json['dates'][0]['journeys']

    return journeys

def print_cheap_trips(journeys):
    for j in journeys:
        price = j['price']
        date = j['departureDateTime']
        date_split = date.split('T')[0].split('-')
        day = datetime.date(year =int(date_split[0]), 
                            month=int(date_split[1]), 
                            day  =int(date_split[2]))
        week_day = day.weekday()
        
        if price < 5:
            print "{} = ${}  {}".format(date, price, calendar.day_name[week_day])

def search_ticket(days_from_today):
    
    today = datetime.date.today()
    
    for day in range(days_from_today):
        date = today + datetime.timedelta(day)

        if date.weekday() in [0, 4, 5, 6]:
            journeys = get_data(STCATHARINES, TORONTO, str(date))
            print_cheap_trips(journeys)

search_ticket(days_from_today = 120)
