class Room(object):
    def __init__(self, mark):
        self.mark = mark
        self.adjacencyList = []
        self.visitedIndex = -1
    
    def appendToAdjacanyList(self, node):
        self.adjacencyList.append(node)


class GroundPlan(object):
    nodes = ['I', 'II', 'III', 'IV', 'V', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S' ]
    adjacencyList = {
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
            '10' : ['9', '11'],
            '11' : ['10', '12'],
            '12' : ['11', '19', 'L', 'S'],
            '13' : ['8', '14', '16'],
            '14' : ['13', '15'],
            '15' : ['14', '16'],
            '16' : ['13', '15', '17', '18'],
            '17' : ['16', '18', '19'],
            '18' : ['16', '17', '19'],
            '19' : ['12', '16', '17', '18', 'S', 'L', 'V'],
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
    def __init__(self):
        self.rooms = [Room(node) for node in GroundPlan.nodes]
        for room in self.rooms:
            for neighbour in GroundPlan.adjacencyList[room.mark]:
                room.appendToAdjacanyList(neighbour)
        self.maxVisitedIndex = 0 # keeps the maximum amount of visited rooms, this is used to determine the intermediate and end node
        self.previousRoom = Room('-') # keeps information of the previous room, is needed for transitions
        self.roomTransitions = [] # keeps information of room transitions



    def visualize(self):
        """
        Generates a .dot file which can be used by the graphviz engine (http://www.webgraphviz.com/)
        """
        
        output = "digraph G {"
        
        for i in range(1, len(self.roomTransitions)):
            output += f"{self.roomTransitions[i][0]} -> {self.roomTransitions[i][1]}[color=green]\n"

        for room in self.rooms:
            if(room.visitedIndex == 1):
                output += f"{room.mark}[fillcolor=green, style=filled]\n"
            elif(room.visitedIndex > 1 and room.visitedIndex < self.maxVisitedIndex):
                output += f"{room.mark}[fillcolor=orange, style=filled]\n"
            elif(room.visitedIndex == self.maxVisitedIndex):
                output += f"{room.mark}[fillcolor=blue, style=filled]\n"

        for room in self.rooms:
            for neighbour in room.adjacencyList:
                output += f"{room.mark} -> {neighbour}\n"

        output += "}"
        F = open("groundplan.dot", "w")
        F.write(output)
        F.close()

    def markVisited(self, mark):
        self.maxVisitedIndex += 1
        for room in self.rooms:
            if(room.mark == mark):
                room.visitedIndex = self.maxVisitedIndex
                self.roomTransitions.append([self.previousRoom.mark, room.mark])
                if(len(self.previousRoom.adjacencyList) > 0): # slechte methode, verwijdert de oude verbinding om dubbele lijn in graphviz te voorkomen
                    self.previousRoom.adjacencyList.remove(room.mark)
                self.previousRoom = room