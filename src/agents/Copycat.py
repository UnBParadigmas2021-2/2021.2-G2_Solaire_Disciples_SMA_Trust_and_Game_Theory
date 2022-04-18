from pade.core.agent import Agent
from pade.misc.utility import display_message
import pprint


class Copycat(Agent):
    def __init__(self, aid):
        super(Copycat, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hi! Im a Copycat: I start cooperating, then I simply \
                        repeat whatever my adversary did in the last round')

    def react(self, message):
        pprint(self.__class__.__name__)
        pprint(message.__dict__)
        display_message(self.aid.localname, 'Mensagem recebida')