from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage


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
