import unittest

from redis import ResponseError
from conf_cases import get_client


cli = get_client()


class IndexCommandsTest(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName=methodName)
        self.dim = 5
        self.m = 32
        self.efconf = 200
        self.other_params = {}

    # unittest sort alphabetically
    def test_0_delete_noexist_index(self):
        with self.assertRaises(ResponseError) as re:
            cli.del_index("test")
        self.assertEqual(
            str(re.exception),
            'Index: usearch.test does not exist',
        )

    def test_1_get_nonexist_index(self):
        with self.assertRaises(ResponseError) as re:
            cli.get_index("test")
        self.assertEqual(
            str(re.exception),
            'Index: usearch.test does not exist',
        )

    def test_2_create_index(self):
        res = cli.create_index(
            "test",
            self.dim,
            self.m,
            efcon=self.efconf,
            **self.other_params
        )
        self.assertEqual(res, True)

    def test_3_get_exist_index(self):
        res = cli.get_index("test")
        self.assertEqual(res["dimensions"], self.dim)
        self.assertEqual(res["connectivity"], self.m)
        self.assertEqual(res["expansion_add"], self.efconf)

    def test_4_delete_exist_index(self):
        res = cli.del_index("test")
        self.assertEqual(res, 1)


if __name__ == "__main__":
    unittest.main()
    cli.close()
