import csv
import unittest


# Memory lookup. This is a simulation of looking up an address in
# memory. The "memory" is provided by an array.
class Memory:
    def __init__(self, data):
        self.memory = data
        self.memory_hit_count = 0

    def get_memory_hit_count(self):
        return self.memory_hit_count

    def name(self):
        return "Memory"

    # This implementation is provided as a stub for a memory
    # access. Do not make assumptions about the implementation
    # here. Your code may be evaluated against a different
    # implementation. All you should assume is that making a call to
    # lookup will provide an answer and that the memory will keep
    # track of the number of hits that are made.
    #
    # If presented with an unknown memory address, the class will
    # return None.
    def lookup(self, address):
        # This one actually has no cache, so every lookup requires a
        # memory hit. Do not make assumptions about the implementation
        # of this method. Your code may be tested against an
        # implementation that operates in a different way. You should
        # only assume that the interface remains the same.
        self.memory_hit_count += 1
        try:
            return self.memory[address]
        except IndexError as error:
            print("Error: Unknown memory location")
            return None


# Tests
class TestMemory(unittest.TestCase):
    # Construct some test data that just has 0,...,100
    def sample_data(self):
        return list(range(0, 100))

    def test_one(self):
        memory = Memory(self.sample_data())
        self.assertEqual(memory.get_memory_hit_count(), 0)

    def test_two(self):
        memory = Memory(self.sample_data())
        self.assertEqual(memory.lookup(0), 0)

    def test_three(self):
        iterations = 10
        memory = Memory(self.sample_data())
        for x in range(0, iterations):
            self.assertEqual(memory.lookup(x), x)
        self.assertEqual(memory.get_memory_hit_count(), iterations)

    def test_four(self):
        iterations = 10
        memory = Memory(self.sample_data())
        for x in range(0, iterations):
            memory.lookup(0)
        self.assertEqual(memory.get_memory_hit_count(), iterations)

    def test_five(self):
        memory = Memory(self.sample_data())
        self.assertIsNone(memory.lookup(100))
