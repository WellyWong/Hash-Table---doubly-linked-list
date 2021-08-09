"""
https://github.com/gabrielegilardi/HashTable/blob/master/Code_Python/HashTable.py
https://gist.github.com/edwintcloud
hash_str uses the djb2 algorithm to compute the hash value of a string http://www.cse.yorku.ca/~oz/hash.html
"""
def hash_str(string):
    hash_n = 5381
    for char in string:
        hash_n = (hash_n << 5) + hash_n + ord(char)   # (hash_n << 5) + hash_n == hash_n * 33
    return hash_n

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self, items=None):
        self.head = None
        self.tail = None

        if items is not None:
            for item in items:
                self.append(item)

    def append(self, k, v):
        new_node = Node(k, v)

        #if the list is empty, set self.head to the new node
        if self.head is None:
            self.head = new_node
        else:
            #otherwise, insert new node after tail
            self.tail.next = new_node
            new_node.prev = self.tail
        self.tail = new_node

    def getItems(self):
        #return a list of items in the LinkedList
        items = []
        cur_node = self.head

        while cur_node is not None:
            if cur_node is self.tail:
                items.append((cur_node.key, cur_node.value))
                break
            items.append((cur_node.key, cur_node.value))
            cur_node = cur_node.next

        return items

    def find(self, k):
        #return value found by key in the LinkedList, or None if it is not found
        cur_node = self.head

        while cur_node is not None:
            if cur_node.key == k:
                return cur_node
            cur_node = cur_node.next

        return None

    def delete(self, k):
        #return True is item/node is successfully deleted from LinkedList, otherwise return False
        cur_node = self.head

        while cur_node is not None:
            if cur_node.key == k:
                if cur_node == self.head and cur_node.next is not None:
                    self.head = cur_node.next
                    cur_node.next = None

                elif cur_node == self.tail:
                    self.tail = cur_node.prev
                    cur_node.prev.next = None
                    cur_node.prev = None
                    cur_node.next = None

                else:
                    prev_node = cur_node.prev
                    prev_node.next = cur_node.next
                    cur_node.next.prev = prev_node
                    cur_node.next = None
                    cur_node.prev = None

                return True

            else:
                cur_node = cur_node.next

        return False


class HashTable:
    def __init__(self, size, items=None):
        self.size = size
        self.slots = [LinkedList() for i in range(self.size)]
        self.num_items = 0
        if items is not None:
            for item in items:
                k, v = item
                self.set(k, v)

    def _hash_str(self, string):
        #return a hash of the given string.
        hash = 5381
        for c in string:
            hash = ((hash << 5) + hash + ord(c)) % self.size
        return hash

    def get_items(self):
        #return a list of tuple (key, value) representing all the item in the hash table
        items = []
        for slot in self.slots:
            items.append(slot.getItems())
        return items

    def contains(self, key):
        #return True if the key is found in the hash table, otherwise return False
        slotIndex = self._hash_str(key)
        if self.slots[slotIndex].find(key) is not None:
            return True
        else:
            return False

    def set(self, k, v):
        #add an item ot the hash table
        slotIndex = self._hash_str(k)
        slot = self.slots[slotIndex]
        node = slot.find(k)
        if node is not None:    #if there's already a key, change the value
            node.value = v
        else:
            slot.append(k, v)
            self.num_items += 1

    def remove(self, k):
        slotIndex = self._hash_str(k)
        slot = self.slots[slotIndex]
        return slot.delete(k)


items = [('fruit', 25), ('animal', 75), ('book', 120), ('socks', 200), ('tool', 28)]
ht = HashTable(8, items)
ht_items = ht.get_items()
print(ht_items)

print(ht.remove('book'))
ht_items = ht.get_items()
print(ht_items)
