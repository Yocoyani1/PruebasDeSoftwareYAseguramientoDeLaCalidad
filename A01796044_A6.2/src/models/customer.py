"""
Customer class for the Reservation System.
Implements customer abstraction with attributes for customer management.
"""


class Customer:
    """Represents a customer in the reservation system."""

    def __init__(self, customer_id, name, email, phone):
        """
        Initialize a Customer instance.

        Args:
            customer_id: Unique identifier for the customer.
            name: Full name of the customer.
            email: Email address of the customer.
            phone: Phone number of the customer.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Convert customer to dictionary for serialization."""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

    @staticmethod
    def from_dict(data):
        """Create Customer instance from dictionary."""
        return Customer(
            customer_id=data['customer_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
