import heapq

class PriorityQueue:
    def __init__(self, items=None):
        self._heap = items if items is not None else []
        heapq.heapify(self._heap)

    def push(self, item):
        heapq.heappush(self._heap, item)

    def pop(self):
        return heapq.heappop(self._heap)

    def peek(self):
      return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def remove(self, neighbor):
        for i, (_, _, n) in enumerate(self._heap):
            if n == neighbor:
                del self._heap[i]
                heapq.heapify(self._heap)
                return

    def contains(self, val):
        return any(n == val for _, _, n in self._heap)

    def empty(self):
        return len(self._heap) == 0

    def to_string(self):
        output = ""
        for item in self._heap:
            output += str(item)
        return output