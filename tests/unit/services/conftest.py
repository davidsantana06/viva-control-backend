import pytest
from unittest.mock import MagicMock

from app.types import OrderStatus, UserRole


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    user.email = "user@example.com"
    user.password_hash = "$2b$12$hashedpasswordexample"
    user.role = UserRole.DISTRIBUTOR
    user.is_active = True
    user.distributor_id = None
    user.sellers = []
    return user


@pytest.fixture
def mock_customer():
    customer = MagicMock()
    customer.id = 1
    customer.distributor_id = 1
    customer.name = "Customer Test"
    return customer


@pytest.fixture
def mock_product():
    product = MagicMock()
    product.id = 1
    product.sku = "SKU-001"
    product.name = "Product Test"
    return product


@pytest.fixture
def mock_order():
    order = MagicMock()
    order.id = 1
    order.status = OrderStatus.PENDING
    order.is_cancelled = False
    order.items = []
    order.distributor_id = 1
    return order


@pytest.fixture
def mock_stock():
    stock = MagicMock()
    stock.id = 1
    stock.product_id = 1
    stock.distributor_id = 1
    stock.current_quantity = 100.0
    return stock


@pytest.fixture
def mock_payment_method():
    payment_method = MagicMock()
    payment_method.id = 1
    payment_method.name = "Dinheiro"
    return payment_method
