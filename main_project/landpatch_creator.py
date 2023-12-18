"""
This module provides classes for representing different landpatches. Landpatch is the base class and extends to the subclasses Rockpatch and Treepatch

Furthermore, this module provides the Firefighter class. 

Requirements
#TODO
------------
Package matplotlib https://matplotlib.org/ which can be installed via PIP.
Package networkx https://networkx.org/ which can be installed via PIP.
Python 3.7 or higher.



Notes
-----
This module is created as material for the phase 2 project for DM857, DS830 (2023). 
"""
from typing import List, Optional, Dict
import random


class Landpatch():
    """This is the base class for representing a patch of land as a vertex of a graph"""

    def __init__(self) -> None:
        pass

        """
        Parameters
        ----------
        # TODO
        """

    # Class methods

    def mutate_landpatch(self):
        """Allows for swapping the subtype of the landpatch without loosing connection to neighbors and associations with firefighters, 
        eg. if initial instance is classified as a Rockpatch, swapped instance is then Treepatch
        """

        # TODO
        print("The landpatch has been swapped")

    def next_neighbours_ID(self):
        """Return the ID of the next neighbors to the present patch"""
        # TODO
        print("This returns the next neighbors to the present patch")


class Rockpatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Rockpatch"""

    def __init__(self, greening_state: Optional[int]) -> None:
        super().__init__()
        # TODO
        """
        Parameters
        greening_state: Optional[int]
            Attribute that represents the rockpatches current level of greening. Used to increase probability of becoming a Treepatch
        ----------
        # TODO
        """
        self._greening_state = greening_state

    def mutate(self):
        """Allows swapping a Rockpatch with a Treepatch without losing connections to neighbors and associations with firefighters."""
        ## Each Rockpatch has a possibility of becoming a Treepatch at each step (default 1%).
        if random.random() < 0.01:
            self.mutate_landpatch(Treepatch)
            print("The Rockpatch has mutated into a Treepatch.")

    def update_greens(self):
        """Updates the greening state of the rockpatch over time."""
        #huh? does the rockpatch green over time?
        # TODO: Implement the logic for updating the greening state
        print("The greening state of the Rockpatch has been updated.")

    def __str__(self):
        return f"Rockpatch(Greening State: {self._greening_state})"


class Treepatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Treepatch"""

    def __init__(self, tree_health: Optional[int]) -> None:
        super().__init__()
        # TODO
        """
        Parameters
        ----------
        tree_health: Optional[int]
            Attribute identifies the current health of the treepatch [0-256]
        # TODO
        """

        self._tree_health = tree_health
        self._ignited = False

    # Methods
    # TODO
    def updateland(self):
        if not self._ignited:
            self._tree_health += 10
        else:
            self._tree_health -= 20

        if self._tree_health < 0:
            self.mutate_landpatch(Rockpatch)
        print("Treestats has been updated.")

    def spread_fire(self):
        """With probability 30%, spread fire to adjacent Treepatch"""
        # Possibly goes on the graph constructor class instance and not here... Not sure yet.
        if random.random() < 0.3:
            # Get the neighbors of the current Treepatch
            neighbors = self.next_neighbours_ID()

            #Ignites adjacents treepatches not already on fire
            for neighbor in neighbors:
                if not neighbor._ignited:
                    neighbor._ignited = True

            print("Fire has spread to adjacent Treepatch")


class Firefighter():
    """Each instance of this class creates a firefighter for extingushing fires in a graph of landpatches"""

    def __init__(self, firefighter_skill: Optional[float] = 1, health: Optional[float] = 100) -> None:
        pass
        # TODO
        """
        Parameters
        ----------
        # TODO
        firefighter_skill: Optional[float]
            represents the instance of firefighters' ability to extinguish fires on a Treepatch
        health: Optional[float], default = 100
            represents the instance of firefighters' current health
        """

        self._firefighter_skill = firefighter_skill
        self._health = health

    # methods
    def extinguish_fire(self):
        """Based on firefighter_skill, extinguishes fire if toggled on Treepatch"""
        # TODO

        print("Hastala no burn today")

    def move_firefighter(self):
        """Firefighter moves to adjacent patch. Will prioritize adjacent Treepatch is ignited, else at random"""
        # Possibly on graph class. Unsure if the logic here can be carried to elsewhere
        # TODO
        print("Firefighter has moved to adjacent patch")

    def update_health(self):
        """Updates the current instance of firefighters health."""
        # TODO
        # If current instance of class firefighter is on ignited landpatch, update health by - 10
        # If current instance of class firefighter is NOT on ignited landpatch, update health by + 5

