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

    def test(self) -> bool:
        """test if created"""
        return True


class Rockpatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Rockpatch"""

    def __init__(self, greening_state: Optional[int] = 0) -> None:
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

    def __init__(self, tree_health: Optional[int]= 100) -> None:
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
        self._current_patch = None

    # methods
    def extinguish_fire(self, treepatch):
        """Based on firefighter_skill, extinguishes fire if toggled on Treepatch"""
        if treepatch._ignited:
            extinguish_probability = self._firefighter_skill
            if random.random() < extinguish_probability:
                treepatch._ignited = False
                print("Fire extinguished by firefighter.")
            else:
                print("Firefighter failed to extinguish fire.")

    def move_firefighter(self):
        if self._current_patch is not None:
            neighbors = self._current_patch.next_neighbours_ID()
            #TODO add logic for staying at patch until fire is gone

            # Check if there are adjacent Treepatches on fire
            adjacent_fire_patches = [neighbor for neighbor in neighbors if
                                     isinstance(neighbor, Treepatch) and neighbor._ignited]

            if adjacent_fire_patches:
                # Move to a random adjacent Treepatch on fire
                new_location = random.choice(adjacent_fire_patches)
            else:
                # Move to a random adjacent patch
                new_location = random.choice(neighbors)

            print(f"Firefighter moved from {self._current_patch} to {new_location}.")
            self._current_patch = new_location
        else:
            print("Firefighter has no current location.")

    def update_health(self, current_patch):
        """Updates the current instance of firefighter's health."""
        if current_patch._ignited:
            self._health -= 10
        else:
            self._health += 5
        print(f"Firefighter health updated to {self._health}.")
