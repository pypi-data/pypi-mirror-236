from ..utils.text_to_latex  import conversion_functions



def converter(data: dict):
    conversion_func = conversion_functions.get(type)
    if conversion_func:
        return conversion_func(data)
    else:
        raise ValueError(f"No conversion function for type {type} found.")
