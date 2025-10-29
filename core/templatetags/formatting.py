from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

from django import template
register = template.Library()


def _coerce_decimal(value: Any) -> Decimal | None:
    """Attempt to coerce the input value to Decimal."""
    if value in (None, ''):
        return None
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


@register.filter
def _format_number(number: Decimal, decimal_places: int) -> str:
    """Return number formatted using Brazilian separators."""
    quantize_pattern = Decimal('1') if decimal_places == 0 else Decimal('1.' + '0' * decimal_places)
    quantized = number.quantize(quantize_pattern, rounding=ROUND_HALF_UP)
    formatted = f'{quantized:,.{decimal_places}f}'
    return formatted.replace(',', '\u00A6').replace('.', ',').replace('\u00A6', '.')


@register.filter
def currency_ptbr(value: Any) -> str:
    """
    Format numeric values using Brazilian currency style.

    Examples:
        12345.67 -> '12.345,67'
        None -> '0,00'
    """
    number = _coerce_decimal(value)
    if number is None:
        return '0,00'
    return _format_number(number, 2)


@register.filter
def decimal_ptbr(value: Any, decimal_places: int = 2) -> str:
    """
    Format numeric values with Brazilian decimal separators without currency prefix.

    Allows specifying decimal places, defaulting to 2.
    """
    number = _coerce_decimal(value)
    if number is None:
        return '0'
    try:
        decimal_places = int(decimal_places)
    except (TypeError, ValueError):
        decimal_places = 2
    if decimal_places < 0:
        decimal_places = 2

    return _format_number(number, decimal_places)


@register.filter
def currency_abbreviated(value: Any) -> str:
    """
    Format currency values with abbreviations for large numbers.

    Examples:
        999.99 -> 'R$ 999,99'
        1500.00 -> 'R$ 1,50 mil'
        1500000.00 -> 'R$ 1,50 mi'
        1500000000.00 -> 'R$ 1,50 bi'
        1500000000000.00 -> 'R$ 1,50 tri'
    """
    number = _coerce_decimal(value)
    if number is None:
        return 'R$ 0,00'

    # Get absolute value for comparison
    abs_number = abs(number)
    sign = '-' if number < 0 else ''

    # Define thresholds and suffixes
    if abs_number >= Decimal('1000000000000'):  # Trillion (trilhão)
        divided = abs_number / Decimal('1000000000000')
        formatted = _format_number(divided, 2)
        return f'{sign}R$ {formatted} tri'
    elif abs_number >= Decimal('1000000000'):  # Billion (bilhão)
        divided = abs_number / Decimal('1000000000')
        formatted = _format_number(divided, 2)
        return f'{sign}R$ {formatted} bi'
    elif abs_number >= Decimal('1000000'):  # Million (milhão)
        divided = abs_number / Decimal('1000000')
        formatted = _format_number(divided, 2)
        return f'{sign}R$ {formatted} mi'
    elif abs_number >= Decimal('1000'):  # Thousand (mil)
        divided = abs_number / Decimal('1000')
        formatted = _format_number(divided, 2)
        return f'{sign}R$ {formatted} mil'
    else:  # Less than 1000
        formatted = _format_number(abs_number, 2)
        return f'{sign}R$ {formatted}'
