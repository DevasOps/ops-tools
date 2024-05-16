#!/usr/bin/env python3


# import pandas as pd
import pymysql
import whois
from datetime import datetime


class GlobalData:
    csv_file = "2024年交付域名信息收集.csv"
    mysql_host = '127.0.0.1'
    mysql_port = 53306
    mysql_user = 'root'
    mysql_password = 'jf_Domain@2024'
    mysql_db = 'jf_domain_check'


##数据处理
# def operatedb(area, domain, system_name, main_domain, sre):
#     mysql_connect = pymysql.connect(host=GlobalData.mysql_host, port=GlobalData.mysql_port, user=GlobalData.mysql_user,
#                                     password=GlobalData.mysql_password, db=GlobalData.mysql_db)
#     exit_sql = 'SELECT id FROM domains where system_name = %s'
#     insert_sql = 'insert into domains (area, domain, system_name, main_domain, sre) VALUES (%s, %s, %s, %s, %s)'
#     update_sql = 'update domains set area=%s, domain=%s,main_domain=%s,sre=%s where system_name=%s'
#
#     try:
#         mysql_cursor = mysql_connect.cursor()
#         mysql_cursor.execute(exit_sql, system_name)
#         system_exit = mysql_cursor.fetchone()
#
#         if system_exit is None:
#             print('开始新建' + '[' + system_name + ']' + '信息')
#             mysql_cursor.execute(insert_sql, (area, domain, system_name, main_domain, sre))
#         else:
#             print('开始更新' + '[' + system_name + ']' + '信息')
#             mysql_cursor.execute(update_sql, (area, domain, main_domain, sre, system_name))
#         mysql_connect.commit()
#         mysql_connect.close()
#     except Exception as e:
#         print(e)
#
#
# def save2db():
#     df = pd.read_csv(GlobalData.csv_file, encoding='gbk')
#     # data_to_write = pd.DataFrame(columns=['区域', '项目名', '域名'])
#     for index, row in df.iterrows():
#         if pd.notnull(row['区域']) and pd.notnull(row['项目名']):
#             area = row['区域']
#             system_name = row['项目名']
#             domain = row['域名']
#             main_domain = domain.split("/")[2]
#             sre = row['运维人员']
#             operatedb(area, domain, system_name, main_domain, sre)


# 更新剩余可用天数
def update_remain_days():
    mysql_connect = pymysql.connect(host=GlobalData.mysql_host, port=GlobalData.mysql_port, user=GlobalData.mysql_user,
                                    password=GlobalData.mysql_password, db=GlobalData.mysql_db)
    main_domain_sql = 'SELECT main_domain, system_name FROM domains'
    get_remain_days_sql = 'update domains set  remain_days= %s where system_name = %s '

    mysql_cursor = mysql_connect.cursor()
    mysql_cursor.execute(main_domain_sql)
    for (main_domain, system_name) in mysql_cursor.fetchall():
        print(str(main_domain))
        # 排除gov、edu特殊域名
        if str(main_domain).endswith('.edu.cn') or str(main_domain).endswith('.gov.cn'):
            print('政府域名 [' + system_name + '] 默认配置')
            remaining_days = 9999
        else:
            print('查询更新 [' + system_name + '] 信息')
            remaining_days = whois_query(main_domain)
        mysql_cursor.execute(get_remain_days_sql, (remaining_days, system_name))
    mysql_connect.commit()
    mysql_connect.close()


# 更新第一次异常的数据
def update_remain_days_again():
    mysql_connect = pymysql.connect(host=GlobalData.mysql_host, port=GlobalData.mysql_port, user=GlobalData.mysql_user,
                                    password=GlobalData.mysql_password, db=GlobalData.mysql_db)
    main_domain_sql = 'SELECT main_domain, system_name FROM domains where remain_days is NULL'
    get_remain_days_sql = 'update domains set  remain_days= %s where system_name = %s '

    mysql_cursor = mysql_connect.cursor()
    mysql_cursor.execute(main_domain_sql)
    for (main_domain, system_name) in mysql_cursor.fetchall():
        print(str(main_domain))
        if str(main_domain).endswith('.edu.cn') or str(main_domain).endswith('.gov.cn'):
            print('政府域名 [' + system_name + '] 默认配置')
            remaining_days = 9999
        else:
            print('查询更新 [' + system_name + '] 信息')
            remaining_days = whois_query(main_domain)
        mysql_cursor.execute(get_remain_days_sql, (remaining_days, system_name))
    mysql_connect.commit()
    mysql_connect.close()


# whois查询
def whois_query(main_domain):
    try:
        w = whois.whois(main_domain)
        # 获取域名到期日期
        expiration_date = w.expiration_date
        if type(expiration_date) is list:
            expiration_date = expiration_date[0]
        if expiration_date:
            if isinstance(expiration_date, str):
                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S')
        # 计算剩余可用天数
        remaining_days = (expiration_date - datetime.now()).days
        if type(remaining_days) == int:
            return remaining_days
    except Exception as e:
        print(e)


if __name__ == '__main__':
    #update_remain_days()
    #update_remain_days_again()
    update_remain_days_again()

