import json
from typing import List, Optional
from products import Product, get_product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        """Load a Cart object from a dictionary."""
        contents = [get_product(item) for item in data.get('contents', [])]
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=contents,
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """Retrieve the cart contents for a given username."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    products_list = []
    for cart_detail in cart_details:
        try:
            # Safely parse contents as a JSON list
            contents = json.loads(cart_detail['contents'])
            products_list.extend(get_product(item) for item in contents)
        except (json.JSONDecodeError, KeyError):
            continue  # Skip invalid entries

    return products_list


def add_to_cart(username: str, product_id: int) -> None:
    """Add a product to the user's cart."""
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """Remove a product from the user's cart."""
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """Delete the user's cart."""
    dao.delete_cart(username)
