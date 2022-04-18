from pprint import pprint
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage

from pade.behaviours.protocols import FipaSubscribeProtocol


class PlayerProtocol(FipaSubscribeProtocol):
    def __init__(self, machine, message, persona):
        super(PlayerProtocol, self).__init__(machine,
                                             message)
        self.persona=persona

    def handle_agree(self, message: ACLMessage):
        display_message(self.agent.aid.name, message.content)
        # if(message.content == "+3coins"):
        #     print("erick: coins recebidas")
        #     self.machine.increment_coins(3)
            
        return

    def handle_inform(self, message):
        reply=message.create_reply()
        pprint('{} está escolhendo'.format(self.agent.aid.name))
        
        if(self.persona == 'Cooperator'):
            reply.set_content(False)
        
        elif(self.persona == 'Cheater'):
            reply.set_content(True)
        
        # TO-DO: elif is Copycat
        elif(self.persona == 'Copycat'):
            reply.set_content(False)
        
        # TO-DO: elif is Grudger
        elif(self.persona == 'Grudger'):
            reply.set_content(False)



        reply.set_performative(ACLMessage.INFORM)
        self.agent.send(reply)

    def handle_refuse(self, message):
        print("erick: confirm recebido")
        self.machine.increment_coins(3)
        return


class AgentPlayer(Agent):
    def __init__(self, aid, machine, persona):
        super(AgentPlayer, self).__init__(aid = aid)
        display_message(self.aid.localname,
                        'Hello World! Im a/an ' + persona)
        self.call_later(8.0, self.launch_subscriber_protocol)
        self.machine = machine
        self.persona = persona
        self.coins   = 10    # saldo de moedas

    def launch_subscriber_protocol(self):
        print('launch subscriber protocol')
        msg = ACLMessage(ACLMessage.SUBSCRIBE)
        msg.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        msg.set_content('Subscription request')
        msg.add_receiver(self.machine.aid)

        self.protocol = PlayerProtocol(self, msg, self.persona)
        self.behaviours.append(self.protocol)
        self.protocol.on_start()

    # def react(self, message):
    #     display_message(self.aid.localname,
    #                     'Mensagem recebida, preparando jogada')
    #
    #     # from pprint import pprint; pprint(message.__dict__)
    #     # pprint(self.persona)
    #     pass

    def increment_coins(self, increment: int):
        print('incrementando em {} moedas'.format(increment))
        self.coins += increment
        return

    def decrement_coins(self, decrement: int):
        print('decrementando em {} moeda'.format(decrement))
        self.coins -= decrement
        return