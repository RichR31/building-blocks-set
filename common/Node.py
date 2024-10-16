class Node():
    def __init__(self, priority:int, sub:int,data:any):
        self.priority = priority
        self.data = data
        self.sub = sub
        self.prev:Node = None
        self.next:Node = None

    def __lt__(self, other)->bool:
        if self.priority == other.priority:
            return self.sub < other.sub
        else:
            return self.priority < other.priority

    def __gt__(self,other)->bool:
        
        if self.priority == other.priority:
            return self.sub > other.sub
        else:
            return self.priority > other.priority
    
    def __le__(self,other)->bool:
        if self.priority == other.priority:
            return self.sub <= other.sub
        else:
            return self.priority <= other.priority
    
    def __ge__(self,other)->bool:
        if self.priority == other.priority:
            return self.sub >= other.sub
        else:
            return self.priority >= other.priority
    
    def __eq__(self,other)->bool:
        if self.priority == other.priority:
            return self.sub <= other.sub
        else:
            return False
    