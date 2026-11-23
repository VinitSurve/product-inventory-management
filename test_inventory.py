"""Comprehensive pytest test suite for Product Inventory Management System."""

import pytest

from inventory import apply_discount, calculate_total_price, check_stock


class TestCalculateTotalPrice:
    """Tests for calculate_total_price(price, quantity)."""

    def test_normal_calculation(self):
        """Test regular calculations with integer and float prices."""
        assert calculate_total_price(50000, 2) == 100000.0
        assert calculate_total_price(250.50, 4) == 1002.0
        assert calculate_total_price(99.99, 3) == 299.97

    def test_zero_quantity(self):
        """Test zero quantity boundary case (allowed, returns 0.0)."""
        assert calculate_total_price(500, 0) == 0.0

    def test_zero_price(self):
        """Test zero price boundary case (free promotional items)."""
        assert calculate_total_price(0, 10) == 0.0
        assert calculate_total_price(0, 0) == 0.0

    def test_negative_price_raises_value_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_total_price(-100, 2)

    def test_negative_quantity_raises_value_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            calculate_total_price(100, -2)

    @pytest.mark.parametrize("invalid_price", ["100", None, [100], {"p": 100}])
    def test_invalid_price_type_raises_type_error(self, invalid_price):
        """Test that non-numeric price raises TypeError."""
        with pytest.raises(TypeError, match="Price must be a numeric value"):
            calculate_total_price(invalid_price, 2)

    @pytest.mark.parametrize("invalid_qty", [2.5, "2", None, [2]])
    def test_invalid_quantity_type_raises_type_error(self, invalid_qty):
        """Test that non-integer quantity raises TypeError."""
        with pytest.raises(TypeError, match="Quantity must be an integer"):
            calculate_total_price(100, invalid_qty)

    def test_reject_boolean_values(self):
        """Test that bools (subclasses of int) are rejected as invalid types."""
        with pytest.raises(TypeError):
            calculate_total_price(True, 5)
        with pytest.raises(TypeError):
            calculate_total_price(100, True)
        with pytest.raises(TypeError):
            calculate_total_price(False, False)


class TestApplyDiscount:
    """Tests for apply_discount(total, discount_percent)."""

    def test_normal_discount(self):
        """Test standard discount values."""
        assert apply_discount(100000, 10) == 90000.0
        assert apply_discount(500, 25) == 375.0
        assert apply_discount(1200.50, 15) == 1020.42

    def test_zero_discount(self):
        """Test 0% discount returns original total."""
        assert apply_discount(1500, 0) == 1500.0
        assert apply_discount(0, 0) == 0.0

    def test_full_discount_100_percent(self):
        """Test 100% discount returns 0.0."""
        assert apply_discount(2500, 100) == 0.0
        assert apply_discount(0, 100) == 0.0

    @pytest.mark.parametrize("invalid_discount", [100.01, 120, 200])
    def test_discount_greater_than_100_raises_value_error(self, invalid_discount):
        """Test that discount > 100 raises ValueError."""
        with pytest.raises(
            ValueError, match="Discount percentage must be between 0 and 100"
        ):
            apply_discount(1000, invalid_discount)

    @pytest.mark.parametrize("negative_discount", [-0.01, -5, -50])
    def test_negative_discount_raises_value_error(self, negative_discount):
        """Test that negative discount raises ValueError."""
        with pytest.raises(
            ValueError, match="Discount percentage must be between 0 and 100"
        ):
            apply_discount(1000, negative_discount)

    def test_negative_total_raises_value_error(self):
        """Test that negative total raises ValueError."""
        with pytest.raises(ValueError, match="Total cannot be negative"):
            apply_discount(-500, 10)

    @pytest.mark.parametrize("invalid_type", ["1000", None, [1000]])
    def test_invalid_total_type_raises_type_error(self, invalid_type):
        """Test invalid total types raise TypeError."""
        with pytest.raises(TypeError, match="Total must be a numeric value"):
            apply_discount(invalid_type, 10)

    @pytest.mark.parametrize("invalid_type", ["10", None, [10]])
    def test_invalid_discount_type_raises_type_error(self, invalid_type):
        """Test invalid discount types raise TypeError."""
        with pytest.raises(TypeError, match="Discount percent must be a numeric value"):
            apply_discount(1000, invalid_type)

    def test_reject_boolean_values(self):
        """Test boolean rejection for apply_discount."""
        with pytest.raises(TypeError):
            apply_discount(True, 10)
        with pytest.raises(TypeError):
            apply_discount(1000, False)


class TestCheckStock:
    """Tests for check_stock(available_stock, requested_quantity)."""

    def test_stock_available(self):
        """Test case where requested quantity is strictly less than stock."""
        assert check_stock(10, 5) is True
        assert check_stock(100, 1) is True

    def test_exact_stock_quantity(self):
        """Test boundary case where requested quantity equals available stock."""
        assert check_stock(5, 5) is True
        assert check_stock(0, 0) is True

    def test_insufficient_stock(self):
        """Test case where requested quantity exceeds available stock."""
        assert check_stock(5, 6) is False
        assert check_stock(0, 1) is False

    def test_zero_requested_quantity(self):
        """Test requested quantity is zero (always fulfillable)."""
        assert check_stock(10, 0) is True
        assert check_stock(0, 0) is True

    def test_negative_stock_raises_value_error(self):
        """Test that negative stock raises ValueError."""
        with pytest.raises(ValueError, match="Available stock cannot be negative"):
            check_stock(-5, 2)

    def test_negative_requested_quantity_raises_value_error(self):
        """Test that negative requested quantity raises ValueError."""
        with pytest.raises(ValueError, match="Requested quantity cannot be negative"):
            check_stock(10, -2)

    @pytest.mark.parametrize("invalid_val", [5.5, "5", None, [5]])
    def test_invalid_stock_type_raises_type_error(self, invalid_val):
        """Test non-integer stock raises TypeError."""
        with pytest.raises(TypeError, match="Available stock must be an integer"):
            check_stock(invalid_val, 2)

    @pytest.mark.parametrize("invalid_val", [2.5, "2", None, [2]])
    def test_invalid_requested_quantity_type_raises_type_error(self, invalid_val):
        """Test non-integer requested quantity raises TypeError."""
        with pytest.raises(TypeError, match="Requested quantity must be an integer"):
            check_stock(10, invalid_val)

    def test_reject_boolean_values(self):
        """Test boolean rejection for check_stock."""
        with pytest.raises(TypeError):
            check_stock(True, 5)
        with pytest.raises(TypeError):
            check_stock(10, False)
        with pytest.raises(TypeError):
            check_stock(True, False)
