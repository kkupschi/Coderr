"""Helper functions for creating orders from offer details."""

from orders_app.models import Order


def create_order_from_detail(offer_detail, customer):
    """Create an order as a snapshot of the chosen detail package."""
    return Order.objects.create(
        customer_user=customer,
        business_user=offer_detail.offer.user,
        title=offer_detail.title,
        revisions=offer_detail.revisions,
        delivery_time_in_days=offer_detail.delivery_time_in_days,
        price=offer_detail.price,
        features=offer_detail.features,
        offer_type=offer_detail.offer_type,
    )
