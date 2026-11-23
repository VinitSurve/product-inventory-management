"""Product Inventory Management System module for Assignment 10.

Provides functions for price calculation, discount processing, and stock
availability verification with comprehensive input validation and structured logging.
"""

import logging
from pathlib import Path

LOG_FILE = Path(__file__).parent / "application.log"


def get_logger() -> logging.Logger:
    """Configure and return the inventory application logger."""
    logger = logging.getLogger("InventoryManagementSystem")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = get_logger()


def calculate_total_price(price: float, quantity: int) -> float:
    """Calculate the total price of a product given unit price and quantity.

    total = price * quantity

    Args:
        price: Unit price of the product (must be >= 0).
        quantity: Non-negative integer quantity (must be an integer >= 0).

    Returns:
        The total price rounded to 2 decimal places.

    Raises:
        TypeError: If price is not numeric or quantity is not an int, or if either is a boolean.
        ValueError: If price or quantity is negative.
    """
    # Reject boolean values (since bool is a subclass of int in Python)
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        logger.error(
            "Validation Error: Invalid price type '%s' (expected float or int).",
            type(price).__name__,
        )
        raise TypeError("Price must be a numeric value (int or float).")

    if isinstance(quantity, bool) or not isinstance(quantity, int):
        logger.error(
            "Validation Error: Invalid quantity type '%s' (expected int).",
            type(quantity).__name__,
        )
        raise TypeError("Quantity must be an integer.")

    if price < 0:
        logger.error("Validation Error: Negative price provided: %s.", price)
        raise ValueError("Price cannot be negative.")

    if quantity < 0:
        logger.error("Validation Error: Negative quantity provided: %s.", quantity)
        raise ValueError("Quantity cannot be negative.")

    total = price * quantity
    logger.info(
        "Total price calculated: Price=Rs. %.2f x Qty=%d => Total=Rs. %.2f",
        price,
        quantity,
        total,
    )
    return round(float(total), 2)


def apply_discount(total: float, discount_percent: float) -> float:
    """Calculate the discounted total for a given total and discount percentage.

    Formula: discounted_total = total - (total * discount_percent / 100)

    Args:
        total: Non-negative base total amount.
        discount_percent: Percentage discount in range [0, 100].

    Returns:
        The final discounted total rounded to 2 decimal places.

    Raises:
        TypeError: If total or discount_percent is non-numeric or is a boolean.
        ValueError: If total is negative or discount_percent is not in [0, 100].
    """
    if isinstance(total, bool) or not isinstance(total, (int, float)):
        logger.error("Validation Error: Invalid total type '%s'.", type(total).__name__)
        raise TypeError("Total must be a numeric value (int or float).")

    if isinstance(discount_percent, bool) or not isinstance(
        discount_percent, (int, float)
    ):
        logger.error(
            "Validation Error: Invalid discount_percent type '%s'.",
            type(discount_percent).__name__,
        )
        raise TypeError("Discount percent must be a numeric value (int or float).")

    if total < 0:
        logger.error("Validation Error: Negative total provided: %s.", total)
        raise ValueError("Total cannot be negative.")

    if not (0 <= discount_percent <= 100):
        logger.error(
            "Validation Error: Discount percent %s out of range [0, 100].",
            discount_percent,
        )
        raise ValueError("Discount percentage must be between 0 and 100 inclusive.")

    discount_amount = total * (discount_percent / 100.0)
    discounted_total = total - discount_amount
    logger.info(
        "Discount applied: Total=Rs. %.2f, Rate=%.2f%% => Discounted=Rs. %.2f",
        total,
        discount_percent,
        discounted_total,
    )
    return round(float(discounted_total), 2)


def check_stock(available_stock: int, requested_quantity: int) -> bool:
    """Determine whether the requested quantity can be fulfilled from available stock.

    Args:
        available_stock: Available inventory units (must be integer >= 0).
        requested_quantity: Customer requested quantity (must be integer >= 0).

    Returns:
        True if requested_quantity <= available_stock, False otherwise.

    Raises:
        TypeError: If available_stock or requested_quantity is not an int or is a boolean.
        ValueError: If either value is negative.
    """
    if isinstance(available_stock, bool) or not isinstance(available_stock, int):
        logger.error(
            "Validation Error: available_stock must be an int, got '%s'.",
            type(available_stock).__name__,
        )
        raise TypeError("Available stock must be an integer.")

    if isinstance(requested_quantity, bool) or not isinstance(requested_quantity, int):
        logger.error(
            "Validation Error: requested_quantity must be an int, got '%s'.",
            type(requested_quantity).__name__,
        )
        raise TypeError("Requested quantity must be an integer.")

    if available_stock < 0:
        logger.error(
            "Validation Error: available_stock cannot be negative: %s.",
            available_stock,
        )
        raise ValueError("Available stock cannot be negative.")

    if requested_quantity < 0:
        logger.error(
            "Validation Error: requested_quantity cannot be negative: %s.",
            requested_quantity,
        )
        raise ValueError("Requested quantity cannot be negative.")

    logger.debug(
        "Stock Check: Available=%d, Requested=%d",
        available_stock,
        requested_quantity,
    )

    if requested_quantity <= available_stock:
        return True
    else:
        logger.warning(
            "Stock Alert: Insufficient inventory! Available: %d, Requested: %d",
            available_stock,
            requested_quantity,
        )
        return False


def run_demonstration():
    """Execute runnable interactive demonstration showing all required scenarios."""
    print("=" * 45)
    print("   PRODUCT INVENTORY MANAGEMENT SYSTEM")
    print("=" * 45)

    logger.info("=== Inventory Operation Started ===")

    # Scenario 1: Standard product purchase with stock available
    product_name = "Laptop"
    price = 50000.0
    qty = 2
    discount_pct = 10.0
    stock = 5

    print(f"\nProduct: {product_name}")
    print(f"Price: Rs. {price:.2f}")
    print(f"Quantity: {qty}")

    total_price = calculate_total_price(price, qty)
    print(f"Total Price: Rs. {total_price:.2f}")

    final_price = apply_discount(total_price, discount_pct)
    print(f"Discount: {discount_pct:.0f}%")
    print(f"Final Price: Rs. {final_price:.2f}")

    print(f"Available Stock: {stock}")
    print(f"Requested Quantity: {qty}")
    is_available = check_stock(stock, qty)
    print(f"Stock Available: {'Yes' if is_available else 'No'}")

    # Scenario 2: Stock unavailable case (warning logged)
    print("\n" + "-" * 45)
    print("Scenario: Stock Insufficiency Check")
    requested_large = 10
    print(f"Available Stock: {stock}")
    print(f"Requested Quantity: {requested_large}")
    is_available_large = check_stock(stock, requested_large)
    print(f"Stock Available: {'Yes' if is_available_large else 'No'}")

    # Scenario 3: Exception Handling demonstration (no crash)
    print("\n" + "-" * 45)
    print("Scenario: Exception Handling for Invalid Inputs")

    test_cases = [
        ("Negative Price", lambda: calculate_total_price(-1500, 2)),
        ("Invalid Type for Quantity", lambda: calculate_total_price(200, "three")),
        ("Discount > 100%", lambda: apply_discount(1000, 150)),
        ("Negative Requested Quantity", lambda: check_stock(10, -3)),
        ("Boolean Value Passed as Price", lambda: calculate_total_price(True, 5)),
    ]

    for label, action in test_cases:
        try:
            action()
        except (ValueError, TypeError) as err:
            print(
                f"Handled [{label}]: Successfully caught {type(err).__name__} -> {err}"
            )

    logger.info("=== Inventory Operation Completed Successfully ===")
    print("\n" + "=" * 45)
    print("Demonstration completed. Execution log saved to application.log")
    print("=" * 45)


if __name__ == "__main__":
    run_demonstration()
