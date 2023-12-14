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
        #TODO
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
        # Methods
        # TODO   

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
        """Updates the value of treestats due to fire or firefighter action for one evolution step"""
        #TODO
        # if not ignited, update tree_health + 10
        # if ignited, update tree_health - 20
        # if tree_health < 0, mutate to Rockpatch
        print("Treestats has been updated.")
    
    def spread_fire(self):
        """With probability 30%, spread fire to adjacent Treepatch"""
        # Possibly goes on the graph constructor class instance and not here... Not sure yet.
        # TODO 
        print("Fire has spread to adjacent Treepatch")

class Firefighter():
    """Each instance of this class creates a firefighter for extingushing fires in a graph of landpatches"""

    def __init__(self, firefighter_skill: Optional[float] = 1, health: Optional[float]=100) -> None:
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
        print("Firefighter has moves to adjacent patch")
    
    def update_health(self):
        """Updates the current instance of firefighters health."""
        # TODO
        # If current instance of class firefighter is on ignited landpatch, update health by - 10
        # If current instance of class firefighter is NOT on ignited landpatch, update health by + 5
    
