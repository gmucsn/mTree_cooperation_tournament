from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random



@directive_enabled_class
class CooperationTitForTatAgent(Agent):
    """
    This class implements an agent which uses the tit for tat strategy which won Axelrod's first tournament
    (Axelrod, 1980). This strategy cooperates on the first move, and then does whatever the other player did 
    on the previous move.
    """
    def __init__(self):
        pass

    @directive_decorator("init_agent")
    def init_agent(self, message: Message):
        """
        This method initializes the agent's variables and replies to the institution once it has been setup

        Message Handled: 
        - "init_agent", sender = institution, payload = none

        Message Sent: 
        - "agent_initialized", receiver = institution, payload = none
        """
        self.institution = None
        self.last_reward = 0
        self.total_reward = 0
        self.choice_history = []
        self.outcome_history = []
        self.First_round = 1
        #send response message
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("agent_initialized")
        self.send(message.get_sender(), new_message)

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
        self.log_data("Agent (tit for tat) Total Reward now: " + str(self.total_reward))


    @directive_decorator("decision_time")
    def item_for_bidding(self, message: Message):
        """
        This method receives the decision_time message and determines which action to take using
        the tit for tat strategy. 

        Message Handled: 
        - 'decision_time', sender = institution, payload = none 

        Message Sent: 
        - 'decision', receiver = institution, payload = {"decision": the decision made, either cooperate or defect}
        """
        self.institution = message.get_sender()
        self.log_message("Agent received request for decision")
        if self.First_round == 1:
            action_decision = "cooperate"
            self.First_round = 0
        else:
            if self.last_reward == 1 or self.last_reward == 0:
                action_decision = "defect"
            else:
                action_decision = "cooperate"
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("decision")
        self.choice_history.append(action_decision)
        new_message.set_payload({"decision": action_decision})
        self.send(self.institution, new_message)  # receiver_of_message, message
