from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import math
import random



@directive_enabled_class
class CooperationInstitution(Institution):
    def __init__(self):
        self.rounds = 200

        self.agents = None


    @directive_decorator("init_institution")
    def init_institution(self, message:Message):
        if self.debug:
            print("Institution: received institution init ...")

    @directive_decorator("decision")
    def decision(self, message:Message):
        agent_decision = message.get_payload()["decision"]
        self.actions.append((agent_decision, message.get_sender()))
        self.actions_outstanding -= 1
        if self.actions_outstanding == 0:
            self.end_round()
            self.next_round()

    def end_round(self):
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
        if self.rounds > 0:
            self.log_message("Round started: " + str(self.rounds))
        
            self.rounds -= 1
            self.actions = []
            self.actions_outstanding = len(self.agents)
            
            for agent in self.agents:
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_directive("decision time")
                self.send(agent, new_message)  # receiver_of_message, message
    
        
    @directive_decorator("start_game", message_schema=["agents"], message_callback="send_agents_start")
    def start_game(self, message:Message):
        self.agents = message.get_payload()["agents"]
        self.next_round()
