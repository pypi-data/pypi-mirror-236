import pytest
from redis.exceptions import RedisClusterException
from redisx import Client, ClusterClient


class TestPipeline:
    def test_pipeline_is_true(self, uc: Client):
        with uc.pipeline() as pipe:
            assert pipe

    def test_deprecated(self, cc: ClusterClient):
        with pytest.raises(RedisClusterException):
            cc.pipeline(transaction=True)
        with pytest.raises(RedisClusterException):

            cc.pipeline(shard_hint=True)


if __name__ == '__main__':
    pytest.main()
