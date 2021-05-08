from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random



@directive_enabled_class
class CooperationEatherleyAgent(Agent):
    #Eatherley always cooperates after cooperation, but defects after defection with a propability equal to the ration of the other player's defections to total moves
    def __init__(self):
        self.institution = None
        self.last_reward = 0
        self.total_reward = 0
        self.choice_history = []
        self.outcome_history = []
        self.enemy_defections = 0
        self.First_round = 1

    @directive_decorator("init_agent")
    def init_agent(self, message: Message):
        pass

    @directive_decorator("outcome")
    def outcome(self, message: Message):
        #status = message.get_payload()["status"]
        self.log_data("Outcome: " + str(message.get_payload()))
        self.outcome_history.append(message.get_payload()["outcome"])
        self.total_reward += message.get_payload()["reward"]
        self.last_reward = message.get_payload()["reward"]
        self.log_data("Agent (eatherley) Total Reward now: " + str(self.total_reward))
        if self.last_reward == 1 or self.last_reward == 0:
            self.enemy_defections += 1


    @directive_decorator("decision time", message_schema=["value"], message_callback="make_bid")
    def item_for_bidding(self, message: Message):
        self.institution = message.get_sender()
        self.log_message("Agent received request for decision")
        if self.First_round == 1:
            action_decision = "cooperate"
            self.First_round = 0
        else:
            if self.last_reward == 1 or self.last_reward == 0:
                if random.choice(range(1,len(self.outcome_history))) <= self.enemy_defections:
                    action_decision = "defect"
                else:
                    action_decision = "cooperate"
            else:
                action_decision = "cooperate"

        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("decision")
        self.choice_history.append(action_decision)
        new_message.set_payload({"decision": action_decision})
        self.send(self.institution, new_message)  # receiver_of_message, message
