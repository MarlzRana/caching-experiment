from memory import Memory
from cache import CyclicCache, LRUCache
import utilities
import unittest

# A collection of basic unit tests for caching.

# Stop unittest printing traces out. Uncomment this line if you want
# to see trace information
__unittest = True

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        data = utilities.sample_data(size=100)
        # This test suite assumes that the cache is of size
        # 4. Changing this may result in some tests failing.
        self.memory = Memory(data)
        self.cyclic = CyclicCache(data, size=4)
        self.lru = LRUCache(data, size=4)


# Unit tests
class LookupTestCase(BasicTestCase):

    # Simple lookup comparisons. The results of looking up a location
    # twice should be the same
    def lookup_check(self, impl, location):
        # Lookup location 0
        datum_1 = impl.lookup(location)
        # Lookup location 1
        datum_2 = impl.lookup(location)
        # The two results should be equal
        self.assertEqual(datum_1, datum_2)

    # Memory
    def test_memory(self):
        self.lookup_check(self.memory, 0)
        self.lookup_check(self.memory, 10)

    # Cyclic
    def test_cyclic(self):
        self.lookup_check(self.cyclic, 0)
        self.lookup_check(self.cyclic, 10)

    # LRU
    def test_lru(self):
        self.lookup_check(self.lru, 0)
        self.lookup_check(self.lru, 10)


class CachingOneTestCase(BasicTestCase):

    # Lookup the same location twice and check the hit count
    def caching_check(self, impl, diff):
        # Warm up and fill the cache.
        for loc in [10, 11, 12, 13]:
            impl.lookup(loc)

        # Lookup location 1
        datum_1 = impl.lookup(1)
        hits_1 = impl.get_memory_hit_count()

        # Lookup location 1
        datum_2 = impl.lookup(1)
        hits_2 = impl.get_memory_hit_count()
        # If the cache is working, then the hit count should have
        # changed by the given amount
        self.assertEqual(hits_1+diff, hits_2)

    # Memory. Hit count should increase by 1
    def test_memory(self):
        self.caching_check(self.memory, 1)

    # Cyclic. Hit count should not increase as the cache should be used.
    def test_cyclic(self):
        self.caching_check(self.cyclic, 0)

    # LRU. Hit count should not increase as the cache should be used
    def test_lru(self):
        self.caching_check(self.lru, 0)


class CachingTwoTestCase(BasicTestCase):

    # Here we look up four items, then request the first one again.
    # Then check the hit counts.
    def caching_check(self, impl, diff):
        # Warm up and fill the cache.
        for loc in [10, 11, 12, 13]:
            impl.lookup(loc)

        # Look up 4 items
        datum_1 = impl.lookup(1)
        datum_2 = impl.lookup(2)
        datum_3 = impl.lookup(3)
        datum_4 = impl.lookup(4)
        hits_1 = impl.get_memory_hit_count()
        datum_5 = impl.lookup(1)
        hits_2 = impl.get_memory_hit_count()
        # Data should be the same
        self.assertEqual(datum_1, datum_5)
        # If the cache is working, then the hit count should have
        # changed by the given amount
        self.assertEqual(hits_1+diff, hits_2)

    # Memory. Hit count should increase by 1
    def test_memory(self):
        self.caching_check(self.memory, 1)

    # Cyclic. Hit count should not increase as the cache should be used.
    def test_cyclic(self):
        self.caching_check(self.cyclic, 0)

    # LRU. Hit count should not increase as the cache should be used.
    def test_lru(self):
        self.caching_check(self.lru, 0)


class CachingThreeTestCase(BasicTestCase):

    # Here we look up four items, then request a different one.
    # Then check the hit counts
    def caching_check(self, impl, diff):
        # Warm up and fill the cache.
        for loc in [10, 11, 12, 13]:
            impl.lookup(loc)
        # Look up 4 items
        datum_1 = impl.lookup(1)
        datum_2 = impl.lookup(2)
        datum_3 = impl.lookup(3)
        datum_4 = impl.lookup(4)
        hits_1 = impl.get_memory_hit_count()
        datum_5 = impl.lookup(5)
        hits_2 = impl.get_memory_hit_count()
        # If the cache is working, then the hit count should have
        # changed by the given amount
        self.assertEqual(hits_1+diff, hits_2)

    # Memory. Hit count should increase by 1
    def test_memory(self):
        self.caching_check(self.memory, 1)

    # Cyclic. Hit count should increase by 1
    def test_cyclic(self):
        self.caching_check(self.cyclic, 1)

    # LRU. Hit count should increase by 1
    def test_lru(self):
        self.caching_check(self.lru, 1)


class CachingSequenceTestCase(BasicTestCase):

    # Generic test structure. The cache is warmed up, then the given
    # sequence of locations are requested. This should result in the
    # given number of hits.
    def caching_check(self, impl, sequence, diff):
        # Warm up and fill the cache.
        for loc in [10, 11, 12, 13]:
            impl.lookup(loc)
        hits_1 = impl.get_memory_hit_count()

        # Sequence of lookups
        for loc in sequence:
            impl.lookup(loc)
        hits_2 = impl.get_memory_hit_count()
        # If the cache is working, then the hit count should have
        # changed by the given amount
        self.assertEqual(hits_1+diff, hits_2)


class CachingFourTestCase(CachingSequenceTestCase):

    # Memory
    def test_memory(self):
        # Should result in 7 additional memory hits for memory
        self.caching_check(self.memory, [1, 2, 3, 4, 1, 5, 1], 7)

    # Cyclic
    def test_cyclic(self):
        # Should result in 6 additional memory hits for cyclic. When 5
        # is requested, 1 is evicted, resulting in an additional
        # memory hit for the final access.
        self.caching_check(self.cyclic, [1, 2, 3, 4, 1, 5, 1], 6)

    # LRU
    def test_lru(self):
        # Should result in 5 additional memory hits for cyclic
        self.caching_check(self.lru, [1, 2, 3, 4, 1, 5, 1], 5)


class CachingFiveTestCase(CachingSequenceTestCase):

    # Memory
    def test_memory(self):
        # Should result in 9 additional memory hits for memory
        self.caching_check(self.memory, [1, 2, 3, 4, 5, 5, 2, 6, 3], 9)

    # Cyclic
    def test_cyclic(self):
        # Should result in 6 additional memory hits for cyclic
        self.caching_check(self.cyclic, [1, 2, 3, 4, 5, 5, 2, 6, 3], 6)

    # LRU
    def test_lru(self):
        # Should result in 7 additional memory hits for lru. When 6 is
        # requested, 3 will be evicted resulting in a memory hit for
        # the final access.
        self.caching_check(self.lru, [1, 2, 3, 4, 5, 5, 2, 6, 3], 7)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(LookupTestCase('test_memory'))
    suite.addTest(LookupTestCase('test_cyclic'))
    suite.addTest(LookupTestCase('test_lru'))
    suite.addTest(CachingOneTestCase('test_memory'))
    suite.addTest(CachingOneTestCase('test_cyclic'))
    suite.addTest(CachingOneTestCase('test_lru'))
    suite.addTest(CachingTwoTestCase('test_memory'))
    suite.addTest(CachingTwoTestCase('test_cyclic'))
    suite.addTest(CachingTwoTestCase('test_lru'))
    suite.addTest(CachingThreeTestCase('test_memory'))
    suite.addTest(CachingThreeTestCase('test_cyclic'))
    suite.addTest(CachingThreeTestCase('test_lru'))
    suite.addTest(CachingFourTestCase('test_memory'))
    suite.addTest(CachingFourTestCase('test_cyclic'))
    suite.addTest(CachingFourTestCase('test_lru'))
    suite.addTest(CachingFiveTestCase('test_memory'))
    suite.addTest(CachingFiveTestCase('test_cyclic'))
    suite.addTest(CachingFourTestCase('test_lru'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
