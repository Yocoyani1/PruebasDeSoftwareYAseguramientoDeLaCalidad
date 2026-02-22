"""Unit tests for Reservation class."""

import unittest
from src import Reservation


class TestReservation(unittest.TestCase):
    """Test cases for Reservation class."""

    def setUp(self):
        """Set up test fixtures."""
        self.reservation = Reservation({
            'reservation_id': 'R001',
            'customer_id': 'C001',
            'hotel_id': 'H001',
            'room_number': '101',
            'check_in': '2025-03-01',
            'check_out': '2025-03-05'
        })

    def test_reservation_creation(self):
        """Test reservation is created with correct attributes."""
        self.assertEqual(self.reservation.reservation_id, 'R001')
        self.assertEqual(self.reservation.customer_id, 'C001')
        self.assertEqual(self.reservation.hotel_id, 'H001')
        self.assertEqual(self.reservation.room_number, '101')
        self.assertEqual(self.reservation.check_in, '2025-03-01')
        self.assertEqual(self.reservation.check_out, '2025-03-05')
        self.assertEqual(self.reservation.status, 'active')

    def test_reservation_with_custom_status(self):
        """Test reservation with custom status."""
        res = Reservation({
            'reservation_id': 'R002',
            'customer_id': 'C002',
            'hotel_id': 'H002',
            'room_number': '102',
            'check_in': '2025-04-01',
            'check_out': '2025-04-03',
            'status': 'cancelled'
        })
        self.assertEqual(res.status, 'cancelled')

    def test_to_dict(self):
        """Test conversion to dictionary."""
        data = self.reservation.to_dict()
        self.assertEqual(data['reservation_id'], 'R001')
        self.assertEqual(data['customer_id'], 'C001')
        self.assertEqual(data['hotel_id'], 'H001')
        self.assertEqual(data['room_number'], '101')
        self.assertEqual(data['check_in'], '2025-03-01')
        self.assertEqual(data['check_out'], '2025-03-05')
        self.assertEqual(data['status'], 'active')

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'reservation_id': 'R002',
            'customer_id': 'C002',
            'hotel_id': 'H002',
            'room_number': '202',
            'check_in': '2025-04-01',
            'check_out': '2025-04-05',
            'status': 'cancelled'
        }
        res = Reservation.from_dict(data)
        self.assertEqual(res.reservation_id, 'R002')
        self.assertEqual(res.customer_id, 'C002')
        self.assertEqual(res.hotel_id, 'H002')
        self.assertEqual(res.room_number, '202')
        self.assertEqual(res.status, 'cancelled')

    def test_from_dict_default_status(self):
        """Test from_dict with missing status uses default 'active'."""
        data = {
            'reservation_id': 'R003',
            'customer_id': 'C003',
            'hotel_id': 'H003',
            'room_number': '303',
            'check_in': '2025-05-01',
            'check_out': '2025-05-03'
        }
        res = Reservation.from_dict(data)
        self.assertEqual(res.status, 'active')

    def test_init_missing_required_key_raises(self):
        """Test __init__ with missing reservation_id raises KeyError."""
        data = {
            'customer_id': 'C001',
            'hotel_id': 'H001',
            'room_number': '101',
            'check_in': '2025-03-01',
            'check_out': '2025-03-05'
        }
        with self.assertRaises(KeyError):
            Reservation(data)

    def test_init_empty_dict_raises(self):
        """Test __init__ with empty dict raises KeyError."""
        with self.assertRaises(KeyError):
            Reservation({})

    def test_from_dict_with_none_raises(self):
        """Test from_dict with None raises TypeError."""
        with self.assertRaises(TypeError):
            Reservation.from_dict(None)


if __name__ == '__main__':
    unittest.main()
