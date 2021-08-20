from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import math
import random



@directive_enabled_class
class CooperationInstitution(Institution):
    """
    This class implements a simple Prisoner's dilemma institution that takes the decisions made by
    two different agents and informs them of the results of the round.
    """
    def __init__(self):

        self.agents = None


    @directive_decorator("init_institution")
    def init_institution(self, message:Message):
        if self.debug:
            print("Institution: received institution init ...")

    @directive_decorator("decision")
    def decision(self, message:Message):
        """
        This method handles the agents sending their decisions to the institution and calls the end_round
        and next_round methods once both agents have responded (tracked using the actions_outstanding variable)
        """
        agent_decision = message.get_payload()["decision"]
        self.actions.append((agent_decision, message.get_sender()))
        self.actions_outstanding -= 1
        if self.actions_outstanding == 0:
            self.end_round()
            self.next_round()

    def end_round(self):
        """
        This method ends the round, figures out the result, and sends the results to both agents.

        Message Handled:
        - none

        Message sent:
        - "outcome", receiver = agents, 
                    payload = {"outcome": one of four possible outcomes: mutual_cooperate, mutual_defect, sucker, exploiter,
                                "reward": the number of points an agent earned this round}
        """
        if self.actions[0][0] == self.actions[1][0]:
            new_message = Message()  # declare message
            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
            new_message.set_directive("outcome")
            
            if self.actions[0][0] == "cooperate":
                new_message.set_payload({"outcome": "mutual_cooperate",
                    "reward": 3})
            else:
                new_message.set_payload({"outcome": "mutual_defect",
                    "reward": 1})
            for agent in self.agents:
                self.send(agent, new_message)  # receiver_of_message, message
        else:
            cooperate_message = Message()  # declare message
            cooperate_message.set_sender(self.myAddress)  # set the sender of message to this actor
            cooperate_message.set_directive("outcome")
            cooperate_message.set_payload({"outcome": "sucker",
                    "reward": 0})
            defect_message = Message()  # declare message
            defect_message.set_sender(self.myAddress)  # set the sender of message to this actor
            defect_message.set_directive("outcome")
            defect_message.set_payload({"outcome": "exploiter",
                    "reward": 5})
            if self.actions[0][0] == "cooperate":
                self.send(self.actions[0][1], cooperate_message)
                self.send(self.actions[1][1], defect_message)
            else:
                self.send(self.actions[1][1], cooperate_message)
                self.send(self.actions[0][1], defect_message)


    def next_round(self):
        """
        This method begins the next round of the simulation by reducing the number of remaining
        rounds by 1 and reseting the actions_outstanding variable, and then sending the 
        decision_time message to both agents.

        Message Handled:
        - none

        Message sent:
        - "decision_time", receiver = agents, payload = none
        """
        if self.rounds > 0:
            self.log_message("Round started: " + str(self.rounds))
        
            self.rounds -= 1
            self.actions = []
            self.actions_outstanding = len(self.agents)
            
            for agent in self.agents:
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_directive("decision_time")
                self.send(agent, new_message)  # receiver_of_message, message
        else:
            #we have completed this game
            new_message = Message()  # declare message
            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
            new_message.set_directive("game_completed")
            self.send(self.environment_address, new_message)  # receiver_of_message, message
    
        
    @directive_decorator("start_game")
    def start_game(self, message:Message):
        """
        This method gets the agent addresses and starts the game by calling the next_round method.

        Message Handled:
        - 'start_game', sender = environment,
                    payload = {"agents": a list of the agent addresses}

        Message Sent:
        - none
        """
        self.environment_address = message.get_sender()
        self.agents = message.get_payload()["agents"]
        self.rounds = 200
        self.next_round()
