from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random



@directive_enabled_class
class CooperationChampionAgent(Agent):
    #Cooperates on the first 10 moves, then plays tit for tat for the next 15 moves. 
    #After these first 25 moves it cooperates unless all of the following are true: 
    #1. The other player defected on the previous move, 2. The other player has cooperated less than 60% of the time, 3. The random number between 0 and 1 is greater than the other player’s cooperation rate. 
    def __init__(self):
        self.institution = None
        self.last_reward = 0
        self.total_reward = 0
        self.choice_history = []
        self.outcome_history = []
        self.round_number = 1
        self.enemy_defections = 0

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
        self.log_data("Agent (champion) Total Reward now: " + str(self.total_reward))
        if self.last_reward == 1 or self.last_reward == 0:
            self.enemy_defections += 1


    @directive_decorator("decision time", message_schema=["value"], message_callback="make_bid")
    def item_for_bidding(self, message: Message):
        self.institution = message.get_sender()
        self.log_message("Agent received request for decision")
        if self.round_number <= 10:
            action_decision = "cooperate"
            self.round_number += 1
        else:
            if self.round_number <= 25 and self.round_number >= 11:
                if self.last_reward == 1 or self.last_reward == 0:
                    action_decision = "defect"
                else:
                    action_decision = "cooperate"
                self.round_number += 1
            else: 
                cooperation_rate = self.enemy_defections / len(self.outcome_history)
                if (self.last_reward == 1 or self.last_reward == 0) and cooperation_rate > .6 and random.uniform(0, 1) > cooperation_rate:
                    action_decision = "defect"
                else:
                    action_decision = "cooperate"
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("decision")
        self.choice_history.append(action_decision)
        new_message.set_payload({"decision": action_decision})
        self.send(self.institution, new_message)  # receiver_of_message, message
