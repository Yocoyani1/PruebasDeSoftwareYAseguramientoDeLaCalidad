"""
Reservation System - Servicio principal para gestionar hoteles, clientes y
reservaciones. Proporciona persistencia en archivos JSON con manejo de errores.
"""

import json
import os

from ..models import Hotel, Customer, Reservation


class ReservationSystem:
    """Manages hotels, customers and reservations with file persistence."""

    def __init__(self, data_dir='data'):
        """
        Initialize the reservation system with file paths.

        Args:
            data_dir: Directory for storing data files.
        """
        self.data_dir = data_dir
        self.hotels_file = os.path.join(data_dir, 'hotels.json')
        self.customers_file = os.path.join(data_dir, 'customers.json')
        self.reservations_file = os.path.join(data_dir, 'reservations.json')
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create data directory if it does not exist."""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except OSError as err:
            print(f"Error creating data directory: {err}")

    def _load_json_file(self, filepath, default=None):
        """
        Load JSON data from file with error handling.

        Args:
            filepath: Path to the JSON file.
            default: Default value if file is empty or invalid.

        Returns:
            Loaded data or default value.
        """
        if default is None:
            default = []
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content.strip():
                        return default
                    return json.loads(content)
            return default
        except json.JSONDecodeError as err:
            print(f"Error: Invalid JSON in {filepath}: {err}")
            return default
        except IOError as err:
            print(f"Error reading file {filepath}: {err}")
            return default

    def _save_json_file(self, filepath, data):
        """
        Save data to JSON file with error handling.

        Args:
            filepath: Path to the JSON file.
            data: Data to save.

        Returns:
            True if successful, False otherwise.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as err:
            print(f"Error writing file {filepath}: {err}")
            return False

    # Hotel operations
    def create_hotel(self, hotel_id, name, address, total_rooms):
        """Create a new hotel and save to file."""
        hotels = self._load_json_file(self.hotels_file, default=[])
        if any(h.get('hotel_id') == hotel_id for h in hotels):
            print(f"Error: Hotel with ID {hotel_id} already exists.")
            return False
        hotel = Hotel(hotel_id, name, address, total_rooms)
        hotels.append(hotel.to_dict())
        return self._save_json_file(self.hotels_file, hotels)

    def delete_hotel(self, hotel_id):
        """Delete a hotel by ID."""
        hotels = self._load_json_file(self.hotels_file, default=[])
        original_len = len(hotels)
        hotels = [h for h in hotels if h.get('hotel_id') != hotel_id]
        if len(hotels) == original_len:
            print(f"Error: Hotel {hotel_id} not found.")
            return False
        return self._save_json_file(self.hotels_file, hotels)

    def display_hotel(self, hotel_id):
        """Display hotel information by ID."""
        hotels = self._load_json_file(self.hotels_file, default=[])
        for h in hotels:
            if h.get('hotel_id') == hotel_id:
                hotel = Hotel.from_dict(h)
                print(f"Hotel ID: {hotel.hotel_id}")
                print(f"Name: {hotel.name}")
                print(f"Address: {hotel.address}")
                print(f"Total rooms: {hotel.total_rooms}")
                avail = hotel.available_rooms()
                print(f"Available: {avail}")
                return True
        print(f"Error: Hotel {hotel_id} not found.")
        return False

    def modify_hotel(
            self, hotel_id, name=None, address=None, total_rooms=None):
        """Modify hotel information."""
        hotels = self._load_json_file(self.hotels_file, default=[])
        for h in hotels:
            if h.get('hotel_id') == hotel_id:
                if name is not None:
                    h['name'] = name
                if address is not None:
                    h['address'] = address
                if total_rooms is not None:
                    h['total_rooms'] = total_rooms
                return self._save_json_file(self.hotels_file, hotels)
        print(f"Error: Hotel {hotel_id} not found.")
        return False

    def reserve_room(self, hotel_id):
        """Reserve a room at the hotel if available."""
        hotels = self._load_json_file(self.hotels_file, default=[])
        for h in hotels:
            if h.get('hotel_id') == hotel_id:
                available = h['total_rooms'] - h.get('reserved_rooms', 0)
                if available <= 0:
                    print(f"Error: No rooms at hotel {hotel_id}.")
                    return False
                h['reserved_rooms'] = h.get('reserved_rooms', 0) + 1
                return self._save_json_file(self.hotels_file, hotels)
        print(f"Error: Hotel {hotel_id} not found.")
        return False

    def cancel_hotel_reservation(self, hotel_id):
        """Cancel one room reservation at the hotel."""
        hotels = self._load_json_file(self.hotels_file, default=[])
        for h in hotels:
            if h.get('hotel_id') == hotel_id:
                reserved = h.get('reserved_rooms', 0)
                if reserved <= 0:
                    msg = f"Error: No reservations at hotel {hotel_id}."
                    print(msg)
                    return False
                h['reserved_rooms'] = reserved - 1
                return self._save_json_file(self.hotels_file, hotels)
        print(f"Error: Hotel {hotel_id} not found.")
        return False

    # Customer operations
    def create_customer(self, customer_id, name, email, phone):
        """Create a new customer and save to file."""
        customers = self._load_json_file(self.customers_file, default=[])
        exists = any(c.get('customer_id') == customer_id for c in customers)
        if exists:
            print(f"Error: Customer ID {customer_id} already exists.")
            return False
        customer = Customer(customer_id, name, email, phone)
        customers.append(customer.to_dict())
        return self._save_json_file(self.customers_file, customers)

    def delete_customer(self, customer_id):
        """Delete a customer by ID."""
        customers = self._load_json_file(self.customers_file, default=[])
        original_len = len(customers)
        customers = [
            c for c in customers
            if c.get('customer_id') != customer_id
        ]
        if len(customers) == original_len:
            print(f"Error: Customer ID {customer_id} not found.")
            return False
        return self._save_json_file(self.customers_file, customers)

    def display_customer(self, customer_id):
        """Display customer information by ID."""
        customers = self._load_json_file(self.customers_file, default=[])
        for c in customers:
            if c.get('customer_id') == customer_id:
                cust = Customer.from_dict(c)
                print(f"Customer ID: {cust.customer_id}")
                print(f"Name: {cust.name}")
                print(f"Email: {cust.email}")
                print(f"Phone: {cust.phone}")
                return True
        print(f"Error: Customer ID {customer_id} not found.")
        return False

    def modify_customer(self, customer_id, updates):
        """
        Modify customer information.

        Args:
            customer_id: ID of the customer to modify.
            updates: Dict with optional name, email, phone keys.
        """
        customers = self._load_json_file(self.customers_file, default=[])
        for c in customers:
            if c.get('customer_id') == customer_id:
                if 'name' in updates and updates['name'] is not None:
                    c['name'] = updates['name']
                if 'email' in updates and updates['email'] is not None:
                    c['email'] = updates['email']
                if 'phone' in updates and updates['phone'] is not None:
                    c['phone'] = updates['phone']
                return self._save_json_file(self.customers_file, customers)
        print(f"Error: Customer ID {customer_id} not found.")
        return False

    # Reservation operations
    def create_reservation(self, data):
        """
        Create a new reservation linking customer and hotel.

        Args:
            data: Dict with reservation_id, customer_id, hotel_id,
                  room_number, check_in, check_out.
        """
        reservation_id = data['reservation_id']
        customer_id = data['customer_id']
        hotel_id = data['hotel_id']
        reservations = self._load_json_file(self.reservations_file, default=[])
        res_ids = [r.get('reservation_id') for r in reservations]
        exists = reservation_id in res_ids
        if exists:
            print(f"Error: Reservation ID {reservation_id} already exists.")
            return False
        if not self._customer_exists(customer_id):
            print(f"Error: Customer {customer_id} not found.")
            return False
        if not self._hotel_exists(hotel_id):
            print(f"Error: Hotel {hotel_id} not found.")
            return False
        if not self.reserve_room(hotel_id):
            return False
        reservation = Reservation(data)
        reservations.append(reservation.to_dict())
        return self._save_json_file(self.reservations_file, reservations)

    def cancel_reservation(self, reservation_id):
        """Cancel a reservation by ID."""
        reservations = self._load_json_file(self.reservations_file, default=[])
        for r in reservations:
            if r.get('reservation_id') == reservation_id:
                if r.get('status') == 'cancelled':
                    msg = f"Error: Res. {reservation_id} already cancelled."
                    print(msg)
                    return False
                r['status'] = 'cancelled'
                hotel_id = r.get('hotel_id')
                self.cancel_hotel_reservation(hotel_id)
                return self._save_json_file(
                    self.reservations_file, reservations)
        print(f"Error: Reservation {reservation_id} not found.")
        return False

    def _customer_exists(self, customer_id):
        """Check if customer exists."""
        customers = self._load_json_file(self.customers_file, default=[])
        return any(c.get('customer_id') == customer_id for c in customers)

    def _hotel_exists(self, hotel_id):
        """Check if hotel exists."""
        hotels = self._load_json_file(self.hotels_file, default=[])
        return any(h.get('hotel_id') == hotel_id for h in hotels)


def _run_menu_option(system, choice):
    """
    Execute the selected menu option.
    Returns False to exit, True to continue.
    """
    if choice == '0':
        return False
    handlers = {
        '1': _handle_create_hotel,
        '2': _handle_delete_hotel,
        '3': _handle_display_hotel,
        '4': _handle_modify_hotel,
        '5': _handle_reserve_room,
        '6': _handle_cancel_hotel_res,
        '7': _handle_create_customer,
        '8': _handle_delete_customer,
        '9': _handle_display_customer,
        '10': _handle_modify_customer,
        '11': _handle_create_reservation,
        '12': _handle_cancel_reservation,
    }
    handler = handlers.get(choice)
    if handler:
        handler(system)
    else:
        print("Invalid option.")
    return True


def _handle_create_hotel(system):
    """Handle create hotel menu option."""
    hid = input("Hotel ID: ")
    name = input("Name: ")
    addr = input("Address: ")
    rooms = input("Total rooms: ")
    try:
        system.create_hotel(hid, name, addr, int(rooms))
    except ValueError:
        print("Error: Total rooms must be a number.")


def _handle_delete_hotel(system):
    """Handle delete hotel menu option."""
    system.delete_hotel(input("Hotel ID: "))


def _handle_display_hotel(system):
    """Handle display hotel menu option."""
    system.display_hotel(input("Hotel ID: "))


def _handle_modify_hotel(system):
    """Handle modify hotel menu option."""
    hid = input("Hotel ID: ")
    name = input("New name (Enter to skip): ") or None
    addr = input("New address (Enter to skip): ") or None
    rooms = input("New total rooms (Enter to skip): ")
    rooms = int(rooms) if rooms else None
    system.modify_hotel(hid, name, addr, rooms)


def _handle_reserve_room(system):
    """Handle reserve room menu option."""
    system.reserve_room(input("Hotel ID: "))


def _handle_cancel_hotel_res(system):
    """Handle cancel hotel reservation menu option."""
    system.cancel_hotel_reservation(input("Hotel ID: "))


def _handle_create_customer(system):
    """Handle create customer menu option."""
    cid = input("Customer ID: ")
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    system.create_customer(cid, name, email, phone)


def _handle_delete_customer(system):
    """Handle delete customer menu option."""
    system.delete_customer(input("Customer ID: "))


def _handle_display_customer(system):
    """Handle display customer menu option."""
    system.display_customer(input("Customer ID: "))


def _handle_modify_customer(system):
    """Handle modify customer menu option."""
    cid = input("Customer ID: ")
    name = input("New name (Enter to skip): ") or None
    email = input("New email (Enter to skip): ") or None
    phone = input("New phone (Enter to skip): ") or None
    system.modify_customer(cid, {'name': name, 'email': email, 'phone': phone})


def _handle_create_reservation(system):
    """Handle create reservation menu option."""
    rid = input("Reservation ID: ")
    cid = input("Customer ID: ")
    hid = input("Hotel ID: ")
    room = input("Room number: ")
    ci = input("Check-in date: ")
    co = input("Check-out date: ")
    system.create_reservation({
        'reservation_id': rid, 'customer_id': cid, 'hotel_id': hid,
        'room_number': room, 'check_in': ci, 'check_out': co
    })


def _handle_cancel_reservation(system):
    """Handle cancel reservation menu option."""
    system.cancel_reservation(input("Reservation ID: "))


def main():
    """Interactive menu for the reservation system."""
    system = ReservationSystem()
    while True:
        print("\n=== Reservation System ===")
        print("1. Create Hotel    2. Delete Hotel    3. Display Hotel")
        print("4. Modify Hotel    5. Reserve Room    6. Cancel Hotel Res.")
        print("7. Create Customer 8. Delete Customer 9. Display Customer")
        print("10. Modify Customer")
        print("11. Create Reservation  12. Cancel Reservation")
        print("0. Exit")
        choice = input("Select option: ").strip()
        if not _run_menu_option(system, choice):
            break
