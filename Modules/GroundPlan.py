import queue
import subprocess
import cv2

from Modules import highgui


class Adjacany(object):
    def __init__(self, fromRoom, toRoom):
        self.fromRoom = fromRoom
        self.toRoom = toRoom
        self.color = "black"


class Room(object):
    def __init__(self, mark):
        self.mark = mark
        self.visitedIndex = -1


class GroundPlan(object):
    nodes = ['I', 'II', 'III', 'IV', 'V', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S' ]
    adjacencies = {
            'I': ['II'],
            'II': ['I', '1', '5', '6', 'A', 'E', 'F', 'III'],
            'III': ['II', 'IV', 'L', '12'],
            'IV': ['III', 'L', '12', 'S', '19'],
            'V': ['S', '19'],
            '1': ['2', 'II'],
            '2': ['1', '3', '4', '5'],
            '3': ['2', '4'],
            '4': ['2', '3', '5', '7', '8'],
            '5': ['2', '4', '7', 'II'],
            '6': ['7', '9', 'II'],
            '7': ['4', '5', '6', '8', '9'],
            '8': ['4', '7', '13'],
            '9': ['6', '7', '10'],
            '10': ['9', '11'],
            '11': ['10', '12'],
            '12': ['11', '19', 'L', 'S'],
            '13': ['8', '14', '16'],
            '14': ['13', '15'],
            '15': ['14', '16'],
            '16': ['13', '15', '17', '18'],
            '17': ['16', '18', '19'],
            '18': ['16', '17', '19'],
            '19': ['12', '16', '17', '18', 'S', 'L', 'V'],
            'A': ['B', 'II'],
            'B': ['A', 'C', 'D', 'E'],
            'C': ['B', 'D'],
            'D': ['B', 'C', 'E', 'G', 'H'],
            'E': ['B', 'D', 'G', 'II'],
            'F': ['G', 'I', 'II'],
            'G': ['D', 'E', 'F', 'I'],
            'H': ['D', 'G', 'M'],
            'I': ['F', 'G', 'J'],
            'J': ['I', 'K'],
            'K': ['J', 'L'],
            'L': ['K', '12', '19', 'S'],
            'M': ['H', 'N'],
            'N': ['M', 'O'],
            'O': ['N', 'P'],
            'P': ['M', 'O', 'Q', 'R', 'S'],
            'Q': ['M', 'P', 'R', 'S'],
            'R': ['P', 'Q', 'S'],
            'S': ['P', 'Q', 'R', 'L', '12', '19'],
        }
    def __init__(self):
        self.rooms = [Room(node) for node in GroundPlan.nodes]
        self.adjacencyList = []
        for room in self.rooms:
            for neighbour in GroundPlan.adjacencies[room.mark]:
                neighbourRoom = next(r for r in self.rooms if r.mark == neighbour)
                self.adjacencyList.append(Adjacany(room, neighbourRoom))
        
        #for room in self.rooms:
        #    for neighbour in GroundPlan.adjacencyList[room.mark]:
        #        room.appendToAdjacanyList(neighbour)
        self.maxVisitedIndex = 0  # keeps the maximum amount of visited rooms, this is used to determine the intermediate and end node
        self.previousRoom = Room('-')  # keeps information of the previous room, is needed for transitions. A dummy room is used here as a starting room
        self.roomTransitions = []  # keeps information of room transitions


    def visualize(self):
        """
        Builds a .dot file and generates a .png image.
        This image gets loaded as a cv2 image and is returned.
        """

        output = "digraph G {"

        for room in self.rooms:
            if(room.visitedIndex == 1): # the node is the starting node
                output += f"{room.mark}[fillcolor=green, style=filled]\n"
            elif(room.visitedIndex > 1 and room.visitedIndex < self.maxVisitedIndex): # the node is an intermediate node
                output += f"{room.mark}[fillcolor=orange, style=filled]\n"
            elif(room.visitedIndex == self.maxVisitedIndex): # the node is the ending node
                output += f"{room.mark}[fillcolor=blue, style=filled]\n"

        for adjacany in self.adjacencyList:
            output += f"{adjacany.fromRoom.mark} -> {adjacany.toRoom.mark}[color={adjacany.color}]\n"

        output += "}"
        F = open("groundplan.dot", "w")
        F.write(output)
        F.close()
        subprocess.run(['dot', 'groundplan.dot', '-Tpng', '-o', 'groundplan.png'])
        return highgui.loadImage("groundplan.jpg")
        

    def markVisited(self, mark):
        """
        Marks a node as visited. It also keeps track of transitions between nodes.
        """
        if mark not in self.nodes:
            return

        
        for room in self.rooms:
            if(room.mark == mark):
                room.visitedIndex = self.maxVisitedIndex
                self.roomTransitions.append([self.previousRoom.mark, room.mark])
                if(self.previousRoom.mark is not '-'):
                    try:
                        adjacany = next(adj for adj in self.adjacencyList if adj.fromRoom == self.previousRoom and adj.toRoom == room)
                        self.maxVisitedIndex += 1
                        adjacany.color = "green"
                    except StopIteration:
                        print('A room was visited which is not in the neighbour list of the previous visited room') # TODO: needs better message or no op
                self.previousRoom = room


def groundPlanMessageConsumer(groundPlan=None, q=None):
    if groundPlan is not None and queue is not None:
        while(1):
            zaal = q.get()
            print(zaal)
            if zaal == 'q':
                break
            else:
                try:
                    groundPlan.markVisited(zaal)
                except:
                    print('GroundPlan.markVisited threw an exception')