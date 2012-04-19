from order import Order, OrderLeg
import unittest

class TestOrderLeg(unittest.TestCase):

    def test_proper_order_leg(self):
        leg = OrderLeg(
            side='buy',
            security_type='stock',
            quantity=10,
            key='COP:::S',
            multiplier=1,
            position_type='opening'
        )

        self.assertEqual(leg.data, {
            'side': 'buy',
            'security_type': 'stock',
            'quantity': 10,
            'key': 'COP:::S',
            'multiplier': 1,
            'position_type': 'opening',
        })

    def test_simple_keys(self):
        leg = OrderLeg(
            side='buy',
            security_type='stock',
            quantity=10,
            key='COP',
            multiplier=1,
            position_type='opening'
        )

        self.assertEqual(leg.data, {
            'side': 'buy',
            'security_type': 'stock',
            'quantity': 10,
            'key': 'COP:::S',
            'multiplier': 1,
            'position_type': 'opening',
        })


class TestOrder(unittest.TestCase):

    def test_proper_order(self):

        class FakeLeg(object):
            def __init__(self):
                self.index = None

            def toDict(self):
                return {'phony': 'leg'}

        legs = [FakeLeg(), FakeLeg(), FakeLeg()]

        order = Order(
            price_type='limit',
            time_in_force='good_till_cancel',
            price='72.50',
            underlying_stock_symbol='COP',
            client_id='someuniqueidentifier',
            legs=legs,
            allOrNone=False,
            order_subtype='single',
        )

        self.assertEqual(order.data, {
            'm_order_id': 1,
            'price_type': 'limit',
            'time_in_force': 'good_till_cancel',
            'price': '72.50',
            'underlying_stock_symbol': 'COP',
            'source': 'API',
            'client_id': 'someuniqueidentifier',
            'preferred_destination': 'BEST',
            'legs': legs,
            'allOrNone': False,
            'order_subtype': 'single',
            'order_type': 'regular'
        })

        self.assertEqual(order.toDict(), {
            'm_order_id': 1,
            'price_type': 'limit',
            'time_in_force': 'good_till_cancel',
            'price': '72.50',
            'underlying_stock_symbol': 'COP',
            'source': 'API',
            'client_id': 'someuniqueidentifier',
            'preferred_destination': 'BEST',
            'legs': [
                { 'index': 0, 'phony': 'leg' },
                { 'index': 1, 'phony': 'leg' },
                { 'index': 2, 'phony': 'leg' },
            ],
            'allOrNone': False,
            'order_subtype': 'single',
            'order_type': 'regular'
        })


if __name__ == '__main__':
    unittest.main()
