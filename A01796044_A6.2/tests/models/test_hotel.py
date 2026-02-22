"""Unit tests for Hotel class."""

import unittest
from src import Hotel


class TestHotel(unittest.TestCase):
    """Test cases for Hotel class."""

    def setUp(self):
        """Set up test fixtures."""
        self.hotel = Hotel(
            hotel_id='H001',
            name='Test Hotel',
            address='Test Address 123',
            total_rooms=10
        )

    def test_hotel_creation(self):
        """Test hotel is created with correct attributes."""
        self.assertEqual(self.hotel.hotel_id, 'H001')
        self.assertEqual(self.hotel.name, 'Test Hotel')
        self.assertEqual(self.hotel.address, 'Test Address 123')
        self.assertEqual(self.hotel.total_rooms, 10)
        self.assertEqual(self.hotel.reserved_rooms, 0)

    def test_available_rooms_initial(self):
        """Test available rooms when no reservations."""
        self.assertEqual(self.hotel.available_rooms(), 10)

    def test_available_rooms_after_reservation(self):
        """Test available rooms after some rooms reserved."""
        self.hotel.reserved_rooms = 3
        self.assertEqual(self.hotel.available_rooms(), 7)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        data = self.hotel.to_dict()
        self.assertEqual(data['hotel_id'], 'H001')
        self.assertEqual(data['name'], 'Test Hotel')
        self.assertEqual(data['address'], 'Test Address 123')
        self.assertEqual(data['total_rooms'], 10)
        self.assertEqual(data['reserved_rooms'], 0)

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'hotel_id': 'H002',
            'name': 'Another Hotel',
            'address': 'Other Address',
            'total_rooms': 5,
            'reserved_rooms': 2
        }
        hotel = Hotel.from_dict(data)
        self.assertEqual(hotel.hotel_id, 'H002')
        self.assertEqual(hotel.name, 'Another Hotel')
        self.assertEqual(hotel.total_rooms, 5)
        self.assertEqual(hotel.reserved_rooms, 2)
        self.assertEqual(hotel.available_rooms(), 3)

    def test_from_dict_default_reserved(self):
        """Test from_dict with missing reserved_rooms uses default 0."""
        data = {
            'hotel_id': 'H003',
            'name': 'Hotel',
            'address': 'Addr',
            'total_rooms': 3
        }
        hotel = Hotel.from_dict(data)
        self.assertEqual(hotel.reserved_rooms, 0)

    def test_from_dict_missing_required_key_raises(self):
        """Test from_dict with missing hotel_id raises KeyError."""
        data = {
            'name': 'Hotel',
            'address': 'Addr',
            'total_rooms': 5
        }
        with self.assertRaises(KeyError):
            Hotel.from_dict(data)

    def test_from_dict_empty_raises(self):
        """Test from_dict with empty dict raises KeyError."""
        with self.assertRaises(KeyError):
            Hotel.from_dict({})

    def test_available_rooms_when_overbooked_returns_negative(self):
        """
        Test available_rooms returns negative
        when reserved exceeds total.
        """
        self.hotel.reserved_rooms = 15
        self.assertEqual(self.hotel.available_rooms(), -5)


if __name__ == '__main__':
    unittest.main()
