import time
import collections

SLEEP_STEP = 50           #sleep step in microseconds
DEFAULT_PRECISION = 0.01  #percentage over specified iterations per second, 0.1 means 10%

class LoopController(object):


    def __init__(self, iterations_ps, precision=DEFAULT_PRECISION):
        super()
        self._precision = precision
        self._iterations_ps = iterations_ps
        self._sleep_time = int(1000000 / iterations_ps)
        self._buffer_size = iterations_ps * 1 # we want a 1 seconds buffer

        self._d = collections.deque([], maxlen=self._buffer_size)

        self._iter_counter = 0


    def new_iteration(self):
        self._d.append(time.time())

        self._iter_counter += 1

        if self._iter_counter == self._buffer_size:
            # too fast, increase sleep time
            current_speed = self.getIterationSpeed()
            print("sending at: {0:.3f} msg/s".format(current_speed))
            #print(self._sleep_time)
            if current_speed > self._iterations_ps * (1 + self._precision):
                self._sleep_time += SLEEP_STEP
            elif current_speed < self._iterations_ps * (1 - self._precision):
                self._sleep_time -= SLEEP_STEP

            self._iter_counter = 0
 

        print('sleeping {}'.format(str(self._sleep_time)))
        time.sleep(self._sleep_time/1000000)


    def getIterationSpeed(self):
        try:
            return (self._buffer_size-1)/(self._d[-1]-self._d[0])
        except ZeroDivisionError:
            return -1

