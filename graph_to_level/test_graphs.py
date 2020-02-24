from graph_structure.graph_node import GNode, Start, End

class TestGraphs:
    @staticmethod
    def get_man_graph():
        a = Start()
        b = GNode("b")
        c = GNode("c")
        d = GNode("d")
        e = GNode("e")
        f = End()
        g = GNode("g")
        h = GNode("h")
        i = GNode("i")

        a.add_child_s(b)
        a.add_child_s(c)
        a.add_child_s(d)
        b.add_child_s(e)
        c.add_child_s(f)
        c.add_child_s(g)
        c.add_child_s(h)
        c.add_child_s(i)
        h.add_child_s(i)

        return a, {a, b, c, d, e, f, g, h, i}

    @staticmethod
    def get_house_graph():
        a = GNode("a")
        b = GNode("b")
        c = GNode("c")
        d = GNode("d")
        e = GNode("e")
        a.add_child_s(b)
        b.add_child_s(c)
        c.add_child_s(d)
        d.add_child_s(a)
        c.add_child_s(e)
        e.add_child_s(a)
        e.add_child_s(d)

        return a, {a, b, c, d, e}

    @staticmethod
    def get_triangle_graph():
        a = GNode("a")
        b = GNode("b")
        c = GNode("c")
        d = GNode("d")
        a.add_child_s(b)
        b.add_child_s(c)
        c.add_child_s(a)
        a.add_child_s(d)
        b.add_child_s(d)
        c.add_child_s(d)

        return a, {a, b, c, d}

    @staticmethod
    def get_graph_a():
        n1 = GNode("a")
        n2 = GNode("b")
        n3 = GNode("c")
        n4 = GNode("d")
        n5 = GNode("e")

        n1.add_child_s([n3, n4, n5])
        n2.add_child_s([n3, n4, n5])
        n3.add_child_s([n1, n2, n4, n5])
        n4.add_child_s([n1, n2, n3, n5])
        n5.add_child_s([n1, n2, n3, n4])

        return n1, {n1, n2, n3, n4, n5}

    @staticmethod
    def get_graph_b():
        n1 = GNode("a")
        n2 = GNode("b")
        n3 = GNode("c")
        n4 = GNode("d")
        n5 = GNode("e")
        n6 = GNode("f")
        n7 = GNode("g")
        n8 = GNode("h")
        n9 = GNode("i")
        n10 = GNode("j")

        n1.add_child_s([n2, n3])
        n2.add_child_s(n4)
        n3.add_child_s([n4, n5])
        n5.add_child_s(n6)
        n6.add_child_s(n7)
        n7.add_child_s([n8, n9])
        n8.add_child_s(n10)
        n9.add_child_s(n10)

        return n1, {n1, n2, n3, n4, n5, n6, n7, n8, n9, n10}