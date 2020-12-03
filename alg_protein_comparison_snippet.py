# classes / loop / some functions redacted

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = open(filename, 'r')
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    scoring_file.close()
    return scoring_dict

    def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
        """
        helper function q4
        return dictionary, scoring_distribution, represents un-normalized distribution
        generated by performing following process num_trials times
        - genereate random permutation rand_y of seq_y using random.shuffle()
        - compute max value score for local align of seq_x and seq_y using score matrix
        - increment entry score in dic (scoring_distribution by one)
        """
        seq_x = read_protein(seq_x)
        seq_y = read_protein(seq_y)
        scoring_matrix = read_scoring_matrix(scoring_matrix)
        scoring_distribution = {}

        for entry_score in range(num_trials):
            protein_1 = str(seq_x)
            protein_2 = list(seq_y)
            random.shuffle(protein_2)
            protein_2 = ''.join(protein_2)

            alignment_matrix = student.compute_alignment_matrix(protein_1, protein_2, scoring_matrix, False)
            scoring_distribution[entry_score] = student.compute_local_alignment(protein_1, protein_2, scoring_matrix, alignment_matrix)[0]

        return scoring_distribution

    def calculate_mean_SD_zscore(graph):
        """
        takes graph, unnormalized
        output tuple (mean, SD, zscore)
        """
        #due to each item playing off of one another, combined into one

        #calculate mean
        total_value = 0.0
        total_numbers = 0.0
        for num in graph:
            total_value += (num*graph[num])
            total_numbers += graph[num]
        mean = total_value/total_numbers

        #calculate SD
        sum_sq_distance = 0
        for num in graph:
            sq_distance = (abs(num-mean))**2
            sum_sq_distance += sq_distance * graph[num]
        sum_sq_distance /= total_numbers
        standard_deviation = math.sqrt(sum_sq_distance)

        #calculate zscore
        #according to solution, s = 875
        z_score = (875 - mean) / standard_deviation

        return (mean, standard_deviation, z_score)
    