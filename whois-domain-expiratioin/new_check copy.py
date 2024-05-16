
import pandas as pd
import pymysql
import whois
from datetime import datetime
import os
import chardet


class GlobalData:
    excel_file = "2024年交付域名信息收集.xlsx"
    mysql_host = '127.0.0.1'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = '123456'
    mysql_db = 'jf_domain_check'

def create_domains_table(mysql_connect):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS domains (
        id INT AUTO_INCREMENT PRIMARY KEY,
        area VARCHAR(255),
        domain VARCHAR(255),
        system_name VARCHAR(255),
        main_domain VARCHAR(255),
        sre VARCHAR(255)
    )
    '''
    mysql_cursor = mysql_connect.cursor()
    mysql_cursor.execute(create_table_sql)


#数据处理
def operatedb(area, domain, system_name, main_domain, sre):
    mysql_connect = pymysql.connect(host=GlobalData.mysql_host, port=GlobalData.mysql_port, user=GlobalData.mysql_user,
                                    password=GlobalData.mysql_password, db=GlobalData.mysql_db)
    create_domains_table(mysql_connect)
    exit_sql = 'SELECT id FROM domains where system_name = %s'
    insert_sql = 'insert into domains (area, domain, system_name, main_domain, sre) VALUES (%s, %s, %s, %s, %s)'
    update_sql = 'update domains set area=%s, domain=%s,main_domain=%s,sre=%s where system_name=%s'

    try:
        mysql_cursor = mysql_connect.cursor()
        mysql_cursor.execute(exit_sql, system_name)
        system_exit = mysql_cursor.fetchone()

        if system_exit is None:
            print('开始新建' + '[' + system_name + ']' + '信息')
            mysql_cursor.execute(insert_sql, (area, domain, system_name, main_domain, sre))
        else:
            print('开始更新' + '[' + system_name + ']' + '信息')
            mysql_cursor.execute(update_sql, (area, domain, main_domain, sre, system_name))
        mysql_connect.commit()
        mysql_connect.close()
    except Exception as e:
        print(e)


def save2db():


    try:
        excel_data = pd.ExcelFile(GlobalData.excel_file)
    except FileNotFoundError:
        print(f"file not find")
    except UnicodeDecodeError as e:
        print(f"encoding error")    
    for sheet_name in excel_data.sheet_names:
      df = excel_data.parse(sheet_name)
      for index, row in df.iterrows():
          if pd.notnull(row['区域']) and pd.notnull(row['项目名']):
              area = row['区域']
              system_name = row['项目名']
              domain = row['域名']
              main_domain = domain.split("/")[2]
              sre = row['运维人员']
              operatedb(area, domain, system_name, main_domain, sre)
    excel_data.close()



save2db()
