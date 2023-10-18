"""
idx.py
"""
from intervaltree import IntervalTree, Interval


class Idx:
    """
    Idx
    """

    def __init__(self):
        self.idx = IntervalTree()
        self.tree = self.idx

    def get_entries(self):
        """method"""
        return self.idx.items()

    def insert(self, *args):
        """
        insert
        """
        if len(args) == 1 and isinstance(args[0], Interval):
            interval = args[0]
            self.idx.add(interval)
        elif len(args) == 2:
            begin, end = args
            self.idx.addi(begin, end, {})
        elif len(args) == 3:
            begin, end, data = args
            self.idx.addi(begin, end, data)
        else:
            raise ValueError("Invalid arguments")

    def get_intervals_contained_by(self, *args):
        """method"""
        return self.idx.envelop(*args)

    def get_intervals_containing(self, *args):
        """
        intervaltree doesn't have a direct query for intervals contained
        by some interval. Instead first get all intervals that overlap
        with the query, and filter the results where the query is completely
        contained. This is still efficient
        """
        
        # Check if the first argument is an instance of Interval
        if isinstance(args[0], Interval):
            query_interval = args[0]
        else:
            query_interval = Interval(*args)

        # Return query results
        return [
            interval
            for interval in self.idx.overlap(*args)
            if interval.contains_interval(query_interval)
        ]

