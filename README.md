# useful-scripts

h2. ssh-add-keys.sh

Simple script that looks for SSH private keys and adds them using ssh-add command. It assumes that ssh-agent is already running. And another good part is if putty-tools package is installed, it detects Putty Private keys, converts them to openssh format and then execute ssh-add!

Usage: bash ssh-add-keys.sh <timeout> <dir>
Legend:
  timeout - optional. default infinite. how long key should be retained by SSH agent. E.g. 1h, 1d, 1w, 1m etc. 
  dir - optional. default ~/.ssh/key.d/. directory where all SSH private keys are stored.
