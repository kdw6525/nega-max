# creating a state class where the scoring function passed as a parameter

class State:
    # scoring function must only take the model as a parameter
    def __init__(self, model, scoring_function):
        self.model = model
        self.s_f = scoring_function
    
    def evaluate(self):
        return self.s_f(self.model)
    
class Node:
    def __init__(self, parent, children, state):
        self.p = parent
        self.c = children
        self.s = state

    def evaluate(self):
        return self.s.evaluate()
    
    def __str__(self):
        string = f'{self.evaluate()}: '
        for child in self.c:
            string += f'{child.evaluate()} '
        return string
    
    def add_child(self, child):
        self.c.append(child)
    

def main():
    # do some test ig
    def f(x):
        return (lambda m : x)
    
    root = Node(None, [], State(None, f(1)))
    root.add_child(Node(root, [], State(None, f(2))))
    root.add_child(Node(root, [], State(None, f(3))))

    print(root)
    return

if __name__ == '__main__':
    main()