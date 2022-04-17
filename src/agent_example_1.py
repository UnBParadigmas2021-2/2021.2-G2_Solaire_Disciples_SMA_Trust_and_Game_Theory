import random
from pade.misc.utility import display_message, start_loop
from pade.behaviours.protocols import FipaSubscribeProtocol, TimedBehaviour
from pade.core.agent import Agent
from pade.acl.filters import Filter as f
from pade.acl.messages import ACLMessage
from pprint import pprint
from pade.acl.aid import AID
from sys import argv
from itertools import groupby
from itertools import combinations


class DummyTime(TimedBehaviour):

    def __init__(self, agent, notify):
        super(DummyTime, self).__init__(agent, 1)
        self.notify = notify
        self.inc = 0

    def on_time(self):
        super(DummyTime, self).on_time()
        print('timed_message')
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        message.set_content(str(random.random()))
        self.notify(message)
        self.inc += 0.1


class MachineSubscriptionProtocol(FipaSubscribeProtocol):

    def __init__(self, agent):
        super(MachineSubscriptionProtocol, self).__init__(agent,
                                                          message=None,
                                                          is_initiator=False)

    def handle_subscribe(self, message):
        self.register(message.sender)
        print('sub recebido')
        display_message(self.agent.aid.name,
                        message.content)
        resposta = message.create_reply()
        resposta.set_performative(ACLMessage.AGREE)
        resposta.set_content('Subscribe message accepted')

        self.agent.send(resposta)

    def handle_cancel(self, message):
        self.deregister(self, message.sender)
        display_message(self.agent.aid.name, message.content)

    def notify(self, message):
        display_message(self.agent.aid.name, 'Notifying')
        super(MachineSubscriptionProtocol, self).notify(message)


class AgentMachine(Agent):
    play_list = list()

    def __init__(self, aid):
        super(AgentMachine, self).__init__(aid=aid)
        display_message(self.aid.localname, 'BEEP BOOP! Im the MACHINE!')
        self.machine_subscription_protocol = MachineSubscriptionProtocol(self)
        self.dummy_timed_message = DummyTime(self,
                                             self.machine_subscription_protocol.notify)

        self.behaviours.append(self.machine_subscription_protocol)
        self.behaviours.append(self.dummy_timed_message)

    # def on_start(self):
    #     message = ACLMessage(ACLMessage.REQUEST)
    #     # message.set_performative()
    #     # message.add_receiver(AID(self.match[0]))
    #     # message.add_receiver(AID(self.match[1]))
    #     message.set_content(
    #         'Jogador {} e {}, Façam suas escolhas!'.format(str(match[0]),
    #                                                        str(match[1])))
    #     self.notify(message)

    def react(self, message):
        super(AgentMachine, self).react(message)
        print('react machine')
        filter = f()
        filter.performative = ACLMessage.REQUEST
        if filter.filter(message=message):

            print('message is request')
            print(message.content)

            reply = message.create_reply()
            reply.set_performative(ACLMessage.AGREE)
            reply.add_receiver(message.sender)
            self.send(reply)
        # display_message(self.aid.localname, message)
        pass


class PlayerProtocol(FipaSubscribeProtocol):
    def __init__(self, machine, message):
        super(PlayerProtocol, self).__init__(machine,
                                                    message)

    def handle_agree(self, message):
        display_message(self.agent.aid.name, message.content)

    def handle_inform(self, message):
        # display_message(self.agent.aid.name, message.content)
        print('inform recebido')

    def handle_request(self, message):
        print('aaaaaaaaaaaa')
        display_message(self.aid.localname,
                        'Mensagem recebida, preparando jogada')
        reply = message.create_reply()
        reply.set_content(True)
        reply.set_performative(ACLMessage.INFORM)
        self.agent.send(reply)


class AgentPlayer(Agent):
    def __init__(self, aid, machine, persona):
        super(AgentPlayer, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hello World! Im a BasePlayer!')
        self.call_later(8.0, self.launch_subscriber_protocol)
        self.machine = machine
        self.persona = persona

    def launch_subscriber_protocol(self):
        print('launch subscriber protocol')
        msg = ACLMessage(ACLMessage.SUBSCRIBE)
        msg.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        msg.set_content('Subscription request')
        msg.set_sender(self.aid)
        msg.add_receiver(self.machine.aid)

        self.protocol = PlayerProtocol(self.machine, msg)
        self.behaviours.append(self.protocol)
        self.protocol.on_start()

    # def react(self, message):
    #     display_message(self.aid.localname,
    #                     'Mensagem recebida, preparando jogada')
    #
    #     # from pprint import pprint; pprint(message.__dict__)
    #     # pprint(self.persona)
    #     pass


# class Cooperator(Agent):
#     def __init__(self, aid):
#         super(Cooperator, self).__init__(aid=aid)
#         display_message(self.aid.localname,
#                         'Hello World! Im a COOPERATOR! I ALWAYS COOPERATE')
#
#     def react(self, message):
#         pprint(self.__class__.__name__)
#         pprint(message.__dict__)
#         display_message(self.aid.localname, 'Mensagem recebida')
#
#
# class Cheater(Agent):
#     def __init__(self, aid):
#         super(Cheater, self).__init__(aid=aid)
#         display_message(self.aid.localname,
#                         'Hello World! Im a CHEATER! I ALWAYS CHEAT')
#
#     def react(self, message):
#         pprint(self.__class__.__name__)
#         pprint(message.__dict__)
#         display_message(self.aid.localname, 'Mensagem recebida')


if __name__ == '__main__':
    cheater = 1
    cooperator = 1
    c = 0
    agents = list()
    player_names = list()

    port = int(argv[1]) + c
    machine_name = 'machine_{}@localhost:{}'.format(port, port)
    machine_instance = AgentMachine(AID(name=machine_name))
    agents.append(machine_instance)
    c += 1

    for i in range(cooperator):
        port = int(argv[1]) + c
        cooperator_name = 'copycat_{}@localhost:{}'.format(port, port)
        cooperator_init = AgentPlayer(AID(name=cooperator_name),
                                      machine=machine_instance,
                                      persona='Copycat')
        player_names.append(cooperator_name)
        agents.append(cooperator_init)
        c += 1

    for i in range(cheater):
        port = int(argv[1]) + c
        cheater_name = 'cheater_{}@localhost:{}'.format(port, port)
        cheater_init = AgentPlayer(AID(name=cheater_name),
                                   machine=machine_instance,
                                   persona='Cheater')
        player_names.append(cheater_name)
        agents.append(cheater_init)
        c += 1

    start_loop(agents)
