"""Unit tests for ReservationSystem and main()."""

import unittest
import os
import tempfile
import shutil
import sys
from io import StringIO
from unittest.mock import patch

from src import ReservationSystem, main


class TestReservationSystem(unittest.TestCase):
    """Test cases for ReservationSystem with file persistence."""

    def setUp(self):
        """Set up temporary data directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.system = ReservationSystem(data_dir=self.temp_dir)

    def tearDown(self):
        """Remove temporary directory after each test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_hotel(self):
        """Test creating a hotel."""
        result = self.system.create_hotel('H001', 'Hotel Test', 'Addr 1', 10)
        self.assertTrue(result)
        hotels = self.system._load_json_file(self.system.hotels_file)
        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0]['name'], 'Hotel Test')

    def test_create_duplicate_hotel_fails(self):
        """Test that creating duplicate hotel returns False."""
        self.system.create_hotel('H001', 'Hotel 1', 'Addr', 5)
        result = self.system.create_hotel('H001', 'Hotel 2', 'Addr2', 3)
        self.assertFalse(result)

    def test_delete_hotel(self):
        """Test deleting a hotel."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        result = self.system.delete_hotel('H001')
        self.assertTrue(result)
        hotels = self.system._load_json_file(self.system.hotels_file)
        self.assertEqual(len(hotels), 0)

    def test_delete_nonexistent_hotel_fails(self):
        """Test deleting non-existent hotel returns False."""
        result = self.system.delete_hotel('H999')
        self.assertFalse(result)

    def test_display_hotel(self):
        """Test displaying hotel information."""
        self.system.create_hotel('H001', 'Hotel Display', 'Address 123', 20)
        captured = StringIO()
        sys.stdout = captured
        result = self.system.display_hotel('H001')
        sys.stdout = sys.__stdout__
        self.assertTrue(result)
        self.assertIn('Hotel Display', captured.getvalue())
        self.assertIn('20', captured.getvalue())

    def test_display_nonexistent_hotel_fails(self):
        """Test displaying non-existent hotel returns False."""
        captured = StringIO()
        sys.stdout = captured
        result = self.system.display_hotel('H999')
        sys.stdout = sys.__stdout__
        self.assertFalse(result)

    def test_modify_hotel(self):
        """Test modifying hotel information."""
        self.system.create_hotel('H001', 'Old Name', 'Old Addr', 10)
        result = self.system.modify_hotel(
            'H001', name='New Name', address='New Addr'
        )
        self.assertTrue(result)
        hotels = self.system._load_json_file(self.system.hotels_file)
        self.assertEqual(hotels[0]['name'], 'New Name')
        self.assertEqual(hotels[0]['address'], 'New Addr')
        self.assertEqual(hotels[0]['total_rooms'], 10)

    def test_modify_nonexistent_hotel_fails(self):
        """Test modifying non-existent hotel returns False."""
        result = self.system.modify_hotel('H999', name='New')
        self.assertFalse(result)

    def test_reserve_room(self):
        """Test reserving a room at hotel."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        result = self.system.reserve_room('H001')
        self.assertTrue(result)
        hotels = self.system._load_json_file(self.system.hotels_file)
        self.assertEqual(hotels[0]['reserved_rooms'], 1)

    def test_reserve_room_when_full_fails(self):
        """Test reserving when no rooms available fails."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 1)
        self.system.reserve_room('H001')
        result = self.system.reserve_room('H001')
        self.assertFalse(result)

    def test_cancel_hotel_reservation(self):
        """Test cancelling a room reservation at hotel."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        self.system.reserve_room('H001')
        result = self.system.cancel_hotel_reservation('H001')
        self.assertTrue(result)
        hotels = self.system._load_json_file(self.system.hotels_file)
        self.assertEqual(hotels[0]['reserved_rooms'], 0)

    def test_create_customer(self):
        """Test creating a customer."""
        result = self.system.create_customer('C001', 'John', 'j@e.com', '555')
        self.assertTrue(result)
        customers = self.system._load_json_file(self.system.customers_file)
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]['name'], 'John')

    def test_create_duplicate_customer_fails(self):
        """Test creating duplicate customer returns False."""
        self.system.create_customer('C001', 'John', 'j@e.com', '555')
        result = self.system.create_customer('C001', 'Jane', 'j2@e.com', '556')
        self.assertFalse(result)

    def test_delete_customer(self):
        """Test deleting a customer."""
        self.system.create_customer('C001', 'John', 'j@e.com', '555')
        result = self.system.delete_customer('C001')
        self.assertTrue(result)
        customers = self.system._load_json_file(self.system.customers_file)
        self.assertEqual(len(customers), 0)

    def test_display_customer(self):
        """Test displaying customer information."""
        self.system.create_customer('C001', 'Jane Doe', 'jane@e.com', '123')
        captured = StringIO()
        sys.stdout = captured
        result = self.system.display_customer('C001')
        sys.stdout = sys.__stdout__
        self.assertTrue(result)
        self.assertIn('Jane Doe', captured.getvalue())

    def test_modify_customer(self):
        """Test modifying customer information."""
        self.system.create_customer('C001', 'Old', 'old@e.com', '111')
        result = self.system.modify_customer(
            'C001', {'name': 'New', 'email': 'new@e.com'}
        )
        self.assertTrue(result)
        customers = self.system._load_json_file(self.system.customers_file)
        self.assertEqual(customers[0]['name'], 'New')
        self.assertEqual(customers[0]['email'], 'new@e.com')

    def _reservation_data(self, rid='R001', cid='C001', hid='H001',
                          room='101', ci='2025-03-01', co='2025-03-05'):
        """Build reservation data dict for tests."""
        return {
            'reservation_id': rid, 'customer_id': cid, 'hotel_id': hid,
            'room_number': room, 'check_in': ci, 'check_out': co
        }

    def test_create_reservation(self):
        """Test creating a reservation."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        self.system.create_customer('C001', 'John', 'j@e.com', '555')
        result = self.system.create_reservation(self._reservation_data())
        self.assertTrue(result)
        reservations = self.system._load_json_file(
            self.system.reservations_file
        )
        self.assertEqual(len(reservations), 1)
        self.assertEqual(reservations[0]['status'], 'active')
        hotels = self.system._load_json_file(self.system.hotels_file)
        self.assertEqual(hotels[0]['reserved_rooms'], 1)

    def test_create_reservation_invalid_customer_fails(self):
        """Test creating reservation with non-existent customer fails."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        result = self.system.create_reservation(
            self._reservation_data(cid='C999')
        )
        self.assertFalse(result)

    def test_create_reservation_invalid_hotel_fails(self):
        """Test creating reservation with non-existent hotel fails."""
        self.system.create_customer('C001', 'John', 'j@e.com', '555')
        result = self.system.create_reservation(
            self._reservation_data(hid='H999')
        )
        self.assertFalse(result)

    def test_cancel_reservation(self):
        """Test cancelling a reservation."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        self.system.create_customer('C001', 'John', 'j@e.com', '555')
        self.system.create_reservation(self._reservation_data())
        result = self.system.cancel_reservation('R001')
        self.assertTrue(result)
        reservations = self.system._load_json_file(
            self.system.reservations_file
        )
        self.assertEqual(reservations[0]['status'], 'cancelled')
        hotels = self.system._load_json_file(self.system.hotels_file)
        self.assertEqual(hotels[0]['reserved_rooms'], 0)

    def test_delete_nonexistent_customer_fails(self):
        """Test deleting non-existent customer returns False."""
        result = self.system.delete_customer('C999')
        self.assertFalse(result)

    def test_display_nonexistent_customer_fails(self):
        """Test displaying non-existent customer returns False."""
        captured = StringIO()
        sys.stdout = captured
        result = self.system.display_customer('C999')
        sys.stdout = sys.__stdout__
        self.assertFalse(result)

    def test_modify_nonexistent_customer_fails(self):
        """Test modifying non-existent customer returns False."""
        result = self.system.modify_customer('C999', {'name': 'New'})
        self.assertFalse(result)

    def test_create_reservation_duplicate_fails(self):
        """Test creating duplicate reservation returns False."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        self.system.create_customer('C001', 'John', 'j@e.com', '555')
        self.system.create_reservation(self._reservation_data())
        result = self.system.create_reservation(
            self._reservation_data(
                room='102',
                ci='2025-03-02',
                co='2025-03-06'
            )
        )
        self.assertFalse(result)

    def test_cancel_reservation_already_cancelled_fails(self):
        """Test cancelling already cancelled reservation returns False."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        self.system.create_customer('C001', 'John', 'j@e.com', '555')
        self.system.create_reservation(self._reservation_data())
        self.system.cancel_reservation('R001')
        captured = StringIO()
        sys.stdout = captured
        result = self.system.cancel_reservation('R001')
        sys.stdout = sys.__stdout__
        self.assertFalse(result)

    def test_cancel_nonexistent_reservation_fails(self):
        """Test cancelling non-existent reservation returns False."""
        captured = StringIO()
        sys.stdout = captured
        result = self.system.cancel_reservation('R999')
        sys.stdout = sys.__stdout__
        self.assertFalse(result)

    def test_cancel_hotel_reservation_when_none_fails(self):
        """Test cancelling room when none reserved returns False."""
        self.system.create_hotel('H001', 'Hotel', 'Addr', 5)
        captured = StringIO()
        sys.stdout = captured
        result = self.system.cancel_hotel_reservation('H001')
        sys.stdout = sys.__stdout__
        self.assertFalse(result)

    def test_load_invalid_json_returns_default(self):
        """Test that invalid JSON file returns default and continues."""
        invalid_path = os.path.join(self.temp_dir, 'invalid.json')
        with open(invalid_path, 'w', encoding='utf-8') as f:
            f.write('not valid json {')
        result = self.system._load_json_file(invalid_path, default=[])
        self.assertEqual(result, [])

    def test_ensure_data_dir_creates_directory(self):
        """Test that data directory is created."""
        new_dir = os.path.join(self.temp_dir, 'new_data')
        ReservationSystem(data_dir=new_dir)
        self.assertTrue(os.path.isdir(new_dir))


class TestMain(unittest.TestCase):
    """Test cases for main() interactive menu."""

    def setUp(self):
        """Set up temporary data directory."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Remove temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('src.services.system.ReservationSystem')
    @patch('builtins.input', side_effect=['0'])
    def test_main_exit_immediately(self, mock_input, mock_system):
        """Test main exits when user selects 0."""
        main()
        mock_system.assert_called_once()

    @patch('src.services.system.ReservationSystem')
    @patch('builtins.input',
           side_effect=['1', 'H001', 'Hotel A', 'Addr 1', '5', '0'])
    def test_main_create_hotel(self, mock_input, mock_system):
        """Test main creates hotel via menu option 1."""
        instance = mock_system.return_value
        instance.create_hotel.return_value = True
        main()
        instance.create_hotel.assert_called_once_with(
            'H001', 'Hotel A', 'Addr 1', 5
        )

    @patch('src.services.system.ReservationSystem')
    @patch('builtins.input',
           side_effect=['1', 'H001', 'Hotel', 'Addr', 'bad', '0'])
    def test_main_create_hotel_invalid_rooms(self, mock_input, mock_system):
        """Test main handles invalid total rooms."""
        main()
        instance = mock_system.return_value
        instance.create_hotel.assert_not_called()

    @patch('src.services.system.ReservationSystem')
    @patch('builtins.input',
           side_effect=['7', 'C001', 'John', 'j@e.com', '555', '0'])
    def test_main_create_customer(self, mock_input, mock_system):
        """Test main creates customer via menu option 7."""
        instance = mock_system.return_value
        instance.create_customer.return_value = True
        main()
        instance.create_customer.assert_called_once_with(
            'C001', 'John', 'j@e.com', '555'
        )

    @patch('src.services.system.ReservationSystem')
    @patch('builtins.input', side_effect=['99', '0'])
    def test_main_invalid_option(self, mock_input, mock_system):
        """Test main handles invalid menu option."""
        main()
        mock_system.assert_called_once()


if __name__ == '__main__':
    unittest.main()
