from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random



@directive_enabled_class
class CooperationSimpleAgent(Agent):
    def __init__(self):
        self.institution = None
        self.total_reward = 0
        self.choice_history = []
        self.outcome_history = []

    @directive_decorator("init_agent")
    def init_agent(self, message: Message):
        pass

    @directive_decorator("outcome")
    def outcome(self, message: Message):
        #status = message.get_payload()["status"]
        self.log_data("Outcome: " + str(message.get_payload()))
        self.total_reward += message.get_payload()["reward"]
        self.log_data("Agent Total Reward now: " + str(self.total_reward))


    @directive_decorator("decision time", message_schema=["value"], message_callback="make_bid")
    def item_for_bidding(self, message: Message):
        self.institution = message.get_sender()
        self.log_message("Agent received request for decision")
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("decision")
        new_message.set_payload({"decision": "cooperate"})
        self.send(self.institution, new_message)  # receiver_of_message, message
