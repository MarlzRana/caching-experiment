import time
from memory import Memory
import utilities


class CyclicCache(Memory):
    def name(self):
        return "Cyclic"

    # Edit the code below to provide an implementation of a cache that
    # uses a cyclic caching strategy with a cache size of 4. You can
    # use additional methods and variables as you see fit as long as
    # you provide a suitable overridding of the lookup method.

    def __init__(self, data, size=4):
        self.cache_memory = [{"address": None, "data": None} for n in range(0, size)]
        self.cache_size = size
        self.cache_next_item_number = 1
        super().__init__(data)

    def lookup(self, address):
        # Check if we have the corresponding data for the the address in catch
        # We are trying to catch the memory request
        for dict in self.cache_memory:
            if dict["address"] == address:
                return dict["data"]

        # If we weren't able to "catch the memory address" we will fetch the value for the corresponding address and store it cache with it's respective address and return it

        # If the the cache_next_item_number is greater than the cache_size it must be pointing at an item that does not exist, hence "we cycle back to the start"
        if self.cache_next_item_number > self.cache_size:
            self.cache_next_item_number = 1
        # Fetch the data in that particular address from memory
        data_in_address = super().lookup(address)
        # Append the address and data to the cache's record
        self.cache_memory[self.cache_next_item_number - 1] = {
            "address": address,
            "data": data_in_address,
        }
        # Append the cache_next_item_number to point to the next item as we have just added an item to where it was pointing
        self.cache_next_item_number += 1
        # Return the data_in_address to serve the lookup
        return data_in_address


class LRUCache(Memory):
    def name(self):
        return "LRU"

    # Edit the code below to provide an implementation of a cache that
    # uses a least recently used caching strategy with a cache size of
    # 4. You can use additional methods and variables as you see fit as
    # long as you provide a suitable overridding of the lookup method.

    def __init__(self, data, size=4):
        self.cache_memory = {}
        self.cache_size = size
        super().__init__(data)

    def lookup(self, address):
        # Check if we have the value in the cache
        if address in self.cache_memory:
            # Update the time of last access
            self.cache_memory[address]["timeOfLastAccess"] = time.time()
            # Return the data for the particular address in cache to service the lookup
            return self.cache_memory[address]["data"]

        # If we could not find the value is cache, add it to the cache and if the cache is full when we are trying to add a "record/value" evict the LeastRecentlyUsed "record/value"

        # If the cache is full, evict the least recently used page
        least_recently_used_memory_address_in_cache = -1
        if len(self.cache_memory) >= self.cache_size:
            # Find the least_recently_used_memory_address_in_cache
            arrOfTimes = []
            for cache_address in self.cache_memory:
                arrOfTimes.append(self.cache_memory[cache_address]["timeOfLastAccess"])
            # Evict the least recently used "record"
            lowestTime = min(arrOfTimes)
            address_of_record_to_evict = -1
            for cache_address in self.cache_memory:
                if self.cache_memory[cache_address]["timeOfLastAccess"] == lowestTime:
                    address_of_record_to_evict = cache_address
            self.cache_memory.pop(address_of_record_to_evict)
        # Add the "record" to cache
        data_in_address = super().lookup(address)
        self.cache_memory[address] = {
            "timeOfLastAccess": time.time(),
            "data": data_in_address,
        }

        return data_in_address
