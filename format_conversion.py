import re
from datetime import datetime,timedelta

def iso8601_to_microseconds(iso_string):
    # Regex to parse ISO 8601 format
    pattern = r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(?:Z|([+-]\d{2}):?(\d{2}))?"
    match = re.match(pattern, iso_string)
    
    if not match:
        raise ValueError("Invalid ISO 8601 format")
    
    # Extract components
    year, month, day = map(int, match.group(1, 2, 3))
    hour, minute, second = map(int, match.group(4, 5, 6))
    microsecond = int(match.group(7) or 0)  # Default to 0 if no fractional seconds
    tz_sign = match.group(8)
    tz_hour = int(match.group(9) or 0) if tz_sign else 0
    tz_minute = int(match.group(10) or 0) if tz_sign else 0
    
    # Create naive datetime object
    dt = datetime(year, month, day, hour, minute, second, microsecond)
    
    # Adjust for timezone offset if present
    if tz_sign:
        offset = timedelta(hours=tz_hour, minutes=tz_minute)
        if tz_sign.startswith('-'):
            dt += offset
        else:
            dt -= offset
    
    # Convert to microseconds since epoch
    epoch = datetime(1970, 1, 1)
    delta = dt - epoch
    return int(delta.total_seconds() * 1_000_000 + delta.microseconds)

def microseconds_to_iso8601(microseconds_str):
    microseconds = int(microseconds_str)
    epoch = datetime(1970, 1, 1)
    dt = epoch + timedelta(microseconds=microseconds)
    return dt.isoformat()[:19] + 'Z'