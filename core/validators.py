"""Shared helpers for validating untrusted request input.

Query parameters and request bodies arrive as strings. Passing them straight
into a queryset lets Django raise ValueError, which surfaces as a 500 error.
These helpers reject bad input with a 400 response instead.
"""

from decimal import Decimal, InvalidOperation

from rest_framework.exceptions import ValidationError


def parse_int(value, field_name):
    """Return value as int, or raise a 400 error naming the field."""
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError({field_name: 'A valid integer is required.'})


def parse_decimal(value, field_name):
    """Return value as Decimal, or raise a 400 error naming the field."""
    try:
        number = Decimal(value)
    except (TypeError, ValueError, InvalidOperation):
        raise ValidationError({field_name: 'A valid number is required.'})
    if not number.is_finite():
        raise ValidationError({field_name: 'A valid number is required.'})
    return number
