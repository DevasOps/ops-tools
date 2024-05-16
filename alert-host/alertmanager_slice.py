# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timezone, timedelta
import json
import schedule
import time
import pandas as pd

def time_change(start_hour, start_min, end_hour, end_min):
    # 获取当前时间和明天的时间
    current_time = datetime.now()
    tomorrow = current_time + timedelta(days=1)
    # 构造北京时间的今天23:00
    start_bj_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, start_hour, start_min, 0)
    end_bj_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, end_hour, end_min, 0)
    # 将北京时间转换为UTC时间
    start_utc_time = start_bj_time.astimezone(timezone.utc)
    end_utc_time = end_bj_time.astimezone(timezone.utc)
    # 将时间格式化为指定格式
    format_start_utc_time = start_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    format_end_utc_time = end_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    return format_start_utc_time, format_end_utc_time


class RegisterData:
    url = 'http://10.100.94.53:9093/api/v2/silences'
    headers = {'Content-Type': 'application/json; charset=utf-8'}


def set_silence(component_name, start_time, end_time):
    data = {
        "matchers": [
            {
                "name": "component",
                "value": component_name,
                "isRegex": False,
            }
        ],
        "startsAt": start_time,
        "endsAt": end_time,
        "createdBy": "JF_ADMIN",
        "comment": "计划内维护"
    }
    response = requests.post(RegisterData.url, headers=RegisterData.headers, data=json.dumps(data))
    print(response.status_code)

def job():
    job_name = '统一监控平台'
    start_min = 0
    end_min = 0
    excel_file = '2024年交付域名信息收集.xlsx'
    df = pd.read_excel(excel_file, sheet_name=3)
    for _, row in df.iterrows():
        print(row['项目名'])
        set_silence(row['项目名'], *time_change(row['静默开始时间'], start_min, row['静默结束时间'], end_min))



if __name__ == '__main__':
    
    

   
    schedule.every().day.at("09:39").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
