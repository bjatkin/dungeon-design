from graph_node import Start, Key, Lock, End

class Graph():
    def __init__(self, lock_count):
        # Generate starting and ending nodes
        start = Start()
        end = End()

        # Generate key and door sets
        node = start
        for i in range(lock_count+1):
            # Not sure why but child_s must be set to [] but if it's not the graph is broken
            k = Key(parent_s=[node], child_s=[], name="Key"+str(i))
            l = Lock(key_s=[k], parent_s=[node], child_s=[], name="Lock"+str(i))

            k.add_lock_s([l])
            node.add_child_s([l, k])
            node = l

        end.add_parent_s([node])
        node.add_child_s([end])

        self.start = start



graph = Graph(lock_count=3)
node = graph.start

count = 0
while not node.name == "End":
    count += 1
    print(node.name)
    for c in node.child_s:
        print("child: ", c.name)
    for p in node.parent_s:
        print("parent: ", p.name)

    if len(node.child_s) == 0:
        break  

    if count > 5:
        break

    node = node.child_s[0]
    print("-------------------------")

print("End: ", node.name)