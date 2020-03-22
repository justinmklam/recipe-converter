"""
Main Script Sample
====================

Just a test to make sure Sphinx Docs works

"""


from loguru import logger


def add(a: int, b: int) -> int:
    """Add two numbers together

    Args:
        a (int): Number 1
        b (int): Number 2

    Returns:
        int: Sum of both numbers
    """
    logger.debug(f"Adding {a} and {b}")
    return a + b


def divide(a: int, b: int) -> float:
    """Divide two numbers

    Args:
        a (int): Number 1
        b (int): Number 2

    Returns:
        int: Sum of both numbers
    """
    logger.debug(f"Dividing {a} and {b}")
    return a / b


if __name__ == "__main__":
    logger.info(f"Executing {__file__}")
    result1 = add(1, 2)
    logger.info(f"Added: {result1}")
    result2 = divide(1, 2)
    logger.info(f"Divided: {result2}")
    logger.warning("Finished already?")
