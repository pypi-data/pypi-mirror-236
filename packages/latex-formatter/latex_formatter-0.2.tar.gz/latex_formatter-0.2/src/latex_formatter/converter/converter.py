from ..utils.text_to_latex  import conversion_functions
from ..utils import transfer_to_dict
from ujson import JSONDecodeError


def converter(data: dict):


    try:
        content_dict = transfer_to_dict(data)
    except (JSONDecodeError):
        print("load err")
        print(type(data))
        return data
    te = content_dict["caption"] if "caption" in content_dict else content_dict
    

    types = (te['type'])
    try:
        conversion_func = conversion_functions.get(types)

        if conversion_func:
            # maybe \\newline
            return conversion_func(te).replace("[br]", "\n")
        else:
            
            raise ValueError(f"No conversion function for type {types} found.")
    except Exception as e:
         print(f"data is {data}, {type(data)}")
         print(e)



