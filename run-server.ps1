param(
    [Parameter(Mandatory=$true)]
    [string]$IP,
    
    [ValidateRange(1, 65535)]
    [int]$PORT
)

caddy_windows_amd64.exe file-server --listen ${IP}:${PORT} --root . --domain $IP

