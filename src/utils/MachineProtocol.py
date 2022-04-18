
from pade.behaviours.protocols import FipaSubscribeProtocol
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message
from pade.behaviours.protocols import FipaSubscribeProtocol
from pade.acl.messages import ACLMessage


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
