from django import template

register = template.Library()

@register.filter
def remove_measurement(value):
    """
    Removes the measurement from the whiskey name.
    """
    if isinstance(value, str):
        # Split the string into words
        words = value.split()
        # Check if the last word is a measurement (e.g., "0.7L")
        if words[-1][-1] in {'L', 'ml'}:
            # If it is, remove it
            return ' '.join(words[:-1])
    # If no measurement is found or value is not a string, return the original value
    return value
