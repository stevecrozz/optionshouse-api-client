import sys
if 'optionshouse' not in sys.path:
    sys.path.append('optionshouse')

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
            legs=legs,
            allOrNone=False,
            order_subtype='single',
        )

        expected_data = {
            'm_order_id': 1,
            'price_type': 'limit',
            'time_in_force': 'good_till_cancel',
            'price': '72.50',
            'underlying_stock_symbol': 'COP',
            'source': 'API',
            'client_id': order.data['client_id'],
            'preferred_destination': 'BEST',
            'legs': legs,
            'allOrNone': False,
            'order_subtype': 'spread',
            'order_type': 'regular'
        }
        self.assertEqual(order.data, expected_data)

        expected_data['legs'] = [
            { 'index': 0, 'phony': 'leg' },
            { 'index': 1, 'phony': 'leg' },
            { 'index': 2, 'phony': 'leg' },
        ]
        self.assertEqual(order.toDict(), expected_data)

        order.modify(1337)
        expected_data['modify_order'] = True
        expected_data['order_id'] = 1337
        self.assertEqual(order.toDict(), expected_data)


if __name__ == '__main__':
    unittest.main()
