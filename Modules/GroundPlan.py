class GroundPlan(object):
    def __init__(self):
        self.nodes = ['I', 'II', 'III', 'IV', 'V', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S' 
        ]
        self.adjacencyList = {
            'I' : ['II'],
            'II' : ['I', '1', '5',' 6', 'A', 'E', 'F', 'III'],
            'III' : ['II', 'IV', 'L', '12'],
            'IV' : ['III', 'L', '12', 'S', '19'],
            'V' : ['S', '19'],
            '1' : ['2', 'II'],
            '2' : ['1', '3', '4', '5'],
            '3' : ['2', '4'],
            '4' : ['2', '3', '5', '7', '8'],
            '5' : ['2', '4', '7', 'II'],
            '6' : ['7', '9', 'II'],
            '7' : ['4', '5', '6', '8', '9'],
            '8' : ['4', '7', '13'],
            '9' : ['6', '7', '10'],
            '10' : ['9', '10'],
            '11' : ['10', '12'],
            '12' : ['11', '19', 'L', 'S'],
            '13' : ['8', '14', '16'],
            '14' : ['13', '15'],
            '15' : ['14', '16'],
            '16' : ['13', '15', '17', '18'],
            '17' : ['16', '18', '19'],
            '18' : ['16', '17', '19'],
            '19' : ['12', '16', '17', '18', 'S', 'L'],
            'A' : ['B', 'II'],
            'B' : ['A', 'C', 'D', 'E'],
            'C' : ['B', 'D'],
            'D' : ['B', 'C', 'E', 'G', 'H'],
            'E' : ['B', 'D', 'G', 'II'],
            'F' : ['G', 'I', 'II'],
            'G' : ['D', 'E', 'F', 'I'],
            'H' : ['D', 'G', 'M'],
            'I' : ['F', 'G', 'J'],
            'J' : ['I', 'K'],
            'K' : ['J', 'L'],
            'L' : ['K', '12', '19', 'S'],
            'M' : ['H', 'N'],
            'N' : ['M', 'O'],
            'O' : ['N', 'P'],
            'P' : ['M', 'O', 'Q', 'R', 'S'],
            'Q' : ['M', 'P', 'R', 'S'],
            'R' : ['P', 'Q', 'S'],
            'S' : ['P', 'Q', 'R', 'L', '12', '19'],
        }
        self.visitedList = {node: False for node in self.nodes}

    def visualize(self):
        """
        Generates a .dot file which can be used by the graphviz engine (http://www.webgraphviz.com/)
        """
        output = "digraph G {"

        for node, visited in self.visitedList.items():
            if(visited):
                output += f"{node}[fillcolor=red, style=filled]\n"

        for node, adjList in self.adjacencyList.items():
            for neighbour in adjList:
                output += f"{node} -> {neighbour}\n"

        output += "}"
        F = open("groundplan.dot", "w")
        F.write(output)
        F.close()

    def markVisited(self, node):
        self.visitedList[node] = True