import test_warehouse as t
import warehouse as we
import policy as p
import pydot
import time


def warehouse_01_mcts_graph():
    #env = t.make_test_warehouse_env_01()
    #env = t.make_test_env_o12_f3()
    env = t.make_test_env_o9_f3()
    policy = p.MCTSPolicy()
    policy.max_iteration = 500
    policy.print_node_flag = True
    we.execute(env, policy, 1)
    graph_node(policy.root)

    t.print_result(env, policy)

def graph_node(root):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')

    pydot_root = pydot.Node(str(root.order_no),label='root')
    graph.add_node(pydot_root)

    graph_node_sub(graph, root.children, pydot_root)

    file_name = 'mcts_' + str(round(time.time())) + '.png'

    graph.write_png(file_name)


def graph_node_sub(graph, children, parent_pydot_node):

    for child in children:
        node_label = str('[' + str(child.order_no) + '],v=' + str(child.visits))
        pydot_node = pydot.Node(str(child.order_no_sequence),label=node_label)
        edge_label = str( 'UCB=' +  str(round(child.ucb,2))  )
        edge = pydot.Edge(parent_pydot_node, pydot_node, label=edge_label)
        graph.add_node(pydot_node)
        graph.add_edge(edge)
        graph_node_sub(graph, child.children, pydot_node)


if __name__ == '__main__':
    warehouse_01_mcts_graph()

