from pade.core.agent import Agent
from pade.misc.utility import display_message
import pprint

class Cheater(Agent):
    def __init__(self, aid):
        super(Cheater, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hello World! Im a CHEATER! I ALWAYS CHEAT')

    def react(self, message):
        pprint(self.__class__.__name__)
        pprint(message.__dict__)
        display_message(self.aid.localname, 'Mensagem recebida')
