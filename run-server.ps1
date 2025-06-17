param(
    [Parameter(Mandatory=$true)]
    [string]$IP,
    
    [ValidateRange(1, 65535)]
    [int]$PORT
)

.\caddy.exe file-server --listen ${IP}:${PORT} --root . --domain $IP

