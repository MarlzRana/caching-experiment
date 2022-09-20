# Exercise: Caching Simulation

This exercise asks you to explore different caching strategies.

The exercise involves implementation of a cache that stores the
results of memory lookups, with the aim of reducing the number of
lookups that are needed during a sequence of memory accesses.

The exercise is *formative*. There is no submission expected, it is
not marked, and does not contribute towards the unit mark. We strongly
recommend that you do the exercise though. It should help your
understanding of caching strategies, and also gives some practice
in python implementation and the use of unit testing.

We have a simple simulation of memory. A memory lookup takes a
location, here modelled as an integer, and returns some data, here
modelled as a string of hex digits.

In the implementation, memory is simulated by an array, which is
passed in to the constructor of a ```Memory``` object. Lookups
will then look in this array to determine the "values" that are held
at a particular location. You should make no assumptions about the
content of this array or the ways in which locations map to elements
of the array.

The memory class provides a ```lookup``` function. This takes a memory
location (an address) and returns the data that is at that
address. A count is kept of each memory "hit" (i.e. each time we call
the lookup on the memory object).

A cache can help to reduce the number of times we need to access
memory. If the contents of a memory location have been cached, then we
can return the result without needing to go to memory for the lookup.

You are given the following files:

* ```memory.py``` Memory simulation. Defines a class ```Memory```.
* ```cache.py``` Within this file there are two classes defined: ```CyclicCache``` and ```LRUCache```.
* ```utilities.py``` Utilities including creation of sample "memory". 
* ```test.py``` Sample unit tests 
* ```harness.py``` Sample driver file 

There are some useful functions defined in ```utilities.py``` that
will generate some sample memory data. These are used in the harness. 

## Running the code

There is some simple harness code that will allow you to inspect the results of running
your implementation. It takes a list of memory locations from `stdin`
and uses those to test the caching implementation.

For example, try running:

```
user@computer> python3 harness.py < in-10.txt
```

This will use the default Memory implementation and should result in
something like the following:

```
user@computer> python3 harness.py < in-10.txt 
001, 0, eccbc87e
002, 1, c81e728d
003, 2, c4ca4238
004, 3, cfcd2084
005, 4, 8f14e45f
006, 5, 1679091c
007, 4, 8f14e45f
008, 6, e4da3b7f
009, 1, c81e728d
010, 2, c4ca4238
Model: Memory
010 Accesses
010 Memory Hits
```

This is reporting that in step ```001```, location ```0``` was
accessed, returning ```eccbc87e```. In step ```002```, location
```1``` was accessed, returning ```c81e728d```. In step ```009```,
location ```1``` was accessed, again returning the value
```c81e728d```. In this case, in total there were ```10``` memory
accesses. There is no caching, so every request will result in a
memory access. 

To use an alternative strategy, try:

```
user@computer> python3 harness.py -s LRU < in-10.txt
```

This will use the LRU implementation. Note that in the skeleton code
given, this will give the ***same answers*** as using the ```Memory```
strategy as the method has not (yet) been overridden. That's your
task!

## Testing

A few simple tests are defined in ```test.py```. You can run them using:

```python test.py```

The code uses python's ```unittest``` framework to run tests against
the code. Unit testing is a common mechanism that's used in software
engineering to test the component parts of a system before
integration.

There is comprehensive documentation on the ```unittest``` framework
here:

<https://docs.python.org/3/library/unittest.html>

In brief, a unit test is defined as a class with a ```setUp()```
method that performs some initialisation. A ```tearDown()``` method
may also be used to clean up resources -- this is not used in these
simple examples. A hierarchy of test cases can be defined, allowing
for generic setup code.

By default, test methods are then defined in a class with the prefix
```test```. The naming convention allows the test runner to determine
which methods should be run as tests. There are other, more
sophisticated mechanisms that can be used to define tests, but this
suffices for our particular example. Within a test, methods such as
```assertEquals()``` are used to make assertions about the expected
results. For example, an assertion

```
assertEquals(someValue,0)
```

will **fail** if someValue is not equal to 0. 

Note that some of these tests are designed to **fail** on the given
code skeletons. For example, in the ```CachingOneTestCase```,
```test_cyclic``` performs the following on the ```CyclicCache```
implementation:

1. a call to ```lookup(0)```, requesting the contents of memory
  location 0. As the cache has just been initialised and will be
  empty, this should require a memory hit in order to retrieve the
  data which can then be cached.
1. another call to ```lookup(0)```. If the cache is working properly,
  this should now result in a cache hit, and no increment to the
  ```memory_hit_count```. With the stub implementation given there is
  no caching, so the memory hit count will be incremented and the test
  will fail.

If you provide a correct implementation for the cache, this test
should then pass. This is a rather simple example of *test driven
development* -- the tests have been defined before development
takes place, and can be used to repeatedly track progress as code is written. 

There are other tests that will check that code is running
correctly. These tests are in no way comprehensive and we recommend
that you develop your own tests, either using the ```unittest```
framework or hand-crafted cases. Share them with your
colleagues. Treat this as a challenge: can you design a test that will
expose an error in someone else's code?

## The Task

The task is to override the implementation of the
```lookup(address)``` operation which takes an address ```n``` and
returns the value at address ```n```. The operation should use the
appropriate caching strategy to minimise memory accesses. Note that
each entry in the cache thus stores an association between an address
and the data that was stored at that address. 

Your implementation of the caches shouldn't make assumptions about the
implementation of ```lookup()``` in the ```memory.py``` class. Nor
should it copy code from the implementation of ```lookup()```. If your
implementation needs to call the lookup method on the ```Memory```
class (for example because a value is not found in the cache), it
should do this through a call to ```super().lookup```. Your code may
eventually be run or tested against a **different** implementation of
```memory.py```. In order to simplify the exercise, there is no need
to check if the cache has been invalidated or worry about flushing the
cache -- you can assume that calls to the memory lookup will always
return the same answer (and thus if it's in the cache it's safe to use
the cached value). Note that you shouldn't be changing the value of
```memory_hit_count``` in the cache implementations. This is taken
care of in memory.

Implement solutions using:

1. a Cyclic strategy.
   * Assume slots ```1,...,N``` in the cache.
   * Keep track of the next slot in the cache to be used (starting
     with ```1```).
   * When an value is cached, we increment our count to use the next
   slot.
   * Once all slots have been filled, go back to slot ```1``` and
     cycle round. 
2. an LRU strategy.
   * Assume ```N``` slots.
   * Keep track of how recently each slot has been used (accessed or stored).
   * If the cache is full and a new value needs to be stored, we
     remove the entry from the slot that was least recently used and replace with
     the new value.

The cache should be of size **N=4**.

Each of these strategies should be implemented in the appropriate
class.

Don't make any changes to the implementation of ```memory.py```. Nor
should you make any assumptions about the results that ```memory.py```
returns. Your code may run against an implementation of
```memory.py``` that has the same interface, but a different
implementation.

We recommend that your code conforms to
[PEP8](https://www.python.org/dev/peps/pep-0008/) guidelines. You can
use [pycodestyle](https://pypi.org/project/pycodestyle/) to check
this.

## Stretch Goals

Think about other strategies that could be used in the
implementation. For example a *Random* strategy will evict a random
entry from the cache if we need to cache a new value.How would you
test such a thing?

Another possibility might be *Least Frequently Used*, where a count of
cache hits is kept and the entry with the lowest count is evicted.

See <https://en.wikipedia.org/wiki/Cache_replacement_policies> for a
list of possible eviction algorithms. 

Alternative strategies may then be useful for the caching experiment,
which will form an assessed exercise.


