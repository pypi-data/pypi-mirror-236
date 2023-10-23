from typing import Union, Dict
import ujson


def transfer_to_dict(data: Union[Dict, str]):
    if isinstance(data, Dict):
        return data
    return ujson.loads(data)