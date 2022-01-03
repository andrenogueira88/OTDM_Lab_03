class Graph:

    # Initialize the complete graph as an adjacent matrix
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    # Return the edges (links) from the MST
    def remaining_links_MST(self):

        # Start the keys with a large value
        key = [99999] * self.V
        # Start the list of remaining edges as blank
        remaining_links = [None] * self.V
        # The first key is set to 0 so it will start by including Node 0 in the MST
        key[0] = 0
        # Start the list of nodes already included in the MST (True is included False Not)
        mstSet = [False] * self.V
        remaining_links[0] = -1

        # Loop over all nodes in the graph
        for count in range(self.V):

            # Find the edge with minimum distance not inserted yet
            min_k = 99999
            for v in range(self.V):
                if key[v] < min_k and mstSet[v] == False:
                    min_k = key[v]
                    u = v

            # Put the node in MST
            mstSet[u] = True

            # Update weight of the adjacent nodes
            for v in range(self.V):
                if 0 < self.graph[u][v] < key[v] and mstSet[v] == False:
                    key[v] = self.graph[u][v]
                    remaining_links[v] = u
        return remaining_links
