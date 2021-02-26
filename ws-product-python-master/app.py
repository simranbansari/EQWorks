# -*- coding: utf-8 -*-

import os
from flask import Flask, jsonify
import sqlalchemy
import datetime as dt

app = Flask(__name__)

engine = sqlalchemy.create_engine(os.getenv('SQL_URI'))

global homeCount
global homeStart
homeCount = 0
homeStart = dt.datetime.now()

@app.route('/')
def index():
    nowTime = dt.datetime.now()

    global homeStart
    global homeCount

    difference = (nowTime - homeStart).total_seconds()
    
    if difference >= 10:
        homeCount = 1
        homeStart = dt.datetime.now()

        return 'Welcome to EQ Works 😎'
    
    else:
        if homeCount == 5:
            wait_time = 10 - difference
            return 'Too many requests, ' + str(round(wait_time, 2)) + ' seconds until you can request again'

        else:
            homeCount += 1
            return 'Welcome to EQ Works 😎'
    


global eHourCount
eHourCount = 0

global event_hour_start
event_hour_start = dt.datetime.now()

@app.route('/events/hourly')
def events_hourly():
    nowTime = dt.datetime.now()

    global event_hour_start
    global eHourCount

    difference = (nowTime - event_hour_start).total_seconds()

    if difference >= 10:
        eHourCount = 1
        event_hour_start = dt.datetime.now()

        return queryHelper('''
        SELECT date, hour, events
        FROM public.hourly_events
        ORDER BY date, hour
        LIMIT 168;
        ''')
    
    else:
        if eHourCount == 5:
            wait_time = 10 - difference
            return 'Too many requests, ' + str(round(wait_time, 2)) + ' seconds until you can request again'

        else:
            eHourCount += 1
            return queryHelper('''
            SELECT date, hour, events
            FROM public.hourly_events
            ORDER BY date, hour
            LIMIT 168;
            ''')


global eventDailyCount
eventDailyCount = 0

global eDailyStart
eDailyStart = dt.datetime.now()

@app.route('/events/daily')
def events_daily():
    nowTime = dt.datetime.now()

    global eDailyStart
    global eventDailyCount

    difference = (nowTime - eDailyStart).total_seconds()# time since the beginning of current interval

    if difference >= 10:
        eventDailyCount = 1
        eDailyStart = dt.datetime.now()

        return queryHelper('''
        SELECT date, SUM(events) AS events
        FROM public.hourly_events
        GROUP BY date
        ORDER BY date
        LIMIT 7;
        ''')
    
    else:
        if eventDailyCount == 5:
            wait_time = 10 - difference
            return 'Too many requests, ' + str(round(wait_time, 2)) + ' seconds until you can request again'

        else:
            eventDailyCount += 1
            return queryHelper('''
            SELECT date, SUM(events) AS events
            FROM public.hourly_events
            GROUP BY date
            ORDER BY date
            LIMIT 7;
            ''')


global sHourlyCount
sHourlyCount = 0

global sHourlyStart
sHourlyStart = dt.datetime.now()

@app.route('/stats/hourly')
def stats_hourly():

    nowTime = dt.datetime.now()

    global sHourlyStart
    global sHourlyCount

    difference = (nowTime - sHourlyStart).total_seconds()

    if difference >= 10:
        sHourlyCount = 1
        sHourlyStart = dt.datetime.now()

        return queryHelper('''
        SELECT date, hour, impressions, clicks, revenue
        FROM public.hourly_stats
        ORDER BY date, hour
        LIMIT 168;
        ''')
    
    else:
        if sHourlyCount == 5:
            wait_time = 10 - difference
            return 'Too many requests, ' + str(round(wait_time, 2)) + ' seconds until you can request again'

        else:
            sHourlyCount += 1
            return queryHelper('''
            SELECT date, hour, impressions, clicks, revenue
            FROM public.hourly_stats
            ORDER BY date, hour
            LIMIT 168;
            ''')
    

global sDailyCount
sDailyCount = 0

global sDailyStart
sDailyStart = dt.datetime.now()

@app.route('/stats/daily')
def stats_daily():
    nowTime = dt.datetime.now()

    global sDailyStart
    global sDailyCount

    difference = (nowTime - sDailyStart).total_seconds()

    if difference >= 10:
        sDailyCount = 1
        sDailyStart = dt.datetime.now()

        return queryHelper('''
            SELECT date,
                SUM(impressions) AS impressions,
                SUM(clicks) AS clicks,
                SUM(revenue) AS revenue
            FROM public.hourly_stats
            GROUP BY date
            ORDER BY date
            LIMIT 7;
        ''')
    
    else:
        if sDailyCount == 5:
            wait_time = 10 - difference
            return 'Too many requests, ' + str(round(wait_time, 2)) + ' seconds until you can request again'

        else:
            sDailyCount += 1
            return queryHelper('''
                SELECT date,
                    SUM(impressions) AS impressions,
                    SUM(clicks) AS clicks,
                    SUM(revenue) AS revenue
                FROM public.hourly_stats
                GROUP BY date
                ORDER BY date
                LIMIT 7;
            ''')
        

global poi_count
poi_count = 0

global poi_start
poi_start = dt.datetime.now()

@app.route('/poi')
def poi():
    nowTime = dt.datetime.now()

    global poi_start
    global poi_count

    difference = (nowTime - poi_start).total_seconds()

    if difference >= 10:
        poi_count = 1
        poi_start = dt.datetime.now()

        return queryHelper('''
        SELECT *
        FROM public.poi;
        ''')
    
    else:
        if poi_count == 5:
            wait_time = 10 - difference
            return 'Too many requests, ' + str(round(wait_time, 2)) + ' seconds until you can request again'

        else:
            poi_count += 1
            return queryHelper('''
            SELECT *
            FROM public.poi;
            ''')


def queryHelper(query):
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        return jsonify([dict(row.items()) for row in result])
