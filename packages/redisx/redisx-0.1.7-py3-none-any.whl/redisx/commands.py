from typing import Dict, Union

from redisx import ann_usearch
from redisx import define

from redis._parsers.helpers import (
    bool_ok,
    pairs_to_dict,
    parse_list_of_dicts,
)
from redis import Redis
from redis.asyncio import Redis as AsyncRedis


# just a commands class set for extend
class RedisXCommands(
    ann_usearch.UsearchVectorCommands,
):
    pass


def int_or_none(response):
    if response is None:
        return None
    return int(response)


def parse_usearch_get_index_result(resp) -> Union[Dict, None]:
    if len(resp) == 0:
        return None
    return pairs_to_dict(resp, decode_keys=True, decode_string_values=True)


def parse_usearch_get_node_result(resp) -> Union[Dict, None]:
    if len(resp) == 0:
        return None
    return pairs_to_dict(resp, decode_keys=True, decode_string_values=True)


def parse_usearch_kann_search_result(resp) -> Union[Dict, None]:
    if len(resp) == 1:
        return {"size": int(resp[0]), "vals": None}
    if len(resp) > 1:
        vals = []
        for item in resp[1:]:
            vals.append(pairs_to_dict(
                item, decode_keys=True, decode_string_values=True))
        return {"size": int(resp[0]), "vals": vals}
    return None


REDISX_RESPONSE_CALLBACKS = {
    # RedisXANN Usearch Vector
    define.CmdName.USEARCH_CREATE_INDEX: bool_ok,
    define.CmdName.USEARCH_GET_INDEX: parse_usearch_get_index_result,
    define.CmdName.USEARCH_DEL_INDEX: int_or_none,
    define.CmdName.USEARCH_ADD_NODE: bool_ok,
    define.CmdName.USEARCH_GET_NODE: parse_usearch_get_node_result,
    define.CmdName.USEARCH_DEL_NODE: int_or_none,
    define.CmdName.USEARCH_ADD_ID_NODE: bool_ok,
    define.CmdName.USEARCH_GET_ID_NODE: parse_usearch_get_node_result,
    define.CmdName.USEARCH_DEL_ID_NODE: int_or_none,
    define.CmdName.USEARCH_SEARCH_KANN: parse_usearch_kann_search_result,
}


def set_response_callback(redis: Union[Redis, AsyncRedis]):
    for cmd, cb in REDISX_RESPONSE_CALLBACKS.items():
        redis.set_response_callback(cmd, cb)
