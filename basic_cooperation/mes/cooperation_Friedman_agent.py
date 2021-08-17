from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random



@directive_enabled_class
class CooperationFriedmanAgent(Agent):
    """
    This class implements an agent which uses the Friedman strategy from Axelrod's first tournament
    (Axelrod, 1980). This strategy cooperates every round until the other player defects, and then
    it defects for the rest of the game.
    """
    #Friedman cooperates until a defection, then defects for the rest of the game
    def __init__(self):
        self.institution = None
        self.last_reward = 0
        self.total_reward = 0
        self.choice_history = []
        self.outcome_history = []
        self.Defection = 0

    @directive_decorator("init_agent")
    def init_agent(self, message: Message):
        pass

    @directive_decorator("outcome")
    def outcome(self, message: Message):
        """
        This method receives the "outcome" message and updates the agent's total rewards.

        Message Handled:
        - "outcome", sender = institution, 
                    payload = {'outcome': one of four possible outcomes: mutual_cooperate, mutual_defect, sucker, exploiter,
                                "reward": the number of points this agent earned the last round}

        Message Sent:
        - none
        """
        self.log_data("Outcome: " + str(message.get_payload()))
        self.outcome_history.append(message.get_payload()["outcome"])
        self.total_reward += message.get_payload()["reward"]
        self.last_reward = message.get_payload()["reward"]
        self.log_data("Agent (friedman) Total Reward now: " + str(self.total_reward))


    @directive_decorator("decision_time")
    def item_for_bidding(self, message: Message):
        """
        This method receives the decision_time message and determines which action to take using
        the Friedman strategy. 

        Message Handled: 
        - 'decision_time', sender = institution, payload = none 

        Message Sent: 
        - 'decision', receiver = institution, payload = {"decision": the decision made, either cooperate or defect}
        """
        self.institution = message.get_sender()
        self.log_message("Agent received request for decision")
        if self.Defection == 1:
            action_decision = "defect"
        else:
            if self.last_reward == 0:
                action_decision = "defect"
                self.defection = 1
            else:
                action_decision = "cooperate"
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("decision")
        self.choice_history.append(action_decision)
        new_message.set_payload({"decision": action_decision})
        self.send(self.institution, new_message)  # receiver_of_message, message
