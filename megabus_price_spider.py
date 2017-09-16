#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import datetime
#import scrapy
import urllib
import json
import sys
# import os
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

    # journeys = price_json['dates'][0]['journeys'] ##obselete on 9/15/2017
    journeys = price_json['journeys']

    return journeys

def print_cheap_trips(journeys):
    for j in journeys:
        price = j['price']
        date = j['departureDateTime']
        date_str = date.split('T')[0]
        time_str = date.split('T')[1]

        time = datetime.datetime.strptime(time_str, "%H:%M:%S")
        time_str = time.strftime("%I:%M %p")


        date_split = date_str.split('-')
        day = datetime.date(year =int(date_split[0]), 
                            month=int(date_split[1]), 
                            day  =int(date_split[2]))
        week_day = day.weekday()
        
        if price < 5:
            print "{} {} = ${}  {}".format(date_str, time_str, price, calendar.day_name[week_day])


def search_ticket(days_from_today, orig, dest, weekdays=[]):
    
    today = datetime.date.today()
    
    for day in range(days_from_today):
        date = today + datetime.timedelta(day)

        if date.weekday() in weekdays:
            journeys = get_data(orig, dest, str(date))
            print_cheap_trips(journeys)

print "==== From ST CATHARINES to TORONTO: ===="
search_ticket(days_from_today = 120,
              orig            = STCATHARINES,
              dest            = TORONTO,
              weekdays        = [2,3,4])

print "\n==== From TORONTO to ST CATHARINES: ===="
search_ticket(days_from_today = 120,
              orig            = TORONTO,
              dest            = STCATHARINES,
              weekdays        = [5,6])

raw_input("Press enter to exit ;)")