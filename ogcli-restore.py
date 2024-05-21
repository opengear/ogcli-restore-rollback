#!/usr/bin/python3
#
# ogcli-restore.py
# Script runs ogcli restore with rollback if an error is detected
#
# Usage: ogcli-restore.py <template>


import argparse
from datetime import datetime
import os
import shutil
import time

# Argparse for user to specify template file name
def userArgs():

    # Create the parser
    parser = argparse.ArgumentParser(description="Tells the script which template to use.")

    # Add the argument for the file
    parser.add_argument('variable', type=str, help="Template name used for restore.")

    # Parse the arguments
    args = parser.parse_args()
    fileName = args.variable
    command = f'ogcli restore {fileName}'

    print(f'Running {command}...\n')

    return command

# Create a rollback of the config db prior to restore
def backUpDb(rollbackFile):

    # Specify the source and destination file paths
    source_path = '/etc/config/ngcs.db'
    destination_path = rollbackFile

    try:
        # Copy the file from source to destination
        shutil.copy(source_path, destination_path)
        print(f"\nCreating config rollback...\n")
        time.sleep(1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run ogcli restore
def restore(rollbackFile):

    command = userArgs()

    output = os.system(command)

    if output == 0:
        time.sleep(1)
        print('\nExiting...\n')
    else:
        print('\nError detected in template. Please check your template.')
        time.sleep(1)
        print('\nRolling back config...')
        time.sleep(1)
        rollback(rollbackFile)

# Rollback in the event of an error
def rollback(rollbackFile):

    # Specify the source and destination file paths
    source_path = rollbackFile
    destination_path = '/etc/config/ngcs.db'

    try:
        # Copy the file from source to destination
        shutil.copy(source_path, destination_path)
        print(f"\nRollback complete. Exiting...\n")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        

if __name__ == "__main__":

    # Create timestamped rollback file name 
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    rollbackFile = f'/tmp/rollbacks/rollback_{timestamp}.db'

    backUpDb(rollbackFile)

    restore(rollbackFile)