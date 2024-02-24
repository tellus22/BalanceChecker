def toDecimals(amount, decimals, precision):
    return round((amount / 10 ** decimals), precision)


def fromDecimals(amount, decimals, precision):
    return round((amount * 10 ** decimals), precision)
