from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import logging
import random



@directive_enabled_class
class CooperationTournamentEnvironment(Environment):
    """
    This class implements a simple Prisoner's dilemma institution which sets up the institution and agents.
    """
    def initialize_environment(self):
        self.agent_address_pairs = []
        self.number_of_pairs_remaining = None


    @directive_decorator("start_environment")
    def start_environment(self, message:Message):
        """
        This method starts the environment and calls the start_game method.
        """
        self.log_message("Environment started")
        self.initialize_environment()
        self.make_agent_pairs()
        self.begin_simulation()

    def begin_simulation(self):
        self.start_game(self.agent_address_pairs[self.number_of_pairs_remaining - 1])

    def start_game(self, agent_pair):
        """
        This method sends a message to the institution telling it to start the mes and tells it what
        the agent addresses are for this run.
        """
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("start_game")
        new_message.set_payload({"agents": agent_pair})
        self.send(self.institutions[0], new_message)  # receiver_of_message, message

    def make_agent_pairs(self):
        """
        This method creates a list of agent address pairs from all the given agents so that each
        agent plays one round against every other agent.
        """
        agent_addresses = self.address_book.select_addresses({"address_type": "agent"})
        for x in range(len(agent_addresses)):
            for y in range(x + 1, len(agent_addresses)):
                agent_set = [agent_addresses[x], agent_addresses[y]]
                self.log_message(f"agent_set: {agent_set}")
                self.agent_address_pairs.append(agent_set)
        self.number_of_pairs_remaining = len(self.agent_address_pairs)


    @directive_decorator("game_completed")
    def game_completed(self, message:Message):
        #we reduce the number of agent pairs remaining after the game is complete
        self.number_of_pairs_remaining = self.number_of_pairs_remaining - 1
        if self.number_of_pairs_remaining == 0:
            #we have completed all the games
            self.log_message("simulation_complete")
        else:
            self.start_game(self.agent_address_pairs[self.number_of_pairs_remaining - 1])





    