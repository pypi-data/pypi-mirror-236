import fsspec
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
fs = fsspec.filesystem(
    "sftp",
    host="slurm.ttic.edu",
    username="yicheng",
    key_filename="/home/yicheng/.ssh/id_ecdsa_ttic",
    sock=paramiko.ProxyCommand("ssh -W slurm.ttic.edu:22 yicheng@ssh.ttic.edu"),
)

print(fs)
