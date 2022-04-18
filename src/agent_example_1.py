from pade.misc.utility import start_loop
from pade.acl.aid import AID
from sys import argv

from agents.AgentMachine import AgentMachine
from agents.AgentPlayer import AgentPlayer


def init_agents(agents: list, number_of_agents, port):
    player_names = list()
    c = 1

    for i in range(number_of_agents[0]):
        port = port + c
        cooperator_name = 'cooperator_{}@localhost:{}'.format(port, port)
        cooperator_init = AgentPlayer(AID(name=cooperator_name),
                                      machine=machine_instance,
                                      persona='Cooperator')
        player_names.append(cooperator_name)
        agents.append(cooperator_init)
        c += 1

    for i in range(number_of_agents[1]):
        port = port + c
        cheater_name = 'cheater_{}@localhost:{}'.format(port, port)
        cheater_init = AgentPlayer(AID(name=cheater_name),
                                   machine=machine_instance,
                                   persona='Cheater')
        player_names.append(cheater_name)
        agents.append(cheater_init)
        c += 1

    for i in range(number_of_agents[2]):
        port = port + c
        copycat_name = 'copycat_{}@localhost:{}'.format(port, port)
        copycat_init = AgentPlayer(AID(name=copycat_name),
                                   machine=machine_instance,
                                   persona='Copycat')
        player_names.append(copycat_name)
        agents.append(copycat_init)
        c += 1
        
    for i in range(number_of_agents[3]):
        port = port + c
        grudger_name = 'grudger_{}@localhost:{}'.format(port, port)
        grudger_init = AgentPlayer(AID(name=grudger_name),
                                   machine=machine_instance,
                                   persona='Grudger')
        player_names.append(grudger_name)
        agents.append(grudger_init)
        c += 1

    return


if __name__ == '__main__':
    cheater     = 3
    cooperator  = 7
    copycat     = 3
    grudger     = 4
    agents = list()

    port = int(argv[1])
    machine_name = 'machine_{}@localhost:{}'.format(port, port)
    machine_instance = AgentMachine(AID(name=machine_name))
    agents.append(machine_instance)

    init_agents(agents=agents, number_of_agents=[cheater, cooperator, copycat, grudger], port=port)
    start_loop(agents)
