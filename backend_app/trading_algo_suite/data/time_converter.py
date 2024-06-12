from datetime import datetime, timezone, timedelta


def get_specific_time_iso8601(specific_time):
    # specific_time_utc = datetime(2024, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
    formatted_time = specific_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted_time


def get_current_time_iso8601():
    current_time_utc = datetime.now(timezone.utc)
    formatted_time = current_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted_time


def get_delta_delayed_time_iso8601(delayed_minutes):
    current_time_utc = datetime.now(timezone.utc)
    # Subtract minutes from the current time
    current_time_utc_minus_one_min = current_time_utc - timedelta(minutes=delayed_minutes)
    formatted_time = current_time_utc_minus_one_min.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted_time


if __name__ == "__main__":
    print("Formatted Date and Time:", get_current_time_iso8601())

    print("Formatted Date and Time:", get_delta_delayed_time_iso8601(1))

    specific_time_utc = datetime(2024, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
    print("Formatted Date and Time:", get_specific_time_iso8601(specific_time_utc))
