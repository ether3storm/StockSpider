# StockSpider

Get stock price data in China A-share market.

## File Description

main.py: main program for getting data

spider.py: functions used in the process

stats.ipynb: some simple examples for using the data

data/: folder for saving the data

stockcode.csv: generated by spider.py, recording existed stock code

## Usage

python main.py directly or with parameters

-u: updating existed stock code list

-g: downloading all historical price data

-t TIME: updating price data everyday at the time specified
