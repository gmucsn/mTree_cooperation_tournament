from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import logging
import random



@directive_enabled_class
class CooperationEnvironment(Environment):
    """
    This class implements a simple Prisoner's dilemma institution which sets up the institution and agents.
    """
    def __init__(self):
        pass

    @directive_decorator("start_environment")
    def start_environment(self, message:Message):
        """
        This method starts the environment and calls the start_game method.
        """
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

    