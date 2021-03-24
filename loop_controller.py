import time
import collections
import logging



class LoopController(object):


    # Buffer size in miliseconds
    def __init__(self, target_iter, buffer_size=1000):

        self._target_iter = target_iter
        self._sleep_time = 1 / target_iter

        # We can not calculate with a single element buffer, minimum buffer size is 2
        self._buffer_size = max(2,int((target_iter * buffer_size) / 1000))

        self._d = collections.deque([], maxlen=self._buffer_size)
        self._iter_counter = 0


    def registerIteration(self):
        # Get current timestamp
        self._d.append(time.time())

        # Increase iteration counter
        self._iter_counter += 1

        # We don't want to do the math every iteration
        if self._iter_counter == self._buffer_size:
            # Get iterations per second
            current_speed = self.getIterationSpeed()

            # Calculate iteration real work time.
            # This is the time the iteration spent doing something other than sleep
            it_time = (1/current_speed) - self._sleep_time

            # Calculate the new sleep time if we want to make the target
            # based on the previously calculated iteration time
            self._sleep_time = max(0,(1/self._target_iter) - it_time)
 
            # Increase iteration counter
            self._iter_counter = 0 

        # Sleep a bit
        time.sleep(self._sleep_time)


    # Get current iterations per second
    def getIterationSpeed(self):
        try:
            # First and last element difference is the time it took
            # to process (_buffer_size - 1) elements
            return (self._buffer_size-1)/(self._d[-1]-self._d[0])
        except ZeroDivisionError:
            return -1

