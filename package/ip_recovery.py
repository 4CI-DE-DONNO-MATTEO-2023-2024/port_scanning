import subprocess
from utility import trace
from icecream import ic
ic.enable()

def ping_ip_dict(file_path):
    '''
    
    
    '''
    try:
        with open(file_path, 'r') as file:
            # Read IP addresses from the file
            ip_addresses = file.read().splitlines()

            # Initialize the results list
            results = []

            # Execute ping for each IP address
            for ip in ip_addresses:
                result = subprocess.run(['ping', ip], stdout=subprocess.PIPE, text=True)
                results.append({'ip': ip, 'result': result.stdout})

            # Initialize the dictionary to store IP status
            dict_ip = {}

            for result in results:
                # Check if the required strings are present in the result
                if "TTL" in result['result'] and "byte" in result['result'] and "durata" in result['result']:
                    # If conditions are met, set the value to 1, otherwise 0
                    dict_ip[result['ip']] = 1
                else:
                    dict_ip[result['ip']] = 0
            ic (dict_ip)
            return dict_ip
    except FileNotFoundError:
        trace("File not found", "../log/ip_recovery.log")
        return None

def list_ip_usable(file_path):
    '''
    
    
    '''
    diz = ping_ip_dict(file_path)
    usable_ips = [ip for ip, status in diz.items() if status == 1]
    return usable_ips

if __name__ == "__main__":
    trace("Start", "../log/ip_recovery.log")
    try:
        trace("Good", "../log/ip_recovery.log")
    except Exception as e:
        trace("Error: {}".format(str(e)), "../log/ip_recovery.log")
