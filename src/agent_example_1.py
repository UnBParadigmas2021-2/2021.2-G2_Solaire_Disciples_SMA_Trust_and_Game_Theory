# Hello world in PADE!
#
# Criado por Lucas S Melo em 21 de julho de 2015 - Fortaleza, Ceará - Brasil

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.filters import Filter as f
from pade.acl.messages import ACLMessage
from pprint import pprint
from pade.acl.aid import AID
from sys import argv
from itertools import groupby
from itertools import combinations


class Machine(Agent):
    play_list = list()
    def __init__(self, aid, match):
        super(Machine, self).__init__(aid=aid)
        self.match = match
        display_message(self.aid.localname, 'BEEP BOOP! Im the MACHINE!')

    def on_start(self):
        message = ACLMessage(ACLMessage.REQUEST)
        message.add_receiver(AID(self.match[0]))
        message.add_receiver(AID(self.match[1]))
        message.set_content(
            'Jogador ' + self.match[0] + ' e ' + self.match[1] + ', Façam suas escolhas!')
        self.send(message)

    def react(self, message):
        display_message(self.aid.localname, message)
            

class BasePlayer(Agent):
    def __init__(self, aid):
        super(BasePlayer, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hello World! Im a BasePlayer!')

    def react(self, message):
        display_message(self.aid.localname, 'Mensagem recebida, preparando jogada')

        


class Cooperator(Agent):
    def __init__(self, aid):
        super(Cooperator, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hello World! Im a COOPERATOR! I ALWAYS COOPERATE')

    def react(self, message):
        pprint(self.__class__.__name__)
        pprint(message.__dict__)
        display_message(self.aid.localname, 'Mensagem recebida')


class Cheater(Agent):
    def __init__(self, aid):
        super(Cheater, self).__init__(aid=aid)
        display_message(self.aid.localname,
                        'Hello World! Im a CHEATER! I ALWAYS CHEAT')

    def react(self, message):
        pprint(self.__class__.__name__)
        pprint(message.__dict__)
        display_message(self.aid.localname, 'Mensagem recebida')


if __name__ == '__main__':
    cheater = 1
    cooperator = 1
    c = 0
    agents = list()
    player_names = list()
    # initializes copycats
    for i in range(cooperator):
        port = int(argv[1]) + c
        cooperator_name = 'copycat_{}@localhost:{}'.format(port, port)
        cooperator_init = Cooperator(AID(name=cooperator_name))
        player_names.append(cooperator_name)
        agents.append(cooperator_init)
        c += 1

    # initializes cheater
    for i in range(cheater):
        port = int(argv[1]) + c
        cheater_name = 'cheater_{}@localhost:{}'.format(port, port)
        cheater_init = Cheater(AID(name=cheater_name))
        player_names.append(cheater_name)
        agents.append(cheater_init)
        c += 1

    # creates matchmaking
    matchmaking = list(combinations(player_names, 2))
    for match in matchmaking:
        port = int(argv[1]) + c
        machine_name = 'machine_{}@localhost:{}'.format(port, port)
        machine_init = Machine(AID(name=machine_name), match)
        agents.append(machine_init)
        c += 1

    start_loop(agents)
