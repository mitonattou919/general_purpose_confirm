# Ansible Sample Playbook for general purpose confirmation

## Procedure
### Ansible Installation (Centos8-stream)

1. Installing Python3.9
    ```:Installing Python3.9
    dnf -y module install python39
    ```

1. Activate Python3.9
    ```:
    alternatives --config python
    =>choose python3.9 and press ENTER key.
    ```

1. Installing sshpass
    ```:Installing sshpass
    dnf -y install sshpass
    ```

1. Installing Ansible by PIP
    ```:Installing Ansible by PIP
    python -m pip install ansible
    ansible --version
    ```

1. Installing OpenPyXl by PIP
    ```:Installing Ansible by PIP
    python -m pip install openpyxl
    python -m pip list | grep openpyxl
    ```


### Preparing
1. Modify Excel file.

1. Upload Excel file to Ansible Server.

1. Create inventory and host-variables
    ```:
    cd gp_confirm
    python create_config_confirm.py xxx.xlsx
    ```


### Execution
1. Fetch original files
    ```:
    cd gp_confirm
    ansible-playbook -i <inventory-file> -l <target-hostname> 01_gpc_fetch.yml
    ```

1. Confirm configuration files and command outputs.
    ```:
    python confirm.py xxx.xlsx
    ```

