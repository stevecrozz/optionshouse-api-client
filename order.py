import time

class Order(object):
    """
    The Order object is used to preivew, create and modify orders.
    """

    # These are all the possible statuses an Order can have
    STATUSES = [
        "Pending",
        "Open",
        "Expired",
        "Exercised",
        "Canceled",
        "Cancel_Pending",
        "Partial_Cancel_Pending",
        "Filled",
        "Rejected",
        "Partial_Cancel",
        "Partially_Filled",
    ]

    def __init__(self, **kwargs):
        """
        The following keyword arguments are required:
        price_type: 'limit' or 'market'
        time_in_force: for limit orders 'day' or 'good_till_cancel'
        price: string representing order price for limit orders or current
            market price for market orders
        underlying_stock_symbol: ticker symbol for the underlying stock
        legs: list of Leg objects

        You may optionally provide the boolean allOrNone keyword argument which
        defaults to false.
        """

        self.data = {
            'm_order_id': 1,
            'price_type': kwargs['price_type'],
            'time_in_force': kwargs['time_in_force'],
            'price': kwargs['price'],
            'underlying_stock_symbol': kwargs['underlying_stock_symbol'],
            'source': 'API',
            'client_id': int(time.time() * 1000),
            'preferred_destination': 'BEST',
            'allOrNone': kwargs['allOrNone'],
            'order_type': 'regular',
            'legs': kwargs['legs'],
        }

        if len(kwargs['legs']) == 1:
            self.data['order_subtype'] = 'regular'
        elif len(kwargs['legs']) > 1:
            self.data['order_subtype'] = 'spread'

    def modify(self, order_id):
        """
        Transform this Order instance into an order modificaation. You must
        provide the order_id so optionshouse knows which order to modify.
        """
        self.data['modify_order'] = True
        self.data['order_id'] = order_id

    def toJson(self):
        """
        Generate a JSON string from this Order instance
        """
        return json.dumps(self.toDict())

    def toDict(self):
        """
        Generate a python dictionary from this Order instance
        """
        dict_legs = []
        for leg in self.data['legs']:
            leg = leg.toDict()
            leg['index'] = len(dict_legs)
            dict_legs.append(leg)

        order = self.data.copy()
        order['legs'] = dict_legs

        return order

class OrderLeg(object):
    """
    All Order objects must contain a list of OrderLeg objects that define the
    structure of the order.
    """

    def __init__(self, **kwargs):
        """
        The following arguments are required:
        side: 'buy' or 'sell'
        security_type: 'stock' or 'option'
        quantity: Integer
        key: String describing the security
        multiplier: Integer - use 1 for stocks, for options get the value from
            options_list
        position_type: 'opening' or 'closing'
        """

        self.data = {
            'side': kwargs['side'],
            'security_type': kwargs['security_type'],
            'quantity': kwargs['quantity'],
            'multiplier': kwargs['multiplier'],
            'position_type': kwargs['position_type'],
        }

        if kwargs['key'].find(":") == -1:
            self.data['key'] = "%s:::S" % kwargs['key']
        else:
            self.data['key'] = kwargs['key']

    def toJson(self):
        """
        Transform this OrderLeg object into a JSON string
        """

        return json.dumps(self.toDict())

    def toDict(self):
        """
        Transform this OrderLeg object into a python dictionary
        """

        return self.data

