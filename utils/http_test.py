# coding=utf-8

# 单元测试相关部分


import unittest
import http


class TestHttp(unittest.TestCase):
    httpObj = None

    def setUp(self):
        self.httpObj = http.Http();

    def tearDown(self):
        pass

    def test_init(self):
        pass

    def test_Add_Remove_RequestInterceptor(self):
        index = self.httpObj.addRequestInterceptor(lambda x: x)
        self.assertEqual(index, 0)
        index = self.httpObj.addRequestInterceptor(lambda x: x)
        self.assertEqual(index, 1)
        self.httpObj.removeRequestInterceptor(1)
        self.assertEqual(self.httpObj.requestInterceptor.__len__(), 1)
        self.httpObj.removeRequestInterceptor(0)
        self.assertEqual(self.httpObj.responseInterceptor, [])

    def test_Add_Remove_ResponseInterceptor(self):
        index = self.httpObj.addResponseInterceptor(lambda x: x)
        self.assertEqual(index, 0)
        index = self.httpObj.addResponseInterceptor(lambda x: x)
        self.assertEqual(index, 1)
        self.httpObj.removeResponseInterceptor(1)
        self.assertEqual(self.httpObj.responseInterceptor.__len__(), 1)
        self.httpObj.removeResponseInterceptor(0)
        self.assertEqual(self.httpObj.responseInterceptor, [])


if __name__ == '__main__':
    unittest.main()
