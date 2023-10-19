# Prgram 명: Cracks for Sentimentals
# Author: jimmy Kang
# Mail: jarvisNim@gmail.com
# 뉴스부문에서 센티멘탈지수에 이상변화를 감지하는  목적

# History
# 20220816  Create
# 20220901  Naver Trend 추가
# 20220903  Google Trend 추가

import sys, os

utils_dir = os.getcwd() + '/pyminerva/Utils'
reports_dir = os.getcwd() + '/pyminerva/Reports'
sys.path.append(utils_dir)

from settings import *
from naverApi import *
from pytrends.request import TrendReq
import plotly.express as px
import json
import requests
from bs4 import BeautifulSoup as bs


###################################################################################################
# 모니터링 테이블 (Sent_Crack) 생성
###################################################################################################
# Connect DataBase
database = 'Crack_Sent.db'
engine = 'sqlite:///' + database
conn = create_connection(database)

# 감성부문 Crack 집계 모니터링
def create_Sent_Crack(conn):
    with conn:
        cur=conn.cursor()
        cur.execute('create table if not exists Sent_Crack (Date text primary key, Tot_Percent real, \
            Tot_Count integer, CRSNT0001 integer, CRSNT0002 integer, CRSNT0003 integer, CRSNT0004 integer, \
            CRSNT0005 integer, CRSNT0006 integer, CRSNT0007 integer, CRSNT0008 integer, CRSNT0009 integer, \
            CRSNT0010 integer)')

    return conn

create_Sent_Crack(conn)
M_table = 'Sent_Crack'
M_query = f"SELECT * from {M_table}"
try:
    # 오늘자 Dataframe, db는 테이블에 있는 Dataframe 읽어온거.
    M_db = pd.read_sql_query(M_query, conn)
    buf = [today, 0,0,0,0,0,0,0,0,0,0,0,0]
    _M_db = pd.DataFrame(data=[buf], columns=M_db.columns)
    # display(M_db[-5:])
    logs = open(reports_dir+"/log_sentiments.txt", 'w')
    logs.write(M_db[-5:])
    logs.close()
except Exception as e:
    print('Exception: {}'.format(e))


###################################################################################################
def news_sp500_corr():
    """
    1. 뉴스 인덱스와 S&P500 correlation 선행지수: CRSNT0001
    https://fredblog.stlouisfed.org/2020/01/have-you-heard-the-news-news-affects-markets/?utm_source=series_page&utm_medium=related_content&utm_term=related_resources&utm_campaign=fredblog

    """
    sp500 = fred.get_series(series_id='SP500', observation_start=from_date_LT)
    news = fred.get_series(series_id='STLENI', observation_start=from_date_LT)
    # display(news[-4:])

    fig, ax1 = plt.subplots(figsize=(15,5))
    ax1.plot(sp500, color='green', label='S&P 500')
    ax2 = ax1.twinx()
    ax2.plot(news, color='blue', label='News')
    plt.title(f"News vs SP500 Earning Correlation", fontdict={'fontsize':20, 'color':'g'})
    ax1.grid()
    ax1.legend(loc=1)
    ax2.legend(loc=2)
    # plt.show()
    plt.savefig("./pyminerva/Reports/sentiments_001.png")


###################################################################################################
def naver_trend_search():
    """
    2. Naver trend search: CRSNT0002
    https://wooiljeong.github.io/python/pynaver/
    https://wooiljeong.github.io/python/naver_datalab_open_api/

    """
    # from naverApi import *
    from datetime import date
    from dateutil.relativedelta import relativedelta
    from volatility_calculations import calculate_historical_vols

    # # 지금은 가격이 아닌 일자별 검색량을 근거로 향후 트렌드를 예측하는 것이지만,
    # # 이것을 가격 데이터를 넣으면....
    keyword_group_set = {
        'keyword_group_1': {'groupName': "1.STOCK", 'keywords': ["삼성전자","주가","코스피", "KOSPI"]},
        'keyword_group_2': {'groupName': "2.BOND", 'keywords': ["국공채","채권","국채", "10년물", "BOND"]},
        'keyword_group_3': {'groupName': "3.REAL ASSET", 'keywords': ["아파트","빌라","다세대"]},
        'keyword_group_4': {'groupName': "4.INFLATION", 'keywords': ["물가","인플레이션","휘발유"]},
        'keyword_group_5': {'groupName': "5.INVERSE", 'keywords': ["인버스","곱버스","하락베팅"]},
    }

    client_id = "FgRmyTtNtW_fX8vNKC3F"
    client_secret = "1p6jC1WBe5"

    from_date= str(date.today() - relativedelta(years = 1))
    to_date= today
    time_unit='date'
    device=''
    ages=[]
    gender=''

    naver = NaverDLabApi(client_id = client_id, client_secret = client_secret)
    naver.add_keyword_groups(keyword_group_set['keyword_group_1'])
    naver.add_keyword_groups(keyword_group_set['keyword_group_2'])
    naver.add_keyword_groups(keyword_group_set['keyword_group_3'])
    naver.add_keyword_groups(keyword_group_set['keyword_group_4'])
    naver.add_keyword_groups(keyword_group_set['keyword_group_5'])
    df = naver.get_data(from_date, to_date, time_unit, device, ages, gender)
    display(df[-121::30])
    fig_1 = naver.plot_daily_trend()



###################################################################################################
if __name__ == "__main__":
    print('batch test...')
    news_sp500_corr()
    naver_trend_search