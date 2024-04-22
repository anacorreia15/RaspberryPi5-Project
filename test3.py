from picamera2 import Picamera2, Preview
import time
from datetime import datetime
import os
import paramiko
from gpiozero import DigitalInputDevice

# Create a DigitalInputDevice object for pin 21 (sensor infravermelho)
input_device = DigitalInputDevice(21)

 # Transferir arquivo para o servidor remoto
SERVER_IP = '192.168.1.100'
SERVER_USER = 'server'
SERVER_PASSWORD = 'server123'
#SERVER_PATH = '/home/server/Desktop/Projeto/Resnet-classification/images'
SERVER_PATH = '/home/server/Desktop/Projeto/resnet-fasterrcnn_1/images'

# Funcao para transferir arquivo para o servidor remoto via SSH
def transfer_file_to_server(local_file, server_ip, server_user, server_password, server_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_ip, username=server_user, password=server_password)
        sftp = ssh.open_sftp()
        sftp.put(local_file, os.path.join(server_path, os.path.basename(local_file)))
        sftp.close()
        ssh.close()
        print("Imagem transferida")
        # Remover arquivo local depois da transferencia
        os.remove(file_name)
        return True
    except Exception as e:
        print(f"Erro ao transferir o arquivo: {e}")
        return False

# Configuracoes da camera e captura de imagem
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

# Variavel para armazenar o estado anterior do pino
prev_pin_value = input_device.value

# Loop principal
try:
    while True:
        # Get the value of the pin
        pin_value = input_device.value

        if pin_value == 0 and prev_pin_value == 1:
            # Esperar 1 segundo para garantir que o tabuleiro esteja parado
            time.sleep(1)
            
            # Capturar a imagem
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            file_name = f"{ts}.jpg"
            picam2.capture_file(file_name)
            print("Imagem capturada ", pin_value)

            transfer_file_to_server(file_name, SERVER_IP, SERVER_USER, SERVER_PASSWORD, SERVER_PATH)
        else:
            print("Sem Tabuleiro ", pin_value)

        # Armazenar o valor atual do pino para a pr�xima itera��o
        prev_pin_value = pin_value

        # Pequeno atraso para evitar processamento excessivo
        time.sleep(2)

except KeyboardInterrupt:
    # Lidar com a interrup��o do teclado (Ctrl+C)
    pass

finally:
    # Parar a visualiza��o e desligar a c�mera ao sair do loop
    picam2.stop_preview()
    picam2.stop()
