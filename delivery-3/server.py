import socket
import threading
from utils import Timer


# Constants
MENU = [
    {
        "id": 1,
        "name": "parmegiana",
        "price": 20
    },
    {
        "id": 2,
        "name": "bife a cavalo",
        "price": 60
    },
    {
        "id": 3,
        "name": "bife acebolado",
        "price": 30
    },
    {
        "id": 4,
        "name": "porcao de feijoada",
        "price": 14
    },
    {
        "id": 5,
        "name": "porcao de arroz",
        "price": 8
    },
    {
        "id": 6,
        "name": "coca cola (lata)",
        "price": 5
    }
]

OPTIONS = 'Digite uma das opcoes a seguir (o número ou por extenso)\n1 - cardapio\n2 - pedido\n3 - conta individual\n4 - nao fecho com robo, chame seu gerente\n5 - nada nao, tava so testando\n6 - conta da mesa\n7 - pagar conta'


# Server class
class Server:
    # Constructor method, that initialize the attributes
    def __init__(self, ip='127.0.0.1', port=5001):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(type=socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.client = set()
        self.event = threading.Event()
        self.info = {}
        self.history = []
        self.orders = []
        self.paid = 0
        self.finished = False

    # Method that starts the server in a thread
    def start(self):
        print('Server iniciado')
        threading.Thread(target=self._recv, daemon=True).start()

    # Method that stops the server
    def stop(self):
        self.event.set()
        self.sock.close()

    # Method that define the response for a received message
    def _recv(self):
        while not self.event.is_set():
            data, ipinfo = self.sock.recvfrom(1024)
            self.client.add(ipinfo)

            message = Timer.get_current_time() + ' CINtofome: '

            recv_message = data[:16]

            # Based on the instruction, do the right action
            # We use a history where the last command is saved, because some actions are defined by the last instruction

            # Coomand used to finish the flow, but only if the user has paid the bill
            if recv_message == b'levantar':
                total_sum = 0

                for order in self.orders:
                    total_sum += order['item']['price']

                # Case of paid bill
                if total_sum <= self.paid:
                    message += 'Volte sempre ^^'
                    self.info = {}
                    self.history = []
                    self.orders = []
                    self.paid = 0
                    self.finished = True

                # Case of unpaid bill
                else:
                    message += 'Você não pagou sua conta! Resta pagar R$ ' + \
                        str(total_sum - self.paid) + ',00\n\n---\n' + OPTIONS
                    self.history.append('options')

            # Command to start the flow to set the user that are using the bot
            elif recv_message in [b'chefia', b'opa', b'campeao']:
                message += 'Digite sua mesa'
                self.history.append('table')

            # Command to set the current table
            elif self.history[-1] == 'table':
                self.info['table'] = data.decode()
                message += 'Digite seu nome'
                self.history.append('name')

            # Command to set the current user name
            elif self.history[-1] == 'name':
                self.info['name'] = data.decode()
                message += '' + OPTIONS
                self.history.append('options')

            # Command to show the menu, by stringfying the menu array
            elif self.history[-1] == 'options' and recv_message in [b'1', b'cardapio']:
                message += '\n*** CARDÁPIO ***\n'
                for item in MENU:
                    message += str(item['id']) + ' - ' + item['name'] + \
                        ' => R$ ' + str(item['price']) + ',00 \n'

                message += '\n\n---\n' + OPTIONS
                self.history.append('options')

            # Command to start the order
            elif self.history[-1] == 'options' and recv_message in [b'2', b'pedir', b'pedido']:
                message += \
                    'Digite qual item que gostaria de pedir (numero ou por extenso)'
                self.history.append('order')

            # Command to register the order, by adding an item in the orders array
            elif self.history[-1] == 'order':
                for item in MENU:
                    if data.decode() in [str(item['id']), item['name']]:
                        self.orders.append(
                            {"user": self.info['name'], "item": item})

                message += 'Pedido confirmado!\n---\n' + OPTIONS
                self.history.append('options')

            # Command to show the user bill, by filtering the orders created by the current user in the options array, and stringfying the result
            elif self.history[-1] == 'options' and recv_message in [b'3', b'conta individual']:
                message += '\n*** CONTA DE "' + self.info['name'] + '" ***\n\n'
                sum = 0

                for order in self.orders:
                    if order['user'] == self.info['name']:
                        message += order['item']['name'] + ' => R$ ' + \
                            str(order['item']['price']) + ',00 \n'
                        sum += order['item']['price']

                message += '\n\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\nTotal - R$ ' + \
                    str(sum) + ',00\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n'

                message += '\n\n' + OPTIONS
                self.history.append('options')

            # Command to show the total bill, by stringfying the bill array
            elif self.history[-1] == 'options' and recv_message in [b'6', b'conta da mesa']:
                message += '\n*** CONTA DA MESA ' + \
                    self.info['table'] + ' ***\n'
                sum = 0

                for order in self.orders:
                    message += '\n\n| ' + order['user'] + ' |\n\n'
                    message += order['item']['name'] + ' => R$ ' + \
                        str(order['item']['price']) + ',00 \n'
                    sum += order['item']['price']

                message += '\n\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\nTotal da mesa - R$ ' + \
                    str(sum) + ',00\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n'

                message += '\n\n---\n' + OPTIONS
                self.history.append('options')

            # Command to respond when user say that don't want to a bot
            elif self.history[-1] == 'options' and recv_message in [b'4', b'gerente', b'nao fecho com robo, chame seu gerente']:
                message += 'Beep beep, chamando o gerente...\n\n---\n' + OPTIONS
                self.history.append('options')

            # Command to respond when user is just testing the bot
            elif self.history[-1] == 'options' and recv_message in [b'5', b'testando', b'nada nao, tava so testando']:
                message += 'Testado!\n\n---\n' + OPTIONS
                self.history.append('options')

            # Command to start the payment flow
            elif self.history[-1] == 'options' and recv_message in [b'7', b'pagar', b'pagar conta']:
                message += 'Digite o valor a ser pago'
                self.history.append('payment')

            # Command to save the amount that the user are paying and inform the user in case of paying more than it should
            elif self.history[-1] == 'payment':
                pay = int(data.decode().replace(',', '.'))
                self.paid += pay

                sum = 0
                total_sum = 0

                for order in self.orders:
                    if order['user'] == self.info['name']:
                        sum += order['item']['price']
                    total_sum += order['item']['price']

                message += 'Sua conta foi de R$ ' + str(sum) + ',00 e a da mesa de R$ ' + str(
                    total_sum) + ',00\nVocê está pagando R$ ' + str(pay) + ',00. '

                if pay > sum:
                    message += 'O valor é R$ ' + \
                        str(sum - pay) + ',00 a mais que sua conta. O valor excedente será distribuído para outros clientes.'

                message += 'Pagamento confirmado!\n\n---\n' + OPTIONS
                self.history.append('options')

            self.send(message.encode())

            # If user finished the flow
            if self.finished:
                self.client.remove(ipinfo)
                self.finished = False

    # Method used to send the message to every client
    def send(self, data):
        for client in self.client:
            self.sock.sendto(data, client)


# Creating a Server instance and using it
server = Server()
server.start()

while True:
    cmd = input()
    cmd = cmd.encode()
    server.send(cmd)

    if cmd == 'sair':
        break
