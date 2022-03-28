from PyInquirer import ValidationError, Validator


class NumberValidator(Validator):
    def validate(self, document: str) -> None:
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))
