import numpy as np
import heapq

class TermOrder(object):
    '''
    Allows an ordering on tuples according to grevlex 
    Used in making the heap object, to pop off the max monomial
    '''
    def __init__(self,tuple_val):
        self.val = tuple_val

    def __str__(self):
        return str(self.val)

    def __lt__(self, other):
        '''
        '''
        if sum(self.val) < sum(other.val):
            return True
        elif sum(self.val) > sum(other.val):
            return False
        else:
            for i,j in zip(self.val,other.val):
                if i<j:
                    return True
                if i > j:
                    return False
            return False

    def __gt__(self, other):
        if sum(self.val) > sum(other.val):
            return True
        elif sum(self.val) < sum(other.val):
            return False
        else:
            for i,j in zip(self.val,other.val):
                if i > j:
                    return True
                if i < j:
                    return False
            return False


    def __eq__(self, other):
        if sum(self.val) != sum(other.val):
            return False
        else:
            for i,j in zip(self.val, other.val):
                if i != j:
                    return False
            return True
 
class MaxHeapTermOrder(TermOrder):
    '''
    Called by MaxHeap object to reverse the ordering for a min heap
    Used exclusively with TermOrder objects
    '''
    def __init__(self,term_order_tuple):
        '''
        Takes in a tuple
        '''
        self.val = term_order_tuple

    def __lt__(self,other): return TermOrder(self.val) > TermOrder(other.val)
    def __gt__(self,other): return TermOrder(self.val) < TermOrder(other.val)
    def __eq__(self,other): return TermOrder(self.val) == TermOrder(other.val)
    def __str__(self): return str(self.val)


class MaxHeap(object):
    '''
    implementation of a set min priorioty queue, one that only adds 
    values to the queue if they don't exist there already
    Do we want to pass term order objects or tuples? 
    If you want to pass TermOrder objs, simply remove this line in headpush
    x = TermOrder(x)
    everything else is identitcal, that will change it to TermOrder on insert
    '''
    def __init__(self): 
        self.h = []
        self._set = set()

    def heappush(self, x): 
        x = MaxHeapTermOrder(x)
        if not x.val in self._set:
            heapq.heappush(self.h,x)
            self._set.add(x.val)
        else:
            pass
            #print('Double')

    def heappop(self): 
        val = heapq.heappop(self.h).val
        self._set.discard(val)
        return val
    def __getitem__(self, i): return self.h[i].val
    def __len__(self): return len(self.h)



class MinHeap(MaxHeap):
    '''
    Implementation of a set max priorioty queue, one that only adds 
    values to the queue if they don't exist there already
    See note in MinHeap about TermOrderObj
    '''
    def heappush(self,x): 
        x = TermOrder(x)
        if not x.val in self._set:
            heapq.heappush(self.h, x)
            self._set.add(x.val)

