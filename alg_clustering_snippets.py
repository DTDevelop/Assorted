# classes / loop / some functions redacted

DATA_3108_URL = open(os.path.join(sys.path[0], "unifiedCancerData_3108.csv"), "r")
#DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_896_URL = open(os.path.join(sys.path[0], "unifiedCancerData_896.csv"), "r")
#DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_290_URL = open(os.path.join(sys.path[0], "unifiedCancerData_290.csv"), "r")
#DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
DATA_111_URL = open(os.path.join(sys.path[0], "unifiedCancerData_111.csv"), "r")

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    #data_file = urllib2.urlopen(data_url)
    data_file = data_url
    data = data_file.read()
    data_lines = data.split('\n')
    #print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])]
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering

    Note that method may return num_clusters or num_clusters + 1 final clusters
    """

    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters

    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)

    return cluster_list
def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    new_cl = list(cluster_list)
    new_cl.sort(key = lambda cluster: cluster.horiz_center())
    while len(new_cl) > num_clusters:
        current_merge = fast_closest_pair(new_cl)
        new_cl[current_merge[1]].merge_clusters(new_cl[current_merge[2]])
        #above mutates self, so remove other cluster
        new_cl.pop(current_merge[2])
        #sort new_cl by height, as FCP needs it
        new_cl.sort(key = lambda cluster: cluster.horiz_center())
    return new_cl

def gen_random_cluster(num_clusters):
    """
    creates list of clusters
    each cluster corresponds to one random gen. point w/ corners (+-1,+-1)
    each cluster is within these coordinates
    """
    cluster_group = []
    for dummy_cluster in range(num_clusters):
        sign_h = random.choice([1,-1])
        sign_v = random.choice([1,-1])
        random_horz = random.random()*sign_h
        random_vert = random.random()*sign_v
        cluster_group.append(Cluster(set(),random_horz,random_vert,0,0))
        cluster_group.sort(key = lambda cluster: cluster.horiz_center())
    return cluster_group
