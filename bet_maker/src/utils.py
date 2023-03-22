from decimal import Decimal


def reformat_num(num_obj, digits=0):
    return Decimal(f"{num_obj:.{digits}f}")
