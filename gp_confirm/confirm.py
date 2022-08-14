#         1         2         3         4         5         6         7
#1234567890123456789012345678901234567890123456789012345678901234567890123456789

# coding: utf-8

import openpyxl
import sys
import os
import re

# Get target Excel file name.
args = sys.argv
my_wb = openpyxl.load_workbook(args[1], data_only=True)

false_values = []
ok_cnt = 0
ng_cnt = 0

# Enviromental variables.
max_target = 16                # Max number of target host.
store_dir = 'gather_config'    # Connfig store directory

class Color:
    BLACK = '\033[30m'
    RED   = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RESET = '\033[0m'


# [ START grep_file]
# Read strings hit first entry from file.
#
# Args:
#   file_path: specify target file path.
#   pattern: text strings to grep(optional).
#   delim: delimiter string to grep(optional).
# Returns:
#   entry in file(str)
#
#         1         2         3         4         5         6         7
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
#
def grep_file(file_path, pattern='Not_Available', delim='='):
    if os.path.exists(file_path):
        with open(file_path, mode='r') as f:
            lines = f.read().splitlines()

        for line in lines:
            serarch_result = re.search('^\s*' + pattern + '\s*' + delim, line)
            if serarch_result or pattern == 'Not_Available':
                return line
                break

        return 'No_Param_Found' + delim +'No_Value_Found'

    else:
        return 'No_File_Found' + delim +'No_File_Found'

# [ END grep_file]


def check_value(sheet_name):

    global ok_cnt, ng_cnt

    # Get values from Excel file.
    my_ws = my_wb[sheet_name]
    values = []

    for row in my_ws.iter_rows(min_row=2, min_col=1):
        values.append([cell.value for cell in row])

    # Proess each row.
    for value in values:
        if value[0] == 'product':
            header_list = value
        
        else:
            for i in range(max_target + 10):
                if i >=10 and value[i] is not None:

                    target_product = value[0]
                    target_value   = str(value[i])
                    target_node    = header_list[i]

                    # Set target file name.
                    if sheet_name == 'cmd':
                        target_parm  = value[3]
                        target_delim = value[4]
                        target_filename = store_dir + '/' + target_node + '/tmp/command_output/' + value[2]
                    else:
                        target_parm  = value[2]
                        target_delim = value[3]
                        target_filename = store_dir + '/' + target_node + value[1]

                    # Get current value
                    if target_parm == None:
                        current_entry = grep_file(target_filename)
                        current_value = current_entry
                        target_parm   = '-'
                    elif target_delim == '\s':
                        current_entry = grep_file(target_filename, target_parm, target_delim)
                        current_list  = re.split(target_delim, current_entry)
                        current_value = ' '.join([str(x) for x in current_list[2:]])
                    else:
                        current_entry = grep_file(target_filename, target_parm, target_delim)
                        current_list  = current_entry.split(target_delim)
                        current_value = str(current_list[1].strip())

                    # Compare target value and current value.
                    if target_value == current_value:
                        msg = ('ok: [' + target_node + '] ' + target_product + ' ' + target_filename 
                               + ' [' + target_parm + '] target: ' + target_value 
                               + ' => current_value: ' + current_value )
                        print(Color.GREEN + msg + Color.RESET)
                        ok_cnt += 1
                    else:
                        msg = ('failed: [' + target_node + '] ' + target_product + ' ' + target_filename 
                               + ' [' + target_parm + '] target: ' + target_value 
                               + ' => current_value: ' + current_value )
                        false_values.append(msg)
                        print(Color.RED + msg + Color.RESET)
                        ng_cnt += 1




def main():

    print('\nCOMFIRM [Configuration Files]')
    print('-------------------------------------------------------------------------------------------')
    check_value('files')

    print('\nCOMFIRM [Command Outputs]')
    print('-------------------------------------------------------------------------------------------')
    check_value('cmd')

    print('\nCOMFIRM [Failed Confirmations]')
    print('-------------------------------------------------------------------------------------------')
    for false_value in false_values:
        print(Color.RED + false_value + Color.RESET)

    print('\nCOMFIRM RECAP')
    print('-------------------------------------------------------------------------------------------')
    total_msg = 'total=' + str(ok_cnt + ng_cnt)
    ok_msg = 'ok=' + str(ok_cnt)
    failed_msg = 'failed=' + str(ng_cnt)
    print(total_msg + ',    ' + Color.GREEN + ok_msg + Color.RESET + ',    ' + Color.RED + failed_msg + Color.RESET)


if __name__ == "__main__":
    main()



