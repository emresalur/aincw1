# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api

#
# A class that creates a grid that can be used as a map
#
# The map itself is implemented as a nested list, and the interface
# allows it to be accessed by specifying x, y locations.
#
# Made some modiciations on the pretty display function to make it more readable and visually appealing


class Grid:

    # Constructor
    #
    # Note that it creates variables:
    #
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    #
    # Grid elements are not restricted, so you can place whatever you
    # like at each location. You just have to be careful how you
    # handle the elements when you use them.
    #
    # Grid class is taken from the Week 5 lab.
    # Accessed on KEATS, file is mapagents.py
    def __init__(self, width, height):
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

    # Print the grid out.
    def display(self):
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print (self.grid[i][j],)
            # A new line after each line of the grid
            print
        # A line after the grid
        print

    # The display function prints the grid out upside down. This
    # prints the grid out so that it matches the view we see when we
    # look at Pacman.
    # Only function that I have modified inside the Grid class
    def prettyDisplay(self):
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                val = self.grid[self.height - (i + 1)][j]
                if val == '%':
                    # Makes the walls more visible
                    print '%%%%',
                else:
                    # Makes the rest of the grid more visible
                    # '%4d' is a string format I found online
                    print '%4d' % val,
            # A new line after each line of the grid
            print
        # A line after the grid
        print

    # Set and get the values of specific elements in the grid.
    # Here x and y are indices.
    def setValue(self, x, y, value):
        self.grid[y][x] = value

    def getValue(self, x, y):
        return self.grid[y][x]

    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

# Author: Emre Salur
# Student ID: 20082471
# Date: 2/12/2022

# This is a class that tries to win the game by using the MDP algorithm.
# My approach consists of 3 main parts:
# 1. Using value iteration through the grid to apply reward values to each cell.
# 2. Using the Bellman equation to convert reward values into utility values.
# 3. Using the utility values to determine the best action to take at each cell.


class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print ("Starting up MDPAgent!")

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print ("Running registerInitialState for MDPAgent!")
        print ("I'm at:")
        print (api.whereAmI(state))

        # Make a map
        self.makeMap(state)

        # Add walls to the map
        self.addWallsToMap(state)

    # This is what gets run in between multiple games
    # Even though the state argument is not used, the code does not run if I remove it.
    def final(self, state):
        print ("Looks like the game just ended!")

        # Display the map in a nice way
        self.map.prettyDisplay()

    # Make a map by creating a grid of the right size
    # Taken from the Week 5 lab.
    # Accessed on KEATS, file is mapagents.py
    def makeMap(self, state):
        corners = api.corners(state)
        height = self.getLayoutHeight(corners)
        width = self.getLayoutWidth(corners)
        self.map = Grid(width, height)

    # Functions to get the height and the width of the grid.
    #
    # We add one to the value returned by corners to switch from the
    # index (returned by corners) to the size of the grid (that damn
    # "start counting at zero" thing again).
    # Taken from the Week 5 lab.
    # Accessed on KEATS, file is mapagents.py
    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    # Functions to manipulate the map.
    #
    # Put every element in the list of wall elements into the map
    # Taken from the Week 5 lab.
    # Accessed on KEATS, file is mapagents.py
    def addWallsToMap(self, state):
        walls = api.walls(state)
        for i in range(len(walls)):
            self.map.setValue(walls[i][0], walls[i][1], '%')

    def getAction(self, state):
        legal = api.legalActions(state)
        self.valueIteration(state)
        return api.makeMove(self.bestMove(state), legal)

    # Compute value iteration with current state
    def valueIteration(self, state):

        # Set the number of iterations to run the algorithm for.
        # The higher the number, the more accurate the solution will be.
        # However, the higher the number, the longer it will take to run.
        # The number of iterations should be set to a value that is high enough
        # to give a good solution, but not so high that it takes too long to run.

        # The limit we have for the small grid is 5 minutes.
        # The limit we have for the large grid is 25 minutes.

        # The number of iterations is set to 100.
        # This is a good number to use, as it gives a good solution, but does not take too long to run.
        # This number can be changed if needed.
        iteratations = 100
        # Takes approximately 15 seconds to run on the small grid on my computer.
        # Takes approximately 7 and a half minutes to run on the large grid on my computer.

        # Get the width of the map.
        width = self.map.getWidth()

        # Get the height of the map.
        height = self.map.getHeight()

        # We want to set reward values for different elements in the map.
        # No reward for walls, as we do not want to move into walls.
        # Give positive reward for food, as we want to consume all foods.
        # Give a negative reward for the ghost, we do not want to be eaten by the ghost at all costs.
        # The small grid does not have capsules, so we do not need to worry about them.
        # However, the large grid does have capsules, so we need to have a positive value similar to food. 
        # The reward values are not aiming for excellency points, just trying to win.

        # To recognize the different elements in the map, we use the api functions.
        # Initializing state variables.

        # Get the food in the map.
        food = api.food(state)

        # Get the capsules in the map.
        capsules = api.capsules(state)

        # Get the ghost in the map.
        ghosts = api.ghosts(state)

        # Get the ghosts that are near Pacman.
        # For each ghost, we want to check if it is within 2 units of Pacman.
        # If it is, we want to add it to the list of ghosts that are near Pacman.
        # The reason we make it a list is because there can be more than one ghost near Pacman.
        nearGhost = [(g[0]+x, g[1]+y)
                     for g in ghosts for x in [-1, 0, 1] for y in [-1, 0, 1]]

        # Our reward values can be set to whatever we want.
        # In this case, we are going to have different reward values for the small and large grid.

        # For the small grid, we are going to set the reward values as follows:
        # 7 is the height of the small grid.
        if(height == 7):

            # Set the reward value for food to 50.
            foodReward = 50

            # Set the reward value for the ghost to -1000.
            ghostReward = -1000

            # Set the reward value for capsules to 20.
            capsuleReward = 20

            # Set the reward value for when a ghost is nearby to -500. Half of the reward for the ghost seems like a good value.
            ghostNearbyReward = -500

            # Set the reward value for an empty space to 10.
            # The reason behind this is that often the pacman goes inside the maze and gets stuck there
            # since the ghost is following. In some cases, we want to award the pacman for getting away
            # from the ghost even if it is not eating food.
            emptySpaceReward = 10

        # For the large grid, we are going to set the reward values as follows:
        # 11 is the height of the large grid.
        elif(height == 11):

            # Set the reward value for food to 50.
            foodReward = 50

            # Set the reward value for the ghost to -1000.
            ghostReward = -1000

            # Set the reward value for capsules to 20.
            capsuleReward = 20

            # Set the reward value for when a ghost is nearby to -500. Half of the reward for the ghost seems like a good value.
            ghostNearbyReward = -500

            # Set the reward value for an empty space to 0.
            # Compared to the small grid, the large grid has a lot more empty spaces, so we do not want to give a reward for them.
            emptySpaceReward = 0

        # We want to iterate through the grid and update the values of each cell.
        # We want to do this for a set number of iterations.
        for i in range(iteratations):
            # Check for each row
            for j in range(width):
                # Check for each column
                for k in range(height):
                    # Make sure the cell is not a wall.
                    if self.map.getValue(j, k) != '%':
                        # First, consider nearby ghosts. If near the ghost, apply ghost nearby reward.
                        if (j, k) in nearGhost:
                            reward = ghostNearbyReward
                        # If the cell is the ghost, apply ghost reward.
                        elif (j, k) in ghosts:
                            reward = ghostReward
                        # If the cell is food, apply food reward.
                        elif (j, k) in food:
                            reward = foodReward
                        # If the cell is a capsule, apply capsule reward.
                        elif (j, k) in capsules:
                            reward = capsuleReward
                        # If the cell is empty, apply empty space reward.
                        else:
                            reward = emptySpaceReward
                        # Use reward values to apply the utility values for each cell
                        # Use the set value function given in the Grid class. 
                        # Set value takes in the x and y coordinates of the cell, and the value to set the cell to.
                        # We know the first two parameters. We can calculate the utility value by using the Bellman equation.
                        self.map.setValue(
                            j, k, (self.bellmanEquation(j, k, reward)))

    # Bellman equation to calculate the utility of the position (x, y) in the map.
    # We learned this in class and were provided with slides on KEATS
    # Apply utility values to the cells in the grid.

    def bellmanEquation(self, x, y, reward):
        # The Bellman equation is as follows:
        # U(s) = R(s) + gamma * max_a sum_s' T(s, a, s') * U(s')
        # Where:
        # U(s) is the utility value of the state s.
        # R(s) is the reward value of the state s.
        # gamma is the discount factor.
        # max_a is the maximum value of the action a.
        # sum_s' is the sum of the state s'.
        # T(s, a, s') is the transition probability of the state s, action a, and state s'.
        # U(s') is the utility value of the state s'.

        # We need to set a discount factor, also mentioned as gamma.
        # If gamma is closer to 0, the pacman will consider immediate rewards more.
        # If gamma is closer to 1, the pacman will consider future rewards more.
        # Considering immediate rewards is good for the small grid.
        # Considering future rewards is good for the large grid.

        # Gamma value for the small grid.
        if(self.map.getHeight() == 7):
            gamma = 0.6

        # Gamma value for the large grid.
        elif(self.map.getHeight() == 11):
            gamma = 0.7

        # Utility values for actions in case there is a wall
        going_up = -50
        going_down = -50
        going_left = -50
        going_right = -50

        # Check if there is a wall to the right of the current position
        if(self.map.getValue(x + 1, y) != '%'):
            # If there is no wall, set the utility value for the action to the utility value of the cell to the right
            going_right = self.map.getValue(x + 1, y)

        # Check if there is a wall to the left of the current position
        if(self.map.getValue(x - 1, y) != '%'):
            # If there is no wall, set the utility value for the action to the utility value of the cell to the left
            going_left = self.map.getValue(x - 1, y)

        # Check if there is a wall above the current position
        if(self.map.getValue(x, y + 1) != '%'):
            # If there is no wall, set the utility value for the action to the utility value of the cell above
            going_up = self.map.getValue(x, y + 1)

        # Check if there is a wall below the current position
        if(self.map.getValue(x, y - 1) != '%'):
            # If there is no wall, set the utility value for the action to the utility value of the cell below
            going_down = self.map.getValue(x, y - 1)

        # The direction probability in the api is 0.8
        # The rest is divided between three other directions instead of two as taught in class
        # Adding the utility value of the opposite direction increases win rate.
        # Utility values for all directions are calculated and the maximum value is returned later.

        utility_right = api.directionProb * going_right + ((1 - api.directionProb) / 3) * going_up + \
            ((1 - api.directionProb) / 3) * going_down + \
            ((1 - api.directionProb) / 3) * going_left
        utility_left = api.directionProb * going_left + ((1 - api.directionProb) / 3) * going_up + \
            ((1 - api.directionProb) / 3) * going_down + \
            ((1 - api.directionProb) / 3) * going_right
        utility_up = api.directionProb * going_up + ((1 - api.directionProb) / 3) * going_right + \
            ((1 - api.directionProb) / 3) * going_left + \
            ((1 - api.directionProb) / 3) * going_down
        utility_down = api.directionProb * going_down + ((1 - api.directionProb) / 3) * going_right + \
            ((1 - api.directionProb) / 3) * going_left + \
            ((1 - api.directionProb) / 3) * going_up

        # Return the maximum utility value out of the calculated utilities
        utility_max = max(utility_right, utility_left,
                          utility_up, utility_down)
        return reward + (gamma * utility_max)

    # We have utility values on the grid, we need to find the best action to take.
    # Consider how the make move method works in the api.
    # The make move method is non-deterministic, pacman will not always move in the direction that we want.
    # Thus, we get different results running the same code multiple times.
    # The make move method uses directions that are legal for the pacman to move in.
    # We can use the api to get the legal directions for the pacman to move in.
    # When the sample is higher than the direction probability, the pacman will use the select new move method.
    # In both cases, the methods return a direction that is legal for the pacman to move in.
    # So, we need to use or return directions in this method as well.
    def bestMove(self, state):

        # Get the legal directions for the pacman to move in.
        legalMoves = api.legalActions(state)

        # Get the position of the pacman.
        x = state.getPacmanPosition()[0]
        y = state.getPacmanPosition()[1]

        # We want to keep the stop action because of our observations on the small grid.
        # Whenever the pacman is near a food, it goes towards it and sometimes gets stuck inside or tries to exit as
        # quickly as possible. This causes the pacman to go to the ghost. Now, the pacman will stop and wait 
        # for the ghost to pass by.

        # A list of possible actions dependning on the legal directions.
        possible_actions = [] 
        # For every legal action possible, we take the utility value and add it to the actions list.
        for action in legalMoves:
            # The api checks if there is a wall in the proposed direction.
            # It only takes consideration of the utility values if it is possible to move there.
            if action == Directions.EAST:
                # If the action is east, we get the utility value of the cell to the right of the pacman.
                possible_actions.append((action, self.map.getValue(x + 1, y)))
            if action == Directions.WEST:
                # If the action is west, we get the utility value of the cell to the left of the pacman.
                possible_actions.append((action, self.map.getValue(x - 1, y)))
            if action == Directions.NORTH:
                # If the action is north, we get the utility value of the cell above the pacman.
                possible_actions.append((action, self.map.getValue(x, y + 1)))
            if action == Directions.SOUTH:
                # If the action is south, we get the utility value of the cell below the pacman.
                possible_actions.append((action, self.map.getValue(x, y - 1)))
            if action == Directions.STOP:
                # If the action is stop, we get the utility value of the current cell.
                possible_actions.append((action, self.map.getValue(x, y)))        

        # We need to return the action with the highest utility value.
        # To do this, we sort the list of possible actions by the utility value.
        # The list is sorted in descending order.
        # The source for this code is from the following link:
        # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
        # https://stackoverflow.com/questions/3766633/how-to-sort-with-lambda-in-python
        # The first element in the list is the action with the highest utility value.
        possible_actions.sort(key=lambda x: x[1], reverse=True)
        return possible_actions[0][0]
        