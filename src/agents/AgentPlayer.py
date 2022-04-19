from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage

from pade.behaviours.protocols import FipaSubscribeProtocol


class PlayerProtocol(FipaSubscribeProtocol):
    def __init__(self, machine, message, persona):
        super(PlayerProtocol, self).__init__(machine,
                                             message)
        self.persona = persona

    def handle_agree(self, message):
        pass

    def handle_inform(self, message):
        reply = message.create_reply()
        if(self.persona == 'Cooperator'):
            reply.set_content(False)
        elif(self.persona == 'Cheater'):
            reply.set_content(True)
        else:
            reply.set_content(False)
        # TO-DO: elif is Copycat
        # TO-DO: elif is Grudger
        reply.set_performative(ACLMessage.INFORM)
        self.agent.send(reply)


class AgentPlayer(Agent):
    def __init__(self, aid, machine, persona):
        super(AgentPlayer, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hello World! Im a/an ' + persona)
        self.call_later(8.0, self.launch_subscriber_protocol)
        self.machine = machine
        self.persona = persona

    def launch_subscriber_protocol(self):
        msg = ACLMessage(ACLMessage.SUBSCRIBE)
        msg.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        msg.add_receiver(self.machine.aid)

        self.protocol = PlayerProtocol(self, msg, self.persona)
        self.behaviours.append(self.protocol)
        self.protocol.on_start()