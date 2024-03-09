import unittest
from abc import abstractmethod


class ScopeExtractorTestCase(unittest.TestCase):
    @abstractmethod
    def test_extract_headers_single_header(self):
        pass

    @abstractmethod
    def test_extract_blocks_single_block(self):
        pass

    @abstractmethod
    def test_extract_blocks_multiple_blocks(self):
        pass

    @abstractmethod
    def test_single_scope(self):
        pass