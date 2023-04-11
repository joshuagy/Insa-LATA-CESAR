import socket
import threading
import time
import sys
import subprocess
import struct
from ip import get_ip
import os

class Multiplayer():
    def __init__(self, plateau, server_address, server_port, listen_port, mode):
        self.plateau = plateau
        self.number_of_players = 1
        self.plateau.modeText = f"Multiplayer Mode - {get_ip()} : {listen_port} - {self.number_of_players} players"
        self.server_address = server_address
        self.server_port = server_port
        self.listen_port = listen_port
        self.mode = mode

        self.p = subprocess.Popen(["./master",str(self.server_address), str(self.server_port), str(self.listen_port), str(self.mode)])
        time.sleep(1)
        self.localhost = "127.0.0.1"
        
        self.nb_NC = 0
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.localhost, self.listen_port))

        self._stop_event = threading.Event()

        self.recv_thread = threading.Thread(target=self.recv_thread)
        self.recv_thread.start()

    def stop(self):
        self.plateau.modeText = "Singleplayer Mode"
        self._stop_event.set()
        self.client_socket.close()
        self.p.kill()
        del self

    def recv_thread(self):
        while not self._stop_event.is_set():
            data_len, data = self.recv_packet(self.client_socket)
            if data:
                data = data.decode('utf-8')
                print(f"[R] payload: {data} | payload_length: {data_len}")
                self.wrapper(data)

    def send(self, message):
        payload = message
        self.send_packet(self.client_socket, payload.encode('utf-8'))

    def recv_packet(self, sockfd):
        # Read the length field from the stream
        length_bytes = sockfd.recv(4)
        if not length_bytes:
            # The connection was closed by the peer
            return 0, None

        # Convert the length field from network byte order to host byte order
        payload_len = struct.unpack('!I', length_bytes)[0]

        # Allocate a buffer for the payload
        payload = bytearray(payload_len)

        # Read the payload from the stream
        total_received = 0
        while total_received < payload_len:
            remaining = payload_len - total_received
            chunk = sockfd.recv(remaining)
            if not chunk:
                # The connection was closed by the peer
                return 0, None
            payload[total_received:total_received + len(chunk)] = chunk
            total_received += len(chunk)

        return payload_len, payload

    def send_packet(self, sockfd, payload):
        # Calculate the total length of the packet (payload + header)
        payload_len = len(payload)
        packet_len = payload_len + 4

        # Allocate a buffer for the packet
        packet = bytearray(packet_len)

        # Write the length field in network byte order
        length_bytes = struct.pack('!I', payload_len)
        packet[0:4] = length_bytes

        # Copy the payload into the packet buffer
        packet[4:] = payload

        # Send the packet
        ret = sockfd.send(packet)
        print(f"[S] payload: {str(packet, 'utf-8')} | payload_length: {payload_len} bytes")
        
        if ret < 0:
            raise socket.error('Error sending packet')

        return ret

    def wrapper(self, message):
        """ Wrapper that recieve message from the network manager and redirect it in the right method """
        message_split = message.split(".")
        #print(message_split)

        #Building - Tested
        if message_split[0] == "SCL":
            self.plateau.clearLand(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBH":
            self.plateau.buildHousingSpot(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBI":
            self.plateau.buildEngineerPost(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBF":
            self.plateau.buildFarm(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBP":
            self.plateau.buildPrefecture(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBS":
            self.plateau.buildSenate(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBR":
            self.plateau.buildRoads(int(message_split[5]), int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[6]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBW":
            self.plateau.buildWell(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBGo":
            self.plateau.buildTemple(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "SBM":
            self.plateau.buildMarket(int(message_split[1]), int(message_split[3]), int(message_split[2]), int(message_split[4]), int(message_split[5]))
            self.plateau.soundMixer.playEffect('buildEffect')
        elif message_split[0] == "UH":
            for b in self.plateau.structures :
                if b.case.x == message_split[1] and b.case.y == message_split[2] :
                    b.becomeAHouse()


        # Change actual player number
        elif message_split[0] == "SYNCNP":
            self.number_of_players = int(message_split[1])
            self.plateau.modeText = f"Multiplayer Mode - {get_ip()} : {self.listen_port} – {self.number_of_players} players"
       
        # Walker - Appear/Disapear tested
        #Appear
        elif message_split[0] == "WA":
            if message_split[1] == "0":
                Immigrant(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6], id=int(message_split[7]))
            elif message_split[1] == "1":
                Engineer(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6], id=int(message_split[7]))
            elif message_split[1] == "2":
                Prefet(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6], id=int(message_split[7]))
            elif message_split[1] == "3":
                cartPusher = CartPusher(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6], id=int(message_split[7]))
                Cart(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, cartPusher)
            elif message_split[1] == "4":
                Prefet(self.model.actualGame.map[int(message_split[2])][int(message_split[3])], self.model.actualGame, self.model.actualGame.map[int(message_split[4])][int(message_split[5])],message_split[6],message_split[7],message_split[8], id=int(message_split[9]))
        #Disappear
        elif message_split[0] == "WD":
            for e in self.model.actualGame.entities:
                if e.id == int(message_split[1]):
                    e.delete()
        #Switch mode
        elif message_split[0] == "WMo": #A discuter niveau pertinence
            for e in self.model.actualGame.entities:
                if e.id == int(message_split[1]):
                    e.mode = int(message_split[2])
        #Move
        elif message_split[0] == "WM": #A discuter niveau pertinence
            for e in self.model.actualGame.entities:
                if e.id == int(message_split[1]):
                    e.change_tile(self.model.actualGame.map[int(message_split[2])][int(message_split[3])])

        # Fire risk related
        elif message_split[0] == "FRC":
            for b in self.model.actualGame.structures:
                if isinstance(b, Building):
                    if b.case == self.model.actualGame.map[int(message_split[1])][int(message_split[2])]:
                        b.set_fireRisk(int(message_split[3]))
                        
        # Gestion de transmission de propriété
        elif message_split[0] == "SLF":
            for b in self.plateau.structures :
                if b.case.x == message_split[1] and b.case.y == message_split[2] :
                    b.property = message_split[3]
                    
        # intercept new Player (work)
        # On intercepte les nouvelles connexion (uniquement pour lhost)
        elif message_split[0] == "NC":
            self.plateau.save_game("multiplayer_game")  # sauvegarde de la game
            full_path = os.path.join("./Model/Save_Folder", "multiplayer_game.pickle")
            with open(full_path, 'rb') as f:
                file_content = f.read()
                content = "contenu factice"
                self.send(f"SNC.{content}.{self.plateau.property}")
            self.nb_NC += 1
        # load map
        elif message_split[0] == "SNC":
            print("ca marche")
            full_path = os.path.join("./Model/Save_Folder", "multiplayer_game_received.pickle")
            with open(full_path, 'wb') as f:
                f.write(message_split[1].encode())
            # self.plateau.load_savefile("multiplayer_game")