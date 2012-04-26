AUTH_LOGIN_RESPONSE = {
   "EZMessage":{
      "data":{
         "lastName":"Doe",
         "funded":"true",
         "nasdaq":{
            "professional":"false",
            "agree":"true"
         },
         "authToken":"b7b426ef-8e20-46f1-bad6-1244f0b6de02",
         "nyse":{
            "professional":"false",
            "agree":"true"
         },
         "opera":{
            "professional":"false",
            "agree":"true"
         },
         "delayedQuotes":"true",
         "firstName":"John",
         "access":"granted",
         "requiresAccountCreation":"false",
         "professional":"false",
      },
      "action":"auth.login"
   }
}

KEEPALIVE_RESPONSE = {}

AUTH_LOGOUT_RESPONSE = {
   "EZMessage":{
      "action":"auth.logout",
      "data":{
         "authToken":"",
         "logout":"complete",
      }
   }
}

ACCOUNT_INFO_RESPONSE = {
   "EZMessage":{
      "data":{
         "account":[
            {
               "canChangeCommissionSchedule":"true",
               "accountId":"1711105",
               "nextCommissionSchedule":"COMMISSION_I",
               "isVirtual":"false",
               "riskMaxDollarsPerOrder":"1000000",
               "riskMaxSharesPerOrder":"50000.0",
               "accountDesc":"Roth IRA",
               "accountName":"Peak6, Corporate",
               "yearAccountOpened":"2007",
               "riskMaxContractsPerOrder":"4001.0",
               "optionsWarning":"false",
               "partnerCode":"OH",
               "accountType":"ROTH_IRA",
               "account":"77959070",
               "canAccountACH":"false",
               "accountTypeId":"5",
               "currentCommissionSchedule":"COMMISSION_I"
            },
            {
               "canChangeCommissionSchedule":"true",
               "accountId":"1761020",
               "nextCommissionSchedule":"COMMISSION_II",
               "isVirtual":"true",
               "riskMaxDollarsPerOrder":"1000000",
               "riskMaxSharesPerOrder":"50000.0",
               "accountDesc":"Individual",
               "accountName":"V_R1796",
               "yearAccountOpened":"2007",
               "riskMaxContractsPerOrder":"4001.0",
               "optionsWarning":"false",
               "accountType":"INDIVIDUAL",
               "account":"V_R1796",
               "accountTypeId":"0",
               "canAccountACH":"false",
               "currentCommissionSchedule":"COMMISSION_II"
            }
         ],
         "login":{
            "lastName":"Doe",
            "accountMode":"single",
            "rfqWarning":"false",
            "toolsWarning":"true",
            "loginCount":"151",
            "firstName":"John",
            "toolsWarningVersion":"4",
            "defaultSymbol":"IBM",
            "uiMode":"retail"
         },
         "inactivityTimeout":"60",
         "requiresAccountCreation":"false"
      },
      "action":"account.info"
   }
}

ACCOUNT_CASH_RESPONSE = {
   "EZMessage":{
      "data":{
         "marginEquity":"4241.02",
         "accountValueYearToDate":"-7233.10",
         "availableToWithdraw":"0.00",
         "accountValueMonthToDate":"-7233.10",
         "pendingOrders":"0.00",
         "accountValueDailyChange":"77.33",
         "dayTradingBuyPower":"0.00",
         "accountValue":"6212.02",
         "optionBuyingPower":"555.37",
         "stockBuyingPower":"1110.74",
         "cashBalance":"-1713.33",
         "availableToTrade":"-1713.33",
         "portfolioValue":"7925.35"
      },
      "action":"account.cash"
   }
}

VIEW_QUOTE_LIST_RESPONSE = {
   "EZMessage":{
      "action":"view.quote.list",
      "data":{
         "session":"open",
         "quote":[
            {
               "key":"MARKETSTATUS",
               "marketClosed":False
            },
            {
               "key":"IBM:::S",
               "symbol":"IBM",
               "bid":163.11000061035156,
               "ask":163.41000366210938,
               "isExchangeDelayed":False,
               "volume":3901100,
               "mark":163.260009765625,
               "dailyChange":-0.2599945068359375,
               "stockLast":163.3000030517578,
               "low":162.61000061035156,
               "high":163.60000610351562,
               "open":163.39999389648438,
               "extClose":"163.30",
               "extChangeAmount":"0.0",
               "extChangePercent":"0.0",
               "extChangeTime":"03:23 PM CST Feb 02 2011",
               "prevClose":163.55999755859375,
               "last":"163.30",
               "change":"-0.2599945",
               "changePercent":"-0.15895972",
               "bidSize":3,
               "askSize":1,
               "exchange":"NYSE",
               "hasDividends":True,
               "divConfirm":True,
               "divAmount":0.6499999761581421,
               "exDate":"Tue Feb 08 00:00:00 CST 2011",
               "hasEarnings":False,
               "earningsConfirm":False
            },
            {
               "key":"QQQQ:::S",
               "symbol":"QQQQ",
               "bid":56.939998626708984,
               "ask":56.959999084472656,
               "isExchangeDelayed":False,
               "volume":48649000,
               "mark":56.94999694824219,
               "dailyChange":-0.07999801635742188,
               "stockLast":56.970001220703125,
               "low":56.84000015258789,
               "high":57.16999816894531,
               "open":56.91999816894531,
               "extClose":"56.97",
               "extChangeAmount":"0.0",
               "extChangePercent":"0.0",
               "extChangeTime":"05:05 PM CST Feb 02 2011",
               "prevClose":57.04999923706055,
               "last":"56.97",
               "change":"-0.07999802",
               "changePercent":"-0.1402244",
               "bidSize":39,
               "askSize":145,
               "exchange":"NASDAQ",
               "hasDividends":False,
               "divConfirm":False,
               "hasEarnings":False,
               "earningsConfirm":False
               "avg10dayVolume":"3816541",
               "week52high":148.86,
               "peRatio":”13.5”,
               "dividendYield":"1.758",
               "dividendDate":"2010/11/08"
            },
            {
               "key":"EVEP:::S",
               "symbol":"EVEP",
               "isExchangeDelayed":False,
               "volume":320400,
               "mark":44.150001525878906,
               "dailyChange":-0.20000076293945312,
               "stockLast":44.130001068115234,
               "low":44.09000015258789,
               "high":44.9900016784668,
               "open":44.75,
               "last":"44.13",
               "change":"-0.20000076",
               "changePercent":"-0.45116344",
               "hasDividends":True,
               "divConfirm":True,
               "divAmount":0.7599999904632568,
               "exDate":"Thu Feb 03 00:00:00 CST 2011",
               "hasEarnings":False,
               "earningsConfirm":False
            }
         ]
      }
   }
}

VIEW_SERIES_RESPONSE = {
   "EZMessage":{
      "action":"view.series",
      "data":{
         "s":[
            {
               "e":"Jul 11",
               "k":[
                  "A:20110716:300000:C",
                  "A:20110716:300000:P",
                  "A:20110716:330000:C",
                  "A:20110716:330000:P",
                  "A:20110716:350000:C",
                  "A:20110716:350000:P",
                  "A:20110716:380000:C",
                  "A:20110716:380000:P",
                  "A:20110716:400000:C",
                  "A:20110716:400000:P",
                  "A:20110716:430000:C",
                  "A:20110716:430000:P",
                  "A:20110716:450000:C",
                  "A:20110716:450000:P",
                  "A:20110716:460000:C",
                  "A:20110716:460000:P",
                  "A:20110716:470000:C",
                  "A:20110716:470000:P",
                  "A:20110716:480000:C",
                  "A:20110716:480000:P",
                  "A:20110716:490000:C",
                  "A:20110716:490000:P",
                  "A:20110716:500000:C",
                  "A:20110716:500000:P",
                  "A:20110716:525000:C",
                  "A:20110716:525000:P",
                  "A:20110716:550000:C",
                  "A:20110716:550000:P",
                  "A:20110716:575000:C",
                  "A:20110716:575000:P",
                  "A:20110716:600000:C",
                  "A:20110716:600000:P",
                  "A:20110716:650000:C",
                  "A:20110716:650000:P",
                  "A:20110716:700000:C",
                  "A:20110716:700000:P",
                  "A:20110716:750000:C",
                  "A:20110716:750000:P"
               ]
            }
         ],
         "q":"51.01"
      }
   }
}

ACCOUNT_MARGIN_JSON_RESPONSE = {
   "EZMessage":{
      "action":"account.margin.json",
      "data":{
         "dayTradesActualPrior":"0",
         "patternDayTrader":"false",
         "noDatabaseRecord":"true",
         "dayTradesActualAfterOrder":"0",
         "marginChange":"-204.32",
         "orgSma":"555.37",
         "fudgeFactor":"0.00",
         "stockBuyingPower":"322.14",
         "optionBuyingPower":"161.07",
         "commission":[
            {
               "m_order_id":"1",
               "commission":"2.95",
               "fee":{
                  "CBOE":"0.00",
                  "PENNY_STOCK":"0.00",
                  "INDEX":"0.00",
                  "SEC":"0.02",
                  "OCC":"0.00",
                  "TAF":"0.01",
                  "DIRECTED_ORDER":"0.00"
               }
            }
         ]
      }
   }
}

ORDER_CREATE_JSON_RESPONSE = {
   "EZMessage":{
      "action":"order.create.json",
      "data":{
         "created":"true",
         "id":"152325619"
      }
   }
}

ORDER_MODIFY_JSON_RESPONSE = {
   "EZMessage":{
      "action":"order.modify.json",
      "data":{
         "modified":"true",
         "newId":"152325620"
      }
   }
}

ORDER_CANCEL_JSON_RESPONSE = {
   "EZMessage":{
      "action":"order.cancel.json",
      "data":{
         "canceled":"true",
         "id":"152325620"
      }
   }
}

MASTER_ACCOUNT_ORDERS_RESPONSE = {
   "EZMessage":{
      "action":"master.account.orders",
      "data":{
         "timestamp":"2011-02-01  12:00:32.460107",
         "response_type":"json",
         "master_account_orders":{
            "page":0,
            "page_size":30,
            "total_records":23,
            "records":[
               {
                  "order_id":29638848,
                  "message":"Click for  details",
                  "time_in_force":"day",
                  "quantity":5,
                  "fill_quantity":"",
                  "transaction":"Buy To  Open",
                  "short_description":"IBM Stock",
                  "long_description":"IBM  Stock",
                  "status":"Canceled",
                  "date_created_ms":1296537096000,
                  "last_updated_ms":1296537106000,
                  "date_created":"2011-01-31 23:11:36",
                  "last_updated":"2011-01-31  23:11:46",
                  "master_order_id":152325506,
                  "order_type":"regular",
                  "price_type":"limit",
                  "price":161,
                  "trigger_or der":False,
                  "trailing_stop_order":False,
                  "complex_order":False,
                  "modifiable":False,
                  "root_order_id":152325506,
                  "is_spread_order":False,
                  "is_mutual_fund_order":False,
                  "underlying_stock_symbol":"IBM",
                  "timestamp":"2011-0 2-01 12:00:32",
                  "has_expired_keys":False,
                  "security_keys":"IBM:::S"
               }
            ]
         }
      }
   }
}

ACCOUNT_POSITIONS_RESPONSE = {
   "EZMessage":{
      "data":{
         "unified":[
            {
               "accountId":"1761020",
               "shareCostBasis":"3.6",
               "isCustomCostBasis":"false ",
               "expString":"Jul 11",
               "stock":"47.98",
               "description":"BP Jul 11 46.00  Call",
               "defaultCostBasis":"720",
               "isExchangeDelayed":"false",
               "underlying":"BP",
               "spc":"100",
               "bid":"4.0",
               "securityKey":"BP:20110716:460000:C",
               "qty":"2",
               "dailyChange":"0.03",
               "multiplier":"100.0",
               "gain":"90",
               "sortHint":[
                  "BP201107160000460000C",
                  "BP201107160000460000C"
               ],
               "mktVal":"810",
               "posValChange":"5",
               "price":"4.05",
               "st rikeString":"46.00",
               "canExercise":"true",
               "costBasis":"720",
               "positionNewToday":"false",
               "ask":"4.1"
            }
         ],
         "timeStamp":"1296583232029"
      },
      "action":"account.positions"
   }
}

ACCOUNT_ACTIVITY_RESPONSE = {
   "EZMessage":{
      "data":{
         "total":"2",
         "timeStamp":"1296583401513",
         "activity":[
            {
               "activityDateStr":"2011/01/31 ",
               "price":"162.0",
               "accountId":"1761020",
               "symbol":"IBM",
               "transaction":"BTO",
               "description":"IBM  Stock",
               "qty":"5.0",
               "netAmount":"-810.00"
            },
            {
               "activityDateStr":"2011/01/10",
               "com":"8.8",
               "price":"3.6",
               "acco untId":"1761020",
               "symbol":"BP",
               "transaction":"BTO",
               "description":"BP Jul 11 46.00  Call",
               "qty":"2.0",
               "netAmount":"-728.80"
            }
         ]
      },
      "action":"account.activity"
   }
}

