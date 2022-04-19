from pade.core.agent import Agent
from pade.misc.utility import display_message
from pprint import pprint

class Grudger(Agent):
    def __init__(self, aid):
        super(Grudger, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hi! Im a Grudger: I will cooperate... unless my \
                        adversary cheats on me (then I will always cheat)!')

    def react(self, message):
        pprint(self.__class__.__name__)
        pprint(message.__dict__)
        display_message(self.aid.localname, 'Mensagem recebida')