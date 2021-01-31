from discord import Embed
from datetime import timezone


# Converter o horário pro fuso do Brasil
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def info_embed(text, level="sucess"):

    colours = {
        "sucess": 0x3FFC7E,
        "info": 0x7BB9FB,
        "error": 0xFF7D70,
        "warning": 0xEFFA80,
    }

    return Embed(description=text, colour=colours[level])
