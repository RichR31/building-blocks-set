from Node import Node

class PriorityQueue:
    """
    A priority queue that stores nodes in a linked list.
    The nodes are ordered by priority.
    The queue has a maximum capacity and will remove the node with the lowest priority
    when the capacity is exceeded.

    Parameters
    ----------
    capacity:int
        The maximum number of nodes that the queue can hold.

    Methods
    -------
    put(priority:int,sub:int,data:any)->int
        Adds a node to the queue. Returns 1 if the node was added, 0 if the queue is full and the node was not added.

    get()->tuple
        Removes and returns the node with the highest priority.

    peek()->tuple
        Returns the node with the highest priority without removing it.

    empty()
        Removes all nodes from the queue

    is_empty()->bool
        Returns True if the queue is empty, False otherwise

    __str__()->str
        Returns a string representation of the queue in the format (priority,data)->(priority,data)->...->(priority,data)

    
    """
    def __init__(self,capacity:int):
        self.front:Node = None
        self.rear:Node = None
        self.capacity:int = capacity
        self.length:int = 0

    def __str__(self) -> str:
        output = ""
        current = self.front
        for i in range(self.length):
            output += "("+str(current.priority)+","+str(current.data)+")"
            output += "" if i==self.length-1 else "->"
            current = current.next

        return output
    
    def is_empty(self)->bool:
         return self.length <= 0
    
    def put(self,priority:int,sub:int,data:any)->int:
        new_node = Node(priority,sub,data)

        if self.is_empty():
            self.front = new_node
            self.rear = new_node
            self.length +=1
            return 1
        
        #if queue is full and the new node is smaller than the rear node
        elif self.length == self.capacity and new_node <= self.rear :
            return 0
        

        #if the new node is smaller than the rear node
        if new_node <= self.rear:
            self.rear.next = new_node
            new_node.prev = self.rear
            self.rear = new_node
            self.length+=1
            return 1

        #traverse queue to see where does it belong
        current = self.front
        for i in range(self.length):
            previous = current.prev

            #add the node to the linked list
            if new_node >= current:

                #when the current node is the front node
                if i==0:
                    self.front = new_node
                    new_node.prev = None
                else:
                    previous.next= new_node
                    new_node.prev = previous
                    

                #when the current node is the rear node
                if i == self.capacity-1:
                    self.rear = new_node
                    new_node.next = None
                else:
                    current.prev = new_node
                    new_node.next = current
                    self.length +=1
                    

                #make sure that the length stays within capacity
                if self.length > self.capacity:
                    target = self.rear.prev
                    target.next = None
                    self.rear = target
                    self.length -=1

                return 1
            current = current.next
            
    
    def get(self)->tuple:
        if self.length==0:
            return None
        else:
            target = self.front
            self.front = target.next
            self.length -=1
            return target.priority, target.sub, target.data
    
    def peek(self)->tuple:
        return self.front.priority, self.front.sub, self.front.data

    def empty(self):
        self.front=None
        self.rear=None
        self.length=0


            

