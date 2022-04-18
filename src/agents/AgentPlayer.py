from pprint import pprint
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage

from pade.behaviours.protocols import FipaSubscribeProtocol


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