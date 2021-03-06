from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random



@directive_enabled_class
class CooperationNydeggerAgent(Agent):
    #nydegger agent does not work correctly presently
    """
    This class implements an agent which uses the Nydegger strategy from Axelrod's first tournament
    (Axelrod, 1980). This strategy Plays tit for tat for the first three moves, unless it is the only 
    one to cooperate on the first move and the only one to defect on the second move, then it defects 
    on the third move. After the third move, its choice is determined from the 3 preceding outcomes 
    in the following manner. Let A be the sum formed by counting the other's defection as 2 points and 
    one's own as 1 point, and giving weights of 16, 4, and 1 to the preceding three moves in chronological order. 
    The choice can be described as defecting only when A equals 1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 
    45, 49, 54, 55, 58, or 61.
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
        self.round_number = 1
        self.decision_list = [1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, 61]
        self.values_list = [0, 0, 0]
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
        self.log_data("Agent (nydegger) Total Reward now: " + str(self.total_reward))


    @directive_decorator("decision_time")
    def decision_time(self, message: Message):
        """
        This method receives the decision_time message and determines which action to take using
        the Nydegger strategy. 

        Message Handled: 
        - 'decision_time', sender = institution, payload = none 

        Message Sent: 
        - 'decision', receiver = institution, payload = {"decision": the decision made, either cooperate or defect}
        """
        self.institution = message.get_sender()
        self.log_message("Agent received request for decision")
        if self.round_number != 0:
            if self.round_number == 1:
                action_decision = "cooperate"
                self.round_number = 2
            else:
                if self.round_number == 2:
                    self.round_number = 3
                    if self.last_reward == 1 or self.last_reward == 0:
                        action_decision = "defect"
                    else:
                        action_decision = "cooperate"
                else:
                    self.round_number = 0
                    if self.outcome_history[0] == "sucker" and self.outcome_history[1] == "exploiter":
                        action_decision = "defect"
                    else:
                        if self.last_reward == 1 or self.last_reward == 0:
                            action_decision = "defect"
                        else:
                            action_decision = "cooperate" 
        else:
            for x in [-1, -2, -3]:
                if self.outcome_history[x] == "mutual_cooperate":
                    self.values_list[x] = 0
                if self.outcome_history[x] == "mutual_defect":
                    self.values_list[x] = 3
                if self.outcome_history[x] == "sucker":
                    self.outcome_history[x] = 2
                if self.outcome_history[x] == "exploiter":
                    self.values_list[x] = 1

                if x == -2:
                    self.values_list[x] *= 4
                if x == -3:
                    self.values_list[x] *= 16
            value_total = self.values_list[0] + self.values_list[1] + self.values_list[2]
            if value_total in self.decision_list:
                action_decision = "defect"
            else:
                action_decision = "cooperate"
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("decision")
        self.choice_history.append(action_decision)
        new_message.set_payload({"decision": action_decision})
        self.send(self.institution, new_message)  # receiver_of_message, message
