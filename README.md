# Stock Manager

This system consists of three systems.

## StockCrawler

Obtain stock information from naver and continous stock list. <br>
continuous stock list is a list that stock prices sequences from today to that keeping rising.<br>

## StockAnalyzer

Figure out what stock is right to vest. It calculates from stocks information that StockCrawler had put into db.

## Django webserver apps

### StockDBManager

RestfulAPI server for DB.<br>
Crawler and Analyzer push data using this.<br>
StockManagementServer also uses this.<br>
It uses session for authentication users.

### StockManagementServer

RestfulAPI server for letting users to control Crawler and Analzyer.
Users can make a schedule for Crawler using this and can analyze stock information.<br>

## AutoInvestor (Not yet)

Invest automactically itself without people.

## InvestmentManagementServer (Not yet)

Control the AutoInvestor using RestfulAPI.<br>
It's controlled by users who uses StockManagementClient.

## StockManagementClient

Interface for users to control all of the servers.
