class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def find_by_index(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current
            count += 1
            current = current.next
        raise IndexError("Index out of range")