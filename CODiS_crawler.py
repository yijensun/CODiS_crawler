import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

class CODiS_crawler:
  def __init__(self, stations, data_type = 'month', year_list = None):
    station_info = self.crawler('https://e-service.cwb.gov.tw/wdps/obs/state.htm', crwl_title = ['站號', '新站號'], crwl_intvl = [1,-1])

    for station in stations:
      temp = station_info.loc[station_info['站號'] == station]
      if(temp.empty):
        print('Station '+station+' do not exist.')
        continue
      print('Processing station '+station+'...')
      id = temp.iloc[0,0]
      alt = temp.iloc[0,3]

      if np.floor(float(alt)) == float(alt):
        alt = str(int(float(alt)))

      path = './data/'+id+'/'+data_type
      if os.path.exists(path) == 0:
        os.makedirs(path)
      
      up_list = self.url_path_list(id, alt, data_type, year_list)
      for up in up_list:
        _ = self.crawler(up[0], crwl_title = ['ObsTime', 'Cloud Amount'], crwl_intvl = [4, None], csv_path = up[1])

  def url_path_list(self, id, alt, data_type, year_list):
    up_list = []

    for year in year_list:
      date = datetime.datetime(year,1,1)
      while date.year == year:
        if data_type == 'year':
          url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/YearDataController.do?command=viewMain&station='+id+'&stname=%25E5%25B9%25B3%25E7%25AD%2589&datepicker='+str(date.year)+'&altitude='+alt+'m'
          path = "./data/"+id+'/'+data_type+'/'+str(date.year)+".csv"
          up_list.append([url, path])
          date += relativedelta(year=1)
          
        if data_type == 'month':
          url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station='+id+'&stname=%25E4%25BA%2594%25E7%25B5%2590&datepicker='+str(date.year)+'-'+str(date.month).zfill(2)+'&altitude='+alt+'m'
          path = "./data/"+id+'/'+data_type+'/'+str(date.year)+'-'+str(date.month).zfill(2)+".csv"
          up_list.append([url, path])
          date += relativedelta(months=1)

        if data_type == 'day':
          url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station='+id+'&stname=%25E5%25B9%25B3%25E7%25AD%2589&datepicker='+str(date.year)+'-'+str(date.month).zfill(2)+'-'+str(date.day).zfill(2)+'&altitude='+alt+'m'
          path = "./data/"+id+'/'+data_type+'/'+str(date.year)+'-'+str(date.month).zfill(2)+'-'+str(date.day).zfill(2)+".csv"
          up_list.append([url, path])
          date += datetime.timedelta(days=1)

    return up_list

  def crawler(self, url, crwl_title = [], crwl_intvl = None, csv_path = None):
    # access
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')

    # find no data page
    error = soup.find("label", class_="imp")
    if error:
      if error.string == '本段時間區間內無觀測資料。':
        idx = [pos for pos, char in enumerate(csv_path) if char == '/']
        path = csv_path[:idx[-1]]
        with open (path+'/nodata.txt','a') as f:
          f.write(csv_path[idx[-1]+1:-4]+'\n')
        return
    
    # title
    titles = soup.find_all("th")
    strtitle=[]
    for title in titles:
      title = title.contents[0] 
      strtitle.append(title)
    str_idx = strtitle.index(crwl_title[0])
    end_idx = strtitle.index(crwl_title[1])
    strtitle = strtitle[str_idx:end_idx+1]
    
    # parameters
    form =[]
    tmps = soup.find_all("tr")
    for tmp in tmps[crwl_intvl[0]:crwl_intvl[1]]:
      tmp = tmp.find_all("td")
      parameter =[]
      for strtmp in tmp:
        if strtmp.string is None:
          parameter.append(strtmp.string)
        else:
          parameter.append(strtmp.string.replace(u'\xa0', u''))
      form.append(parameter)
    form = pd.DataFrame(form, columns=strtitle)

    # save csv
    if csv_path:
      form.to_csv(csv_path, encoding ="utf-8", index = False)
    
    return form