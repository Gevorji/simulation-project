import sys
from map import Map

sys.path.insert(1, r'../')

test_cases = (((0, 0), (2, 2)),
              ((0, 0), (0, 9)),
              ((0, 0), (9, 0)),
              ((9, 9),),
              ((0, 0), (0, 0))
              )

if __name__ == '__main__':

    m = Map(10, 10)
    for test in test_cases:
        l = [f'{c.x}, {c.y}' for c in m.field_iterator(*test, return_contents=False)]
        print(f'{l} length: {len(l)}')
