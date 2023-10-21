from personnummer import personnummer
from personnummer.personnummer import PersonnummerException


def validate_ssn(ssn: str, country: str = "SE", fail_as_none: bool = False):
    """Validates SSN and normalizes it.

    Supports
        - SE, including coordination numbers
        dash and space are allowed as separators
        plus sign is for ssn over 100 years old

    Args:
        ssn (str): SSN to validate.
        country (str): Country code, ISO 3166-1 alpha-2.
            default: "SE"

    Returns:
        str or None: Normalized SSN.

    Raises:
        TypeError: If ssn is not a string.
        ValueError: If ssn is not a valid SSN.

    """
    if not isinstance(ssn, str):
        raise TypeError("ssn must be a string")
    if country == "SE":
        ssn = ssn.replace(" ", "")
        try:
            pn = personnummer.parse(ssn)
            if pn.valid():
                return pn.format(long_format=True)
        except PersonnummerException as e:
            if fail_as_none:
                return None
            else:
                raise ValueError(f"Invalid SSN: {ssn}") from e
    else:
        raise ValueError(f"Unsupported country: {country}")
