class Node:
    def __init__(self, data = None) -> None:
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self, *args) -> None:
        self.head = None
        self.tail = None
        self.length = 0     # initialize length of list as 0
        for arg in args:
            self.push_back(arg)
    
    def push_back(self, data) -> None:
        """
        add the data into the back of the list

        :param `data`: `Any` type to add to the back of the list
        """
        new_tail = Node(data)   # new data
        if self.tail == None:   # empty list
            self.head = self.tail = new_tail
        else:
            self.tail.next = new_tail
            new_tail.prev = self.tail
            self.tail = new_tail

        self.length += 1    # add to length
    
    def push_front(self, data) -> None:
        """
        add the data into the front of the list

        :param `data`: `Any` type to add to the front of the list
        """
        new_head = Node(data)   # new data
        if self.head == None:   #empty list
            self.head = self.tail = new_head
        else:
            self.head.prev = new_head
            new_head.next = self.head
            self.head = new_head

        self.length += 1    # add to length

    def remove_front(self) -> None:
        if(self.head is not None): # only when the list is not empty
            if(self.head.next is None): # only one element on the list
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None

            self.length -= 1    # subtract length by 1