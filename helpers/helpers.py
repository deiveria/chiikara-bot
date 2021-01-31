from datetime import timezone

# Converter o horário pro fuso do Brasil
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)