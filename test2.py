from picamera2 import Picamera2, Preview
import time
from datetime import datetime
import os
import paramiko
from gpiozero import DigitalInputDevice

# Create a DigitalInputDevice object for pin 40
input_device = DigitalInputDevice(21)

# Funcao para transferir arquivo para o servidor remoto via SSH
def transfer_file_to_server(local_file, server_ip, server_user, server_password, server_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=server_user, password=server_password)
    sftp = ssh.open_sftp()
    sftp.put(local_file, os.path.join(server_path, os.path.basename(local_file)))
    sftp.close()
    ssh.close()

# Configuracoes da camera e captura de imagem
#output_folder = 'images'
dt = datetime.now()
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)

ts = datetime.timestamp(dt)
#file_name = os.path.join(output_folder, f"{ts}.jpg")
file_name = f"{ts}.jpg"
picam2.capture_file(file_name)
picam2.stop_preview()
picam2.stop()

# Transferencia de arquivo para o servidor remoto
SERVER_IP = '192.168.1.112'
SERVER_USER = 'server'
SERVER_PASSWORD = 'server123'
SERVER_PATH = '/home/server/Desktop/Projeto/Resnet-classification/images'
transfer_file_to_server(file_name, SERVER_IP, SERVER_USER, SERVER_PASSWORD, SERVER_PATH)

# Remover arquivo local depois da transferencia
os.remove(file_name)
