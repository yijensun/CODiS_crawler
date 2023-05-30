# CODiS_crawler
中央氣象局觀測資料查詢系統 (CWB Observation Date Inquire System, CODiS) 資料下載工具<br>
Web crawler tool for [CWB Observation Date Inquire System (CODiS)](https://e-service.cwb.gov.tw/HistoryDataQuery/).

# Installation
Clone `CODiS_crawler` from this repository.
```bash
git clone https://github.com/yijensun/CODiS_crawler
```

# Crawling CODiS data into CSV
## Assign stations and years
`CODiS_crawler` supports download data from single station/year and multiple stations/years.
```python
# To crawl single station and year
years = [2023]
stations = ['467610'] #成功 

# To crawl multiple stations and years
years = [2003, 2005, 2014]
stations = ['C0X080', 'C0O900', '467410'] #佳里, 善化, 臺南 
```
## Crawl data into CSV
Here is the demonstration of downloading monthly data from a single station. To download yearly or daily data, change the attribute `data_type` to 'year' or 'day'.
```python
import os
from CODiS_crawler.CODiS_crawler import CODiS_crawler

# Change current working directory to desired path
path = '/content'
os.chdir(path)

# To download monthly data
run = CODiS_crawler(stations, data_type = 'month', year_list = years)
```
## Check period without data in each station
The folder structure of the downloaded CSV:

     data/
       |-------- station id/
                     |
                     | ----- year/
                     | ----- month/
                     | ----- day/
                     
In the folder of each station contains folders for each data type.
Each data type folder contains a text file named `no_data.txt` that contains the periods when the data is absent.

<div>
   <a href="https://colab.research.google.com/drive/1iH8FdF3JS2wzl3mwjKcS1TegipWaUYFn?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
</div>

# Declaration
The source code of this tool is revised from [s3131212/CWB-Observation-Crawler](https://github.com/s3131212/CWB-Observation-Crawler) released by [TienYang](https://github.com/wy36101299) and [Allen Chou](https://github.com/s3131212). The original repository is out of maintenance and due to CODiS has updated its format, the repo cannot compile anymore. [Yi-Jen Sun](https://github.com/yijensun) revised from it and released this tool.

# Bugs report and suggestions 
If you encounter any bug or issue, please contact Yi-Jen Sun via elainesun442@gmail.com. Suggestions are also appreciated!
