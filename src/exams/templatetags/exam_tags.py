from django import template

register = template.Library()


@register.filter
def duration(seconds):
    """Format seconds as `12m 05s` (or `45s`)."""
    seconds = int(seconds or 0)
    minutes, secs = divmod(seconds, 60)
    if not minutes:
        return f'{secs}s'
    return f'{minutes}m {secs:02d}s'


@register.filter
def letter(index):
    return 'ABCDE'[index] if 0 <= index < 5 else '?'


@register.filter
def marks(value):
    """Decimal score without trailing zeros: 61.75, 62, -1.5."""
    text = f'{value:.2f}'.rstrip('0').rstrip('.')
    return '0' if text == '-0' else text


@register.filter
def ring(pct, circumference=289.03):
    """stroke-dasharray for an SVG score ring of radius 46."""
    filled = max(0.0, min(100.0, float(pct))) * circumference / 100
    return f'{filled:.2f} {circumference}'
