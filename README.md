# ogcli-restore-rollback

This script addresses the case when ogcli restore runs into an error. When an error occurs, any configuration in the config template prior to the error remains active on the device. The script enhances ogcli restore by adding a rollback if an error is detected during the restore process putting the device in the pre-restore config state. This script is a wrapper of the ogcli restore command.

Usage: python3 ogcli-restore.py "template"

Example: python3 ogcli-restore.py my-template.txt
