# Task 2: 🐳 Extract and Save Data of Exchange Rates 

Author: **Liubomyr Mokrytskyi**

## 📝 What does this code?

_Here is a source code of program that get the exchange rates for currencies from [NBU](https://bank.gov.ua/ua/open-data/api-dev) cite, transform them a bit and save to the [Google SpreadSheet](https://docs.google.com/spreadsheets/d/12gAzrX5oiCU1mtb0c2_uWjBFDOuboDA8ePThSbJupeY/edit?gid=0#gid=0)._

In the end, we should get:

- [README.md](README.md) - README file that contains documentation and results(this file actually heh)
- [main.py](main.py) - Python file for the program
- exchangerates-435618-45bc1dde0500.json - json file with credentials (if you want to run the code, you will need to generate your own)
- Screenshots with the results


## 🏃‍♂️ How to use/run)

As code is hosted in pythonanywhere.com the steps are pretty simple:

- Authorise with default user:
  - default user - <u>user</u>; 
  - default password - <u>password</u>.

- Use one of the written endpoints:
  - Sever URL - https://liubmok.pythonanywhere.com
   - '/get-currency-exchange-rate' - more for test to see whether we extract the correct data from NBU cite;
   - '/update-excel-exchange-rate' - to update the [Google SpreadSheet](https://docs.google.com/spreadsheets/d/12gAzrX5oiCU1mtb0c2_uWjBFDOuboDA8ePThSbJupeY/edit?gid=0#gid=0);

But also in the task description we had the requirement that we should have an ability to choose for which dates we want to update the data in SpreadSheet. So here are parameters that you can fill in the url:

### Parameters
{base_url} - url of the exact endpoint you want to use (server url + endpoint)<br>
&nbsp;&nbsp;&nbsp;&nbsp;?<u>update_from=</u> - the starting date from which we get the data (date format - 'yyyy-mm-dd, default - today's date) <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&<u>update_to=</u> - the end date by which we get the data (date format - 'yyyy-mm-dd, default - today's date) <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&<u>valcode=</u> - valcode of the currency for which you want to see the exchange rate (default - 'usd')(I added this as an additional option, as it may be needed in the future)

Several examples:
- {base_url}/get-currency-exchange-rate?update_from=2024-09-01&update_to=2024-09-14&valcode=usd
- {base_url}/update-excel-exchange-rate?update_from=2024-09-01&update_to=2024-09-14
- {base_url}/get-currency-exchange-rate?update_from=2024-09-01

## 🎀  Results

🔻 Screenshots of🔻
#### Requests

- get jsonfied dates and exchange rates for period 2024-09-01 - 2024-09-14 (September)
<br>[URL]( https://liubmok.pythonanywhere.com/get-currency-exchange-rate?update_from=2024-09-01&update_to=2024-09-14&valcode=usd)
![get_usd_exchange_rates.png](Screenshots%2Fget_usd_exchange_rates.png)
- update dates and exchange rates in [Google SpreadSheet](https://docs.google.com/spreadsheets/d/12gAzrX5oiCU1mtb0c2_uWjBFDOuboDA8ePThSbJupeY/edit?gid=0#gid=0) for period 2024-09-01 - 2024-09-14 (September)
<br> [URL](https://liubmok.pythonanywhere.com/update-excel-exchange-rate?update_from=2024-09-01&update_to=2024-09-14&valcode=usd)
![update_spreadsheet.png](Screenshots%2Fupdate_spreadsheet.png)
![updated_spreadsheet.png](Screenshots%2Fupdated_spreadsheet.png)

#### Error Handling
- wrong date format (14-09-2024 instead of 2024-09-14) :
[URL](https://liubmok.pythonanywhere.com/update-excel-exchange-rate?update_from=2024-09-01&update_to=14-09-2024&valcode=usd)
![wrong_date_format.png](Screenshots%2Fwrong_date_format.png)
- a future date (today is 2024-09-14 but user want to see data for 2024-09-15) :
[URL](https://liubmok.pythonanywhere.com/update-excel-exchange-rate?update_from=2024-09-01&update_to=2024-09-15&valcode=usd)
![future_date.png](Screenshots%2Ffuture_date.png)
- wrong order of dates (2024-09-14 should be after 2024-09-01):
[URL](https://liubmok.pythonanywhere.com/update-excel-exchange-rate?update_from=2024-09-14&update_to=2024-09-01&valcode=usd)
![wrong_order.png](Screenshots%2Fwrong_order.png)