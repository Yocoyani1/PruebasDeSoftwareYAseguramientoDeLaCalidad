"""
Reservation class for the Reservation System.
Implements reservation abstraction linking customers and hotels.
"""


class Reservation:
    """Represents a room reservation for a customer at a hotel."""

    def __init__(self, data):
        """
        Initialize a Reservation instance from a data dictionary.

        Args:
            data: Dict with keys reservation_id, customer_id, hotel_id,
                  room_number, check_in, check_out, and optional status.
        """
        self.reservation_id = data['reservation_id']
        self.customer_id = data['customer_id']
        self.hotel_id = data['hotel_id']
        self.room_number = data['room_number']
        self.check_in = data['check_in']
        self.check_out = data['check_out']
        self.status = data.get('status', 'active')

    def to_dict(self):
        """Convert reservation to dictionary for serialization."""
        return {
            'reservation_id': self.reservation_id,
            'customer_id': self.customer_id,
            'hotel_id': self.hotel_id,
            'room_number': self.room_number,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        """Create Reservation instance from dictionary."""
        return Reservation(data)
