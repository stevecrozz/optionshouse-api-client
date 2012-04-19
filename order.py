"""
price_type [limit,market]
time_in_force [day,good_till_cancel]
order_subtype [single,spread]
"""
class Order(object):
    def __init__(self, **kwargs):
        order = {}
        order['m_order_id'] = 1
        order['price_type'] = kwargs['price_type']
        order['time_in_force'] = kwargs['time_in_force']
        order['price'] = kwargs['price']
        order['underlying_stock_symbol'] = kwargs['underlying_stock_symbol']
        order['source'] = 'API'
        order['client_id'] = kwargs['client_id']
        order['preferred_destination'] = 'BEST'
        order['allOrNone'] = kwargs['allOrNone']
        order['order_subtype'] = kwargs['order_subtype']
        order['order_type'] = 'regular'
        order['legs'] = kwargs['legs']

        self.data = order

    def toJson(self):
        return json.dumps(self.toDict())

    def toDict(self):
        dict_legs = []
        for leg in self.data['legs']:
            leg = leg.toDict()
            leg['index'] = len(dict_legs)
            dict_legs.append(leg)

        order = self.data
        order['legs'] = dict_legs

        return order

class OrderLeg(object):
    def __init__(self, **kwargs):
        leg = {}

        if kwargs['key'].find(":") == -1:
            leg['key'] = "%s:::S" % kwargs['key']
        else:
            leg['key'] = kwargs['key']

        leg['side'] = kwargs['side']
        leg['security_type'] = kwargs['security_type']
        leg['quantity'] = kwargs['quantity']
        leg['multiplier'] = kwargs['multiplier']
        leg['position_type'] = kwargs['position_type']

        self.data = leg

    def toJson(self):
        return json.dumps(self.toDict())

    def toDict(self):
        return self.data

