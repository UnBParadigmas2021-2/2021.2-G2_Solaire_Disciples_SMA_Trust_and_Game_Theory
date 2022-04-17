# Hello world in PADE!
#
# Criado por Lucas S Melo em 21 de julho de 2015 - Fortaleza, Ceará - Brasil

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
from itertools import groupby
from itertools import combinations


class Machine(Agent):
    def __init__(self, aid):
        super(Machine, self).__init__(aid=aid)
        display_message(self.aid.localname, 'BEEP BOOP! Im the MACHINE!')

class Cooperator(Agent):
    has_been_cheated_on = False

    def __init__(self, aid):
        super(Cooperator, self).__init__(aid=aid)
        display_message(self.aid.localname, 'Hello World! Im a COOPERATOR! I ALWAYS COOPERATE')


class Cheater(Agent):
    def __init__(self, aid):
        super(Cheater, self).__init__(aid=aid)
        display_message(self.aid.localname, 'Hello World! Im a CHEATER! I ALWAYS CHEAT')


if __name__ == '__main__':
    cheater = 3
    cooperator = 7
    c = 0
    agents = list()
    player_names = list ()
    ## intializes the machine
    port = int(argv[1])
    c += 1000
    machine_name = 'machine_{}@localhost:{}'.format(port, port)
    machine_init = Machine(AID(name=machine_name))
    agents.append(machine_init)

    ## initializes copycats
    for i in range(cooperator):
        port = int(argv[1]) + c
        cooperator_name = 'copycat_{}@localhost:{}'.format(port, port)
        cooperator_init = Cooperator(AID(name=cooperator_name))
        player_names.append(cooperator_name)
        agents.append(cooperator_init)
        c += 1000

    ## initializes cheater
    for i in range(cheater):
        port = int(argv[1]) + c
        cheater_name = 'cheater_{}@localhost:{}'.format(port, port)
        cheater_init = Cheater(AID(name=cheater_name))
        player_names.append(cheater_name)
        agents.append(cheater_init)
        c += 1000

    ## creates matchmaking
    matchmaking = list(combinations(player_names, 2))


    start_loop(agents)
