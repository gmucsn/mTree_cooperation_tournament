from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random



@directive_enabled_class
class CooperationGraaskampAgent(Agent):
    """
    This class implements an agent which uses the Graaskamp strategy from Axelrod's first tournament
    (Axelrod, 1980). This strategy Plays tit for tat for 50 moves, defects once, then plays tit for tat 
    for another 5 moves. Checks to see if it is playing itself or tit for tat, if so it plays accordingly. 
    If its score is bad it assumes it is playing random and defects for the rest of the game. Otherwise it 
    plays tit for tat but throws in a defection every 5 to 15 moves.
    """
    def __init__(self):
        self.institution = None
        self.last_reward = 0
        self.total_reward = 0
        self.choice_history = []
        self.outcome_history = []
        self.round_number = 0
        self.state = "default"

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
        self.round_number = 0
        self.state = "default"
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
        #status = message.get_payload()["status"]
        self.log_data("Outcome: " + str(message.get_payload()))
        self.outcome_history.append(message.get_payload()["outcome"])
        self.total_reward += message.get_payload()["reward"]
        self.last_reward = message.get_payload()["reward"]
        self.log_data("Agent (graaskamp) Total Reward now: " + str(self.total_reward))


    @directive_decorator("decision_time")
    def item_for_bidding(self, message: Message):
        """
        This method receives the decision_time message and determines which action to take using
        the Graaskamp strategy. 

        Message Handled: 
        - 'decision_time', sender = institution, payload = none 

        Message Sent: 
        - 'decision', receiver = institution, payload = {"decision": the decision made, either cooperate or defect}
        """
        self.institution = message.get_sender()
        self.log_message("Agent received request for decision")
        self.round_number += 1
        if self.round_number == 1:
            action_decision = "cooperate"
        else:
            if self.round_number > 1 and self.round_number < 50:
                if self.last_reward == 1 or self.last_reward == 0:
                    action_decision = "defect"
                else:
                    action_decision = "cooperate"
            else:
                if self.round_number == 50:
                    action_decision = "defect"
                else:
                    if self.round_number > 50 and self.round_number < 56:
                        if self.last_reward == 1 or self.last_reward == 0:
                            action_decision = "defect"
                        else:
                            action_decision = "cooperate"
                    else:
                        if self.round_number == 56:
                            defection_positions = []
                            for x in range(56):
                                #TODO: there's a bug that needs to be fixed here (list index out of range)
                                if self.outcome_history[x] == "mutual_defect" or self.outcome_history[x] == "sucker":
                                    defection_positions.append(x)
                            if len(defection_positions) == 1 and defection_positions[0] == 50:
                                self.state = "tit_for_tat"
                            else:
                                if len(defection_positions) and defection_positions[0] == 51 and defection_positions[1] == 53 and defection_positions[2] == 55:
                                    self.state = "tit_for_tat"
                                else:
                                    if len(defection_positions) > 20 and len(defection_positions) < 34:
                                        self.state = "defect"
                                    else: 
                                        self.state = "default"
                            if self.state == "tit_for_tat":
                                action_decision = "cooperate"
                            else: 
                                action_decision = "defect"
        if self.round_number > 56:
            if self.state == "tit_for_tat":
                if self.last_reward == 1 or self.last_reward == 0:
                    action_decision = "defect"
                else:
                    action_decision = "cooperate"
            else:
                if self.state == "defect":
                    action_decision = "defect"
                else: 
                    broke_loop = "false"
                    for x in [-1,-2,-3,-4,-5]:
                        if self.outcome_history[x] == "mutual_defect" or self.outcome_history[x] == "exploiter":
                            if self.last_reward == 1 or self.last_reward == 0:
                                action_decision = "defect"
                            else:
                                action_decision = "cooperate"
                            broke_loop = "true"
                            break
                    if broke_loop == "true":
                        pass
                    else:
                        if self.last_reward == 1 or self.last_reward == 0:
                            action_decision = "defect"
                        else:
                            if random.choice(range(1,11)) == 1:
                                action_decision = "defect"
                            else:
                                action_decision = "cooperate"
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("decision")
        self.choice_history.append(action_decision)
        new_message.set_payload({"decision": action_decision})
        self.send(self.institution, new_message)  # receiver_of_message, message