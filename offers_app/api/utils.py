"""Helper functions for aggregating offer detail values."""


def get_min_price(offer):
    """Return the lowest price across all detail packages of an offer."""
    prices = [detail.price for detail in offer.details.all()]
    return min(prices) if prices else None


def get_min_delivery_time(offer):
    """Return the shortest delivery time across all detail packages."""
    times = [detail.delivery_time_in_days for detail in offer.details.all()]
    return min(times) if times else None
