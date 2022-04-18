
from pade.core.agent import Agent
from pade.misc.utility import display_message
from pade.acl.filters import Filter as f
from pade.acl.messages import ACLMessage

from utils.DummyTime import DummyTime
from utils.MachineProtocol import MachineProtocol


class AgentMachine(Agent):
   play_list = list()

   def __init__(self, aid):
      super(AgentMachine, self).__init__(aid=aid)
      display_message(self.aid.localname, 'BEEP BOOP! Im the MACHINE!')
      self.machine_subscription_protocol = MachineProtocol(self)
      self.dummy_timed_message = DummyTime(self,
                                          self.machine_subscription_protocol.notify)

      self.behaviours.append(self.machine_subscription_protocol)
      self.behaviours.append(self.dummy_timed_message)

   def react(self, message: ACLMessage):
      super(AgentMachine, self).react(message)
      filter = f()
      filter.performative = ACLMessage.REQUEST

      if filter.filter(message=message):
         reply = message.create_reply()
         reply.set_performative(ACLMessage.AGREE)
         reply.add_receiver(message.sender)
         self.send(reply)

      else:
         if(isinstance(message.content, bool)):
               self.play_list.append({'play': message.content, 'player': message.sender.name})
      
      if len(self.play_list) == 2:
         print('{} vs {}'.format(self.play_list[0]['player'], self.play_list[1]['player']))
         
         if self.play_list[0]['play'] == False and self.play_list[1]['play'] == False:
               print('Ninguem roubou!')
               # ambos recebem 3 moedas
               # message.set_message("+3coins")
               # reply = message.create_reply()
               # reply.set_performative(ACLMessage.REFUSE)
               # reply.add_receiver(message.sender)
               # self.send(reply)
         
         elif self.play_list[0]['play'] == True and self.play_list[1]['play'] == False:
               print('{} roubou!'.format(self.play_list[0]['player']))
         
         elif self.play_list[0]['play'] == False and self.play_list[1]['play'] == True:
               print('{} roubou!'.format(self.play_list[1]['player']))
         
         elif self.play_list[0]['play'] == True and self.play_list[1]['play'] == True:
               print('Os dois roubaram!')
         
         self.play_list= []
      # display_message(self.aid.localname, message)
      pass

   # def on_start(self):
   #     message = ACLMessage(ACLMessage.REQUEST)
   #     # message.set_performative()
   #     # message.add_receiver(AID(self.match[0]))
   #     # message.add_receiver(AID(self.match[1]))
   #     message.set_content(
   #         'Jogador {} e {}, Façam suas escolhas!'.format(str(match[0]),
   #                                                        str(match[1])))
   #     self.notify(message)
