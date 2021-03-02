## API NbtExchangeRate

Get Exchange Rates of National Bank of Tajikistan

<br/>

#### Authentication
No authorize option

#### HTTP Request

`GET /`

#### Query Parameters
None

#### Success Response

```json
{
  "date": "20210223",
  "usd": "11.3035",
  "eur": "13.7179",
  "rub": "0.1506"
}
```
    
#### Response parameters
Parameter | Type | Description 
:---------- | ----- | ------------
date | date YYYYMMDD | date of exchange rate
usd | string | exchange rate 1 dollar to somoni
eur | string | exchange rate 1 ruble to somoni
rub | string | exchange rate 1 euro to somoni
 
 
#### Error Response

```json
{
  "error_code": 0,
  "error_message": "string" 
}
```

#### Error Codes

 http code | error code | error message 
---------- | ----- | ------------
404 | 5000 | Data not found
400 | 5001 | Bad request
