from pade.misc.utility import display_message, start_loop
from pade.behaviours.protocols import FipaSubscribeProtocol, TimedBehaviour
from pade.core.agent import Agent
from pade.acl.filters import Filter as f
from pade.acl.messages import ACLMessage
from pprint import pprint
from pade.acl.aid import AID
from sys import argv


class DummyTime(TimedBehaviour):

    def __init__(self, agent, notify):
        super(DummyTime, self).__init__(agent, 1)
        self.notify = notify
        self.inc = 0

    def on_time(self):
        super(DummyTime, self).on_time()
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        self.notify(message)
        self.inc += 0.1


class MachineProtocol(FipaSubscribeProtocol):

    def __init__(self, agent):
        super(MachineProtocol, self).__init__(agent,
                                              message=None,
                                              is_initiator=False)

    def handle_subscribe(self, message):
        self.register(message.sender)
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
        super(MachineProtocol, self).notify(message)


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
            elif self.play_list[0]['play'] == True and self.play_list[1]['play'] == False:
                print('{} roubou!'.format(self.play_list[0]['player']))
            elif self.play_list[0]['play'] == False and self.play_list[1]['play'] == True:
                print('{} roubou!'.format(self.play_list[1]['player']))
            elif self.play_list[0]['play'] == True and self.play_list[1]['play'] == True:
                print('Os dois roubaram!')
            self.play_list= []
        # display_message(self.aid.localname, message)
        pass


class PlayerProtocol(FipaSubscribeProtocol):
    def __init__(self, machine, message, persona):
        super(PlayerProtocol, self).__init__(machine,
                                             message)
        self.persona=persona

    def handle_agree(self, message):
        display_message(self.agent.aid.name, message.content)

    def handle_inform(self, message):
        reply=message.create_reply()
        pprint('{} está escolhendo'.format(self.agent.aid.name))
        if(self.persona == 'Cooperator'):
            reply.set_content(False)
        elif(self.persona == 'Cheater'):
            reply.set_content(True)
        # TO-DO: elif is Copycat
        # TO-DO: elif is Grudger
        reply.set_performative(ACLMessage.INFORM)
        self.agent.send(reply)


class AgentPlayer(Agent):
    def __init__(self, aid, machine, persona):
        super(AgentPlayer, self).__init__(aid = aid)
        display_message(self.aid.localname,
                        'Hello World! Im a/an ' + persona)
        self.call_later(8.0, self.launch_subscriber_protocol)
        self.machine = machine
        self.persona = persona

    def launch_subscriber_protocol(self):
        print('launch subscriber protocol')
        msg = ACLMessage(ACLMessage.SUBSCRIBE)
        msg.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        msg.set_content('Subscription request')
        msg.add_receiver(self.machine.aid)

        self.protocol = PlayerProtocol(self, msg, self.persona)
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


class Copycat(Agent):
    def __init__(self, aid):
        super(Copycat, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hi! Im a Copycat: I start cooperating, then I simply \
                        repeat whatever my adversary did in the last round')


class Grudger(Agent):
    def __init__(self, aid):
        super(Copycat, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hi! Im a Grudger: I will cooperate... unless my \
                        adversary cheats on me (then I will always cheat)!')

def init_agents(agents: list, number_of_agents, port):
    player_names = list()
    c = 1

    for i in range(number_of_agents[0]):
        port = port + c
        cooperator_name = 'cooperator_{}@localhost:{}'.format(port, port)
        cooperator_init = AgentPlayer(AID(name=cooperator_name),
                                      machine=machine_instance,
                                      persona='Cooperator')
        player_names.append(cooperator_name)
        agents.append(cooperator_init)
        c += 1

    for i in range(number_of_agents[1]):
        port = port + c
        cheater_name = 'cheater_{}@localhost:{}'.format(port, port)
        cheater_init = AgentPlayer(AID(name=cheater_name),
                                   machine=machine_instance,
                                   persona='Cheater')
        player_names.append(cheater_name)
        agents.append(cheater_init)
        c += 1

    for i in range(number_of_agents[2]):
        port = port + c
        copycat_name = 'copycat_{}@localhost:{}'.format(port, port)
        copycat_init = AgentPlayer(AID(name=copycat_name),
                                   machine=machine_instance,
                                   persona='Copycat')
        player_names.append(copycat_name)
        agents.append(copycat_init)
        c += 1
        
    for i in range(number_of_agents[3]):
        port = port + c
        grudger_name = 'grudger_{}@localhost:{}'.format(port, port)
        grudger_init = AgentPlayer(AID(name=grudger_name),
                                   machine=machine_instance,
                                   persona='Grudger')
        player_names.append(grudger_name)
        agents.append(grudger_init)
        c += 1

    return

if __name__ == '__main__':
    cheater     = 3
    cooperator  = 7
    copycat     = 3
    grudger     = 4
    agents = list()

    port = int(argv[1])
    machine_name = 'machine_{}@localhost:{}'.format(port, port)
    machine_instance = AgentMachine(AID(name=machine_name))
    agents.append(machine_instance)

    init_agents(agents=agents, number_of_agents=[cheater, cooperator, copycat, grudger], port=port)
    start_loop(agents)
