from pade.core.agent import Agent
from pade.misc.utility import display_message
from pprint import pprint

class Cooperator(Agent):
    def __init__(self, aid):
        super(Cooperator, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hello World! Im a COOPERATOR! I ALWAYS COOPERATE')

    def react(self, message):
        pprint(self.__class__.__name__)
        pprint(message.__dict__)
        display_message(self.aid.localname, 'Mensagem recebida')
