import socket
from utility import trace, extract_json_data
from ip_recovery import list_ip_usable
import traceback
from icecream import ic
import time
ic.enable()

IP_DATA_FILE = "../data/txt/ip_container.txt"
PORT = "../data/json/esempio.json"
open_ports = []


def get_host_ip_addr (target):
    try:
        ip_addr = socket.gethostbyname(target)
    except socket.gaierror as e:            #in caso di errore di reperimento dell'inidirizzo (per non bloccare)
        ic (f"Errore: {e}") 
    else:
        return ip_addr

def scan_port (ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #AF_INET SPECIFICA USO DI IPV4 e SOCK_STREAM DI TCP
    sock.settimeout(1) #in realta richiede float ma effettua casting implicito
    conn_status = sock.connect_ex ((ip, port))  #restituisce 0 se la connessione va a buon fine, 1 in caso di errori
    if conn_status == 0:
        open_ports.append(port)
    sock.close()
    return open_ports


def get_ports_info ():
    '''
    respoonsabile dir estituire i dati utilizzabili (info sulle porte che ci servono)
    '''
    data = extract_json_data(PORT)
    ports_info = {int (k): value for (k, value) in data.items()}                    
    #Sta prendendo ogni coppia chiave-valore dal dizionario originale 
    #data (ottenuto dal file JSON) e sta convertendo la chiave in un
    # numero intero usando int(). Quindi, il nuovo dizionario ports_info avrà 
    #chiavi che sono numeri interi e valori corrispondenti presi dal dizionario
    # originale. Infine, questo nuovo dizionario viene restituito.
    return ports_info



def main():
    global open_ports  # Indica che stiamo usando una variabile globale
    list_ip = list_ip_usable(IP_DATA_FILE)
    ic(list_ip)
    dict_ip_open_port = {}
    for ip in list_ip:
        ic(ip)
        ports_info = get_ports_info()
        for port in ports_info.keys():
            ic(f"Scanning: {ip}:{port}")
            open_ports = scan_port(ip, port)
        ic(open_ports)
        dict_ip_open_port[ip] = open_ports
        open_ports = []
    ic ( dict_ip_open_port)
        
        



if __name__ == "__main__":
    t1 = time.time()
    trace("Start", "../log/port_scanner.log")
    try:
        main ()
        trace("Good", "../log/port_scanner.log")
    except Exception as e:
        trace("Error: {}".format(str(e)), "../log/port_scanner.log")
        traceback.ic_exc()
    t2 = time.time()
    ic (t2-t1)