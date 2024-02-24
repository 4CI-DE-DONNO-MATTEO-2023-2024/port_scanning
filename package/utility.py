'''
Matteo De Donno
utility.py
'''

import time
import platform
import os
import csv
import json

def time_control(f):
    '''
    Condition = The file you want to check is a .csv / .log file.
    Input     = Directory of the file.
    Call      = No Call.
    Process   = checks if the last execution took place more than 
                a month ago, if it is positive change the file name to
                'x_year-monts-day-hour-minute-second'. 
    Output    = Any change of the file name
    Return    = A boolean value that is true if the file name is changed
    '''
    mod = False
    if f.split(".")[len(f.split(".")) - 1] == 'log':
        with open(f, 'r', encoding='utf-8-sig') as file_log:
            lines = file_log.readlines()
            first_line = lines[0].split(';')
            epoch = float(first_line[0])
            gap = time.time() - epoch
            if gap >= 2629056:
                new_name = f[:-4]
                last_line = lines[-1].split(';')
                last_date = float(last_line[0])
                new_name += time.strftime('_%Y-%m-%d_%H-%M-%S', time.localtime(last_date))
                new_name += '.log'
                mod = True
        if mod:
            os.rename(f, new_name)
    if f.split(".")[len(f.split(".")) - 1] == 'csv':
        with open (f, newline='', encoding='utf-8-sig') as file_csv:
            next(csv.reader(file_csv, delimiter=','))
            header = next(csv.reader(file_csv, delimiter=','))
            epoch = float(header[0])
            gap = time.time() - epoch
            if gap >= 2629056:
                last_row = None
                for row in csv.reader(file_csv, delimiter=','):
                    last_row = row
                if last_row is not None:
                    new_name = f[:-4]
                    time_1 = time.strftime('_%Y-%m-%d_%H-%M-%S', time.localtime(float(last_row[0])))
                    new_name += time_1
                    new_name += '.csv'
                    mod = True
        if mod:
            os.rename(f, new_name)
    return mod


def csv_f_x (header, values, n, f):
    '''
    Condition = The csv file already exist.
                es: header =  [header1, header2, header3]
                    values =  [values1, values2, values3,
                               values1, values2, values3]
    Input     = Two list, an Header, and another one with all the values.
                The directory of the CSV file and the number of file that the values 'repeat'
    Call      = Function 'time_control' in order to check if is 
                necessary to create a different file log if the
                one checked is getting to big (check the time).
    Process   = Control if the file is empty, if its empty write the first
                line (Header), otherwise it will just write the values.
    Output    = The values on the file.
                The same execution can produce more than 1 line in case of more than 1 repetitions,
                the same execution can be understood from the epoch.
    Return    = No return.
    '''
    t = time.time()
    if f.endswith(".csv"):
        if os.path.getsize(f) == 0:
            with open(f, 'a', newline='', encoding='utf-8-sig') as file_csv:
                csv_writer = csv.writer(file_csv)
                csv_writer.writerow(["Time", "Host"] + header)
                for i in range (n):
                    if i == 0:
                        csv_writer.writerow([t, platform.node()] + values [: i + len(header)])
                    else:
                        csv_writer.writerow([t, platform.node()] + values [(i * len(header)) : (i * len(header)) + len(header)])
        else:
            check = time_control(f)
            if check:
                with open(f, 'a', newline='', encoding='utf-8-sig') as file_csv:
                    csv_writer = csv.writer(file_csv)
                    csv_writer.writerow(["Time", "Host"] + header)
                    for i in range (n):
                        if i == 0:
                            csv_writer.writerow([t, platform.node()] + values [: i + len(header)])
                        else:
                            csv_writer.writerow([t, platform.node()] + values [(i * len(header)) : (i * len(header)) + len(header)])
            else:
                with open(f, 'a', newline='', encoding='utf-8-sig') as file_csv:
                    csv_writer = csv.writer(file_csv)
                    for i in range (n):
                        if i == 0:
                            csv_writer.writerow([t, platform.node()] + values [: i + len(header)])
                        else:
                            csv_writer.writerow([t, platform.node()] + values [(i * len(header)) : (i * len(header)) + len(header)])


def csv_f_1(header, values, f):
    '''
    Condition = The csv file already exist.
    Input     = Two list, an Header, and another one with all the values.
                The directory of the CSV file.
    Call      = Function 'time_control' in order to check if is 
                necessary to create a different file log if the
                one checked is getting to big (check the time).
    Process   = Control if the file is empty, if its empty write the first
                line (Header), otherwise it will just write the values.
    Output    = The values on the file.
    Return    = No return.
    '''
    if f.endswith(".csv"):
        if os.path.getsize(f) == 0:
            with open(f, 'a', newline='', encoding='utf-8-sig') as file_csv:
                csv_writer = csv.writer(file_csv)
                csv_writer.writerow(["Time", "Host"] + header)
                csv_writer.writerow([time.time(), platform.node()] + values)
        else:
            check = time_control(f)
            if check:
                with open(f, 'a', newline='', encoding='utf-8-sig') as file_csv:
                    csv_writer = csv.writer(file_csv)
                    csv_writer.writerow(["Time", "Host"] + header)
                    csv_writer.writerow([time.time(), platform.node()] + values)
            else:
                with open(f, 'a', newline='', encoding='utf-8-sig') as file_csv:
                    csv_writer = csv.writer(file_csv)
                    csv_writer.writerow([time.time(), platform.node()] + values)



def trace(stringa, f):
    '''
    Condition = The log file already exists.
    Input     = String that indicates the situation of the file.
                the directory of the file.
    Call      = Function 'time_control' in order to check if it is 
                necessary to create a different log file if the
                checked one is getting too big (check the time).
    Process   = Writes general information for each execution 
                to a file, allowing for better identification 
                of the execution.
    Output    = Append all the information.
    Return    = No return.
    '''
    # Modifica qui: Aggiunto controllo se il file non esiste o è vuoto
    if f.endswith(".log"):
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            with open(f, 'a', encoding='utf-8-sig') as file_log:
                file_log.write(str(time.time()))
                file_log.write(';')
                file_log.write(platform.node())
                file_log.write(';')
                file_log.write(os.environ.get('USERNAME'))
                file_log.write(';')
                file_log.write(platform.system())
                file_log.write(';')
                file_log.write(platform.release())
                file_log.write(';')
                file_log.write(platform.version())
                file_log.write(';')
                file_log.write(platform.machine())
                file_log.write(';')
                file_log.write(stringa)
                file_log.write('\n')
        else:
            time_control(f)
            with open(f, 'a', encoding='utf-8-sig') as file_log:
                file_log.write(str(time.time()))
                file_log.write(';')
                file_log.write(platform.node())
                file_log.write(';')
                file_log.write(os.environ.get('USERNAME') or os.environ.get('USER') or 'UnknownUser')
                file_log.write(';')
                file_log.write(platform.system())
                file_log.write(';')
                file_log.write(platform.release())
                file_log.write(';')
                file_log.write(platform.version())
                file_log.write(';')
                file_log.write(platform.machine())
                file_log.write(';')
                file_log.write(stringa)
                file_log.write('\n')


def extract_json_data(filename):
    '''
    
    
    
    '''
    with open(filename, "r") as file:
        data = json.load(file)
    return data



if __name__ == "__main__":
    t1 = time.time()
    print(f'Execution lasted: {time.time() - t1}s')
