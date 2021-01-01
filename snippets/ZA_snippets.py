# classes / gameplay loop / some functions redacted

    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        #use breadth-first search, which uses four-way
        #once a square is found with a human, stop
        #if multiple at same iteration, choose random

        #imitate fire spreading check
        #does not apply to square if obstacle is on it.
        #each new iteration will have new squares being applied
        #four way distance

        #not necessarily returning a distance
        #see which of the opposite entities comes into contact w/
        #the search first

        #create new grid of same size of original, empty

        visit_grid = poc_grid.Grid(self._grid_height, self._grid_width)

        #create 2d list distance-field; present as dictionary for later use
        dist_field = [] #make a list of a list which corresponds to height/width

        #2 grids to compare w/ original
        for dummy_i in range(self._grid_height):
            temp_lst = []
            for dummy_j in range(self._grid_width):
                temp_lst.append(self._grid_height*self._grid_width)
            dist_field.append(temp_lst)

        q_boundary = poc_queue.Queue()

        if entity_type == ZOMBIE:
            entities = self._zombie_list
        else:
            entities = self._human_list

        for entity in entities:
            q_boundary.enqueue(entity)
            visit_grid.set_full(entity[0], entity[1])
            dist_field[entity[0]][entity[1]] = 0 #set other entities in list to 0 val.


        while len(q_boundary) != 0:
            current_cell = q_boundary.dequeue()
            current_dist = dist_field[current_cell[0]][current_cell[1]]

            #checks each of the values which is returned by four_neighbors
            neighbors = visit_grid.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                #T/F if empty on both grids & no obstacle (considered FULL)
                if self.is_empty(neighbor[0], neighbor[1]) and visit_grid.is_empty(neighbor[0], neighbor[1]):
                    visit_grid.set_full(neighbor[0], neighbor[1]) # set full
                    dist_field[neighbor[0]][neighbor[1]] = current_dist + 1 #set val
                    q_boundary.enqueue(neighbor)
        return dist_field
