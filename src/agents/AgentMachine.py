
from pade.core.agent import Agent
from pade.misc.utility import display_message
from pade.acl.filters import Filter as f
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaSubscribeProtocol
from utils.DummyTime import DummyTime


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

    def react(self, message):
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
                if(len(self.play_list) == 0):
                    print('-------------------')
                self.play_list.append(
                    {'play': message.content, 'player': message.sender.name})
                print('{} fez sua jogada!'.format(message.sender.name))
        if len(self.play_list) == 2:
            print('{} vs {}'.format(
                self.play_list[0]['player'], self.play_list[1]['player']))
            if self.play_list[0]['play'] == False and self.play_list[1]['play'] == False:
                print('Ninguem roubou!')
            elif self.play_list[0]['play'] == True and self.play_list[1]['play'] == False:
                print('{} roubou!'.format(self.play_list[0]['player']))
            elif self.play_list[0]['play'] == False and self.play_list[1]['play'] == True:
                print('{} roubou!'.format(self.play_list[1]['player']))
            elif self.play_list[0]['play'] == True and self.play_list[1]['play'] == True:
                print('Os dois roubaram!')
            self.play_list = []
        pass


class MachineProtocol(FipaSubscribeProtocol):
    def __init__(self, agent):
        super(MachineProtocol, self).__init__(agent,
                                              message=None,
                                              is_initiator=False)

    def handle_subscribe(self, message):
        self.register(message.sender)
        resposta = message.create_reply()
        resposta.set_performative(ACLMessage.AGREE)
        self.agent.send(resposta)

    def handle_cancel(self, message):
        self.deregister(self, message.sender)
        display_message(self.agent.aid.name, message.content)

    def notify(self, message):
        display_message(self.agent.aid.name, '')
        super(MachineProtocol, self).notify(message)
