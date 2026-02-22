"""
Hotel class for the Reservation System.
Implements hotel abstraction with attributes for hotel management.
"""


class Hotel:
    """Represents a hotel with rooms and basic information."""

    def __init__(self, hotel_id, name, address, total_rooms):
        """
        Initialize a Hotel instance.

        Args:
            hotel_id: Unique identifier for the hotel.
            name: Name of the hotel.
            address: Physical address of the hotel.
            total_rooms: Total number of rooms available.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.address = address
        self.total_rooms = total_rooms
        self.reserved_rooms = 0

    def available_rooms(self):
        """Return the number of available rooms."""
        return self.total_rooms - self.reserved_rooms

    def to_dict(self):
        """Convert hotel to dictionary for serialization."""
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'address': self.address,
            'total_rooms': self.total_rooms,
            'reserved_rooms': self.reserved_rooms
        }

    @staticmethod
    def from_dict(data):
        """Create Hotel instance from dictionary."""
        hotel = Hotel(
            hotel_id=data['hotel_id'],
            name=data['name'],
            address=data['address'],
            total_rooms=data['total_rooms']
        )
        hotel.reserved_rooms = data.get('reserved_rooms', 0)
        return hotel
