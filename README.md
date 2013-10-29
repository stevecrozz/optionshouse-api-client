# optionshouse-api-client
optionshouse-api-client is a simple python wrapper around the optionshouse
trading platform API. The goal of this project is to provide a working, but
minimal, non-magic interface to the API.
[http://lithostech.com/2012/09/automated-trading-via-optionshouse-api/](http://lithostech.com/2012/09/automated-trading-via-optionshouse-api/ "lithostech.com")

Disclaimer:
This API client has some test coverage, and it has seen some real-world
use. That said, you should do your own research and testing before
running any of this on your own. If you use this software, you must
assume all responsibility for your actions and the actions of this
software package.

## Basic Example Session
```python
from session import Session
s = Session('myusername', 'mypassword')
s.open()
s.quote('GS')
s.close()
```

## Placing a Simple Order
```python
s = Session('myusername', 'mypassword')
s.open()
order = Order(
  price_type='limit',
  time_in_force='good_till_cancel',
  price='72.50',
  underlying_stock_symbol='COP',
  legs=[
    OrderLeg(
        side='buy',
        security_type='stock',
        quantity=50,
        key='COP:::S',
        multiplier=1,
        position_type='opening',
    )
  ]
)
```

## Just supply your account id and your order object
```python
s.preview_order(12345, order)
```

## Looks good? Go ahead and place it
```python
s.place_order(12345, order)
s.close()
```

## Responses
All of the API requests have structured responses which vary. Take a look in
the tests folder for some examples.

## Supported API Methods
This API client supports all the documented optionshouse API actions. Each one is available as a method on instances of Session:

* account_activity
* account_cash
* account_info
* account_positions
* cancel_order
* close
* issue_request
* keepalive
* list_orders
* modify_order
* open
* options_list
* parse_response
* place_order
* preview_order
* quote

## Custom OptionsHouse API Solutions
If you're looking for an [Optionshouse API developer](http://www.brandedcrate.com/optionshouse-api-developer/),
or support for your API project, you can find me over at [Branded Crate](http://www.brandedcrate.com).
