# classes / loop / some functions redacted

"""
Implementing BFS

Computing set of connect components (CCs) of an undirected graph
as well as determining the size of its largest component

computing resilience of a graph (measured by size of largest CC)
as a sequence of nodes are deleted from the graph
"""
def compute_resilience(ugraph, attack_order):
    """
    takes undirected ugraph, list of nodes attack_order
    iterates through attack_order
    removes the given node and its edges from graph then computes size of largest CC
    return list whose k+1th entry is size of largest CC, after removal of first k in attack_order
    first entry (index 0) is size of largest CC in original graph
    """
    #calculates the largest connected component after each attack
    #strongest = []
    largest = []
    attacking = list(attack_order)
    test_graph = dict(ugraph)
    largest.append(largest_cc_size(test_graph))
    while len(attacking) > 0:

        #removes item from test graph & attack order
        #keep info(neighbors) of deleted node, delete the node, delete the info of deleted node
        #test graph is dict, attack_order is list
        attack = attacking.pop(0)
        removed = test_graph.pop(attack)
        for item in removed: #return set of values, remove item, place back in dict
            change = test_graph[item]
            change.remove(attack)
            test_graph[item] = change

        largest.append(largest_cc_size(test_graph))
        #if test_largest > largest:
        #largest test_largest
            #strongest = []
            #for key in test_graph:
                #strongest.append(key)
    return largest
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    
def make_er_graph(num_nodes, probability): #probability == 0.004
    """
    takes number of nodes
    returns dictionary corresponding to complete directed graph
    contains all possible edges (minus self-loops)
    numbered 0 to num_nodes - 1, when num_nodes is positive
    otherwise, return dic. correspond empty graph
    """
    #if not positive / contains 0
    if num_nodes < 1:
        return {}


    er_graph = {}
    edge_queue = deque([])
    edge_queue.extend(range(num_nodes))

    #BFS_check = [nodes for nodes in range(num_nodes)]
    #create a dic. value for range num_nodes

    #create a pairing system which removes the current item from the list when creating next iteration
    #queue system
    while len(er_graph) < num_nodes:
        #keep going until ER_graph completed
        current_list = []
        current_node = edge_queue.popleft()
        for edge in edge_queue:
            if probability < random.random():
                continue
            else:
                current_list.append(edge)
                #place edge value in opposite permutation as well
            if edge in edge_queue:
                if edge in er_graph.keys():
                    er_graph[edge].add(current_node)
                else:
                    er_graph[edge] = set([current_node])

        if current_node in er_graph.keys(): #if key exists with values, update, else create key and value pair
            er_graph[current_node].update(set(current_list))
        else:
            er_graph[current_node] = set(current_list)
            #places edge w/ p probability


    return er_graph
