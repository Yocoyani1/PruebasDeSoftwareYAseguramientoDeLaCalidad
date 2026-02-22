"""Unit tests for Customer class."""

import unittest
from src import Customer


class TestCustomer(unittest.TestCase):
    """Test cases for Customer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.customer = Customer(
            customer_id='C001',
            name='John Doe',
            email='john@email.com',
            phone='555-1234'
        )

    def test_customer_creation(self):
        """Test customer is created with correct attributes."""
        self.assertEqual(self.customer.customer_id, 'C001')
        self.assertEqual(self.customer.name, 'John Doe')
        self.assertEqual(self.customer.email, 'john@email.com')
        self.assertEqual(self.customer.phone, '555-1234')

    def test_to_dict(self):
        """Test conversion to dictionary."""
        data = self.customer.to_dict()
        self.assertEqual(data['customer_id'], 'C001')
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['email'], 'john@email.com')
        self.assertEqual(data['phone'], '555-1234')

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'customer_id': 'C002',
            'name': 'Jane Doe',
            'email': 'jane@email.com',
            'phone': '555-5678'
        }
        customer = Customer.from_dict(data)
        self.assertEqual(customer.customer_id, 'C002')
        self.assertEqual(customer.name, 'Jane Doe')
        self.assertEqual(customer.email, 'jane@email.com')
        self.assertEqual(customer.phone, '555-5678')

    def test_from_dict_missing_required_key_raises(self):
        """Test from_dict with missing customer_id raises KeyError."""
        data = {
            'name': 'Jane',
            'email': 'jane@email.com',
            'phone': '555-5678'
        }
        with self.assertRaises(KeyError):
            Customer.from_dict(data)

    def test_from_dict_empty_raises(self):
        """Test from_dict with empty dict raises KeyError."""
        with self.assertRaises(KeyError):
            Customer.from_dict({})


if __name__ == '__main__':
    unittest.main()
