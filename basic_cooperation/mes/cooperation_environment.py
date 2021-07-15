from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.components.property_types import MTreeBoolProperty, MTreeIntProperty, MTreeRealProperty, MTreeSetProperty
from mTree.microeconomic_system.property_decorators import *
import logging
import random



@directive_enabled_class#(expected_properties=[agent_endowment, "num_auctions"])
class CooperationEnvironment(Environment):
    """
    This class implements a simple Prisoner's dilemma institution which sets up the institution and agents.
    """
    def __init__(self):
        self.num_auctions = 10

    @directive_decorator("start_environment")
    def start_environment(self, message:Message):
        self.log_message("Environment started")
        self.start_game()

    def start_game(self):
        """
        This method sends a message to the institution telling it to start the mes and tells it what
        the agent addresses are.
        """
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("start_game")
        new_message.set_payload({"agents": self.agent_addresses})
        self.send(self.institutions[0], new_message)  # receiver_of_message, message

    