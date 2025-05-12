# caddy_linux_amd64 file-server --listen "$1:$2" --root . --domain "$1"

python ./https_server.py -c config.toml
