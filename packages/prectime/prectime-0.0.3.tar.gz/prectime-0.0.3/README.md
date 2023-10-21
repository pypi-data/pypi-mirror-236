```
import prectime
import time
import io


@prectime.function
def request_far_away():
    # requesting to server...
    time.sleep(3)
    response = "Hello!"
    return response

response = request_far_away()
# stdout >>> request_far_away - 3.0004s

@prectime.function() # this works too
def request_not_far_away():
    # requesting to server...
    time.sleep(0.01)
    response = "Here!"
    return response


@prectime.methods
class BigCalculation(object):
    def pi(digits: int):
        time.sleep(digits // 100_000)
        return
    
    def matrix_mul(a, b):
        a_cols = len(a[0])
        a_rows = len(a)
        b_rows = len(b)
        o_n = a_cols * b_rows * a_rows
        time.sleep(o_n)
        return


pi = BigCalculation.pi(100_000)
# stdout >>> pi - 1.0005s
new_matrix = BigCalculation.matrix_mul([[1, 2], [3, 4]], [[1, 2], [3, 4]])
# stdout >>> matrix_mul - 8.0005s


def tetration(base, height):
    n = base
    for _ in range(height - 1):
        n = base ** n
    return n

with prectime.context("big number"):
    result = tetration(8, 3)
# stdout >>> big number - 0.3087s

# you can create own class to point (output, round_digits, format)
stream = io.StringIO()
my_measure = prectime.Measure(output=stream,
                              round_digits=1,
                              format="{name} --> {time} seconds\n")


with my_measure.context("test"):
    time.sleep(0.459)

# stream >>> test --> 0.5 seconds

@prectime.function(stream)
def last_example():
    return None and None

last_example()
# stream >>> last_example - 0.0s
```