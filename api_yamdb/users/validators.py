import re

from django.core.exceptions import ValidationError


class ValidateUsername:
    """Username validators."""

    def validate_username(self, username):
        pattern = re.compile(r'^[\w.@+-]+\Z')
        symbols_forbidden = re.sub(pattern, '', username)
        if symbols_forbidden:
            symbols = ", ".join(symbols_forbidden)
            raise ValidationError(
                f'Forbidden symbols: {symbols}'
            )
        if username == 'me':
            raise ValidationError(
                f'{username} is not allowed'
            )
        return username
