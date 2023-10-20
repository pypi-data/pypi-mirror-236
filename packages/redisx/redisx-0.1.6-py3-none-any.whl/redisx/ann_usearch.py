from redisx import define
from typing import (Sequence, Tuple, Union)
from functools import reduce
from redis.typing import (CommandsProtocol)

VectorType = Sequence[Union[int, float]]


class TextVectorEncoder:
    SEP = bytes(",", "ascii")
    BITS = ("0", "1")

    @classmethod
    def vector_str(cls, vector: VectorType) -> bytes:
        """
        @return e.g: "0.1,0.0,0.2"
        """
        s = ",".join(["%f" % x for x in vector])
        return bytes(s, encoding="ascii")

    @classmethod
    def encode_with_square_brackets(cls, vector: VectorType, is_binary=False) -> bytes:
        s = ""
        if is_binary:
            s = "[" + ",".join([cls.BITS[x] for x in vector]) + "]"
        else:
            s = "[" + ",".join(["%f" % x for x in vector]) + "]"
        return bytes(s, encoding="ascii")  # ascii is enough

    @classmethod
    def decode_with_square_brackets(cls, buf: bytes) -> Tuple[float]:
        if buf[0] != ord("[") or buf[-1] != ord("]"):
            raise ValueError("invalid text vector value")
        is_int = True
        components = buf[1:-1].split(cls.SEP)
        for x in components:
            if not x.isdigit():
                is_int = False

        if is_int:
            return tuple(int(x) for x in components)
        return tuple(float(x) for x in components)


class UsearchVectorCommands(CommandsProtocol):

    def create_index(
        self,
        name: str,
        dim: int,
        m: int = 10,
        efcon: int = 128,
        metric: str = define.DistanceMetric.InnerProduct,
        quantization: str = define.UsearchQuantizationType.F32,
        **kwargs
    ):
        """
        create a index
        cmd eg: usearch.index.create idx0 dim 3 m 10 efcon 12 metric ip quantization f32
        """
        params = reduce(lambda x, y: x + y, kwargs.items(), ())
        return self.execute_command(
            define.CmdName.USEARCH_CREATE_INDEX,
            name,
            "dim",
            dim,
            "m",
            m,
            "efcon",
            efcon,
            "metric",
            metric,
            "quantization",
            quantization,
            *params
        )

    def get_index(self, name: str):
        """
        get the infomation of an index
        """
        return self.execute_command(
            define.CmdName.USEARCH_GET_INDEX,
            name
        )

    def del_index(self, name: str):
        """
        delete an index and all its data
        """
        return self.execute_command(
            define.CmdName.USEARCH_DEL_INDEX,
            name
        )

    def add_vector(
            self,
            index_name: str,
            name: str,
            vector: Union[VectorType, str],
    ):
        """
        add vector to index by name
        """
        if not isinstance(vector, str):
            vector = TextVectorEncoder.vector_str(vector)
        return self.execute_command(
            define.CmdName.USEARCH_ADD_NODE,
            index_name,
            name,
            vector
        )

    def add_vector_id(
            self,
            index_name: str,
            id: int,
            vector: Union[VectorType, str],
    ):
        """
        add vector to index by id
        """
        if not isinstance(vector, str):
            vector = TextVectorEncoder.vector_str(vector)
        return self.execute_command(
            define.CmdName.USEARCH_ADD_ID_NODE,
            index_name,
            id,
            vector
        )

    def get_vector(self, index_name: str, name: str):
        """
        get vector from index by name
        """
        return self.execute_command(
            define.CmdName.USEARCH_GET_NODE,
            index_name,
            name
        )

    def get_vector_id(self, index_name: str, id: int):
        """
        get vector from index by id
        """
        return self.execute_command(
            define.CmdName.USEARCH_GET_ID_NODE,
            index_name,
            id
        )

    def del_vector(self, index_name: str, name: str):
        """
        del vector from index by name
        """
        return self.execute_command(
            define.CmdName.USEARCH_DEL_NODE,
            index_name,
            name
        )

    def del_vector_id(self, index_name: str, id: int):
        """
        del vector from index by id
        """
        return self.execute_command(
            define.CmdName.USEARCH_DEL_ID_NODE,
            index_name,
            id
        )

    def kann_search(
        self,
        index_name: str,
        k: int,
        query_vector: Union[VectorType, str],
        **kwargs
    ):
        """
        KANN search from index by query vector
        cmd eg: usearch.search.kann idx0 6 0.0,0.0,0.0 "" ef_search 10
        """
        params = reduce(lambda x, y: x + y, kwargs.items(), ())
        if not isinstance(query_vector, str):
            query_vector = TextVectorEncoder.vector_str(query_vector)
        return self.execute_command(
            define.CmdName.USEARCH_SEARCH_KANN,
            index_name,
            k,
            query_vector,
            *params
        )
