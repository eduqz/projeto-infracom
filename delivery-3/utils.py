import time
import zlib
import warnings
from datetime import datetime


# Timer class
class Timer:
    # Constructor method, that initialize the attributes
    def __init__(self):
        self.start_time = None

    # Method that sets the start_time to zero to restart the timer
    def restart(self):
        self.start_time = time.perf_counter()

    # Method that gets the elapsed time
    def check(self):
        if self.start_time is None:
            raise Exception(f"Use o comando de restart() para inicia-lo")

        elapsed_time = time.perf_counter() - self.start_time
        return elapsed_time

    # Static method that get the current time and format it in a string
    @staticmethod
    def get_current_time():
        n = datetime.now()
        time_tuple = n.timetuple()
        _, _, _, h, mi, _, _, _, _ = time_tuple
        time = str(h) + ':' + str(mi)

        return time


# RDT class, that setup the data transfer on UDP using the Kurose instructions for RDT 3.0
class Rdt:
    # Constructor method, that initialize the attributes
    def __init__(self, socket, feeder, saver, first_sender, client_adress, timer_limit, size):
        self.socket = socket
        self.saver = saver
        self.feeder = feeder
        self.timer_limit = timer_limit
        self.size = size
        self.client_adress = client_adress

        self.timer = Timer()
        self.action = True
        self.sender_sequence = 0
        self.receiver_ack = 0
        self.retransmit = False

        if first_sender:
            self.state = 1
            self.feeder.load_next_data()
        else:
            self.state = 2

    # Method that transforms bytes in string
    @staticmethod
    def decode_msg(bytecode):
        string_head = bytecode.decode('utf-8')
        decoded_msg = eval(string_head)
        return decoded_msg

    # Method that transforms string in bytes
    @staticmethod
    def encode_msg(msg):
        string_head = str(msg)
        bytecode = string_head.encode('utf-8')
        return bytecode

    # Method that, by using zlib, calculates the verify sum
    @staticmethod
    def verify_sum(data):
        return zlib.crc32(data)

    # Method that do the sender action
    def send(self, msg):
        self.socket.sendto(msg, self.client_adress)
        self.timer.restart()
        self.state = 2

    # Method that receive the response and interpretate it
    def recieve_response(self):
        if self.timer.start_time == None or self.timer.check() < self.timer_limit:
            encoded_response, self.client_adress = self.socket.recvfrom(
                self.size)
            if(encoded_response):
                self.last_response = self.decode_msg(encoded_response)
                if self.last_response["verify_sum"] != self.verify_sum(self.last_response["data"]):
                    warnings.warn("O pacote recebido eh invalido")
                else:
                    self.receiver_ack = self.last_response["seq"]
                    if not self.last_response['finished']:
                        self.saver.save_data(self.last_response["data"])
                    else:
                        if self.feeder.finish and self.last_response["ack"] == self.sender_sequence:
                            self.action = False

                if self.last_response["ack"] != self.sender_sequence:
                    self.retransmit = True
                    warnings.warn(
                        "O ultimo pacote nao foi recebido adequadamente")
                else:
                    self.retransmit = False
                    self.sender_sequence = 1 if self.sender_sequence == 0 else 0
                    self.feeder.load_next_data()

                self.state = 1
            else:
                self.state = 2
        else:
            self.retransmit = True
            self.state = 1

    # Method that setups the packet to send it
    def transmit(self):
        while self.action:
            if self.state == 1:
                data_to_send = self.feeder.get_data()
                msg = {
                    "ack": self.receiver_ack,
                    "seq": self.sender_sequence,
                    "verify_sum": self.verify_sum(data_to_send),
                    "finished": self.feeder.finish,
                    "data": data_to_send
                }
                encoded_msg = self.encode_msg(msg)
                self.send(encoded_msg)
                if hasattr(self, 'last_response') and self.feeder.finish and self.last_response['finished'] and not self.retransmit:
                    self.action = False
            elif self.state == 2:
                self.recieve_response()

        self.saver.close()
        self.socket.close()
