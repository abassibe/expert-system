class Stack:
    def __init__(self):
        self.stack = []
        self.capacity = len(self.stack)


    def peek(self):
        if self.capacity >= 1:
            var = self.stack.pop()
            self.stack.append(var)
            return var


    def lenght(self):
        return self.capacity


    def push(self, to_push):
        self.stack.append(to_push)
        self.capacity += 1


    def pop(self):
        if self.capacity > 0:
            self.capacity -= 1
            return self.stack.pop()


    def isEmpty(self):
        return self.capacity == 0


    def flush(self):
        self.stack = []
    

    def __repr__(self):
        return ''.join([elem for elem in self.stack])
