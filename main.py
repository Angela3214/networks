import re
import subprocess
import argparse

args = argparse.ArgumentParser()

pat = re.compile(
    r"^(https?:\/\/)?((?:[-a-z0-9._~!$&\'()*+,;=]|%[0-9a-f]{2})+(?::(?:[-a-z0-9._~!$&\'()*+,;=]|%[0-9a-f]{2})+)?@)?(?:((?:(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))|((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z][a-z0-9-]*[a-z0-9]))(:\d+)?((?:\/(?:[-a-z0-9._~!$&\'()*+,;=:@]|%[0-9a-f]{2})+)*\/?)(\?(?:[-a-z0-9._~!$&\'()*+,;=:@\/?]|%[0-9a-f]{2})*)?(\#(?:[-a-z0-9._~!$&\'()*+,;=:@\/?]|%[0-9a-f]{2})*)?$"
)

args.add_argument("host")

if not pat.match(args.parse_args().host):
    print(f"Wrong format for {args.parse_args().host}")
    exit(1)


if subprocess.run(
    ["cat", "/proc/sys/net/ipv4/icmp_echo_ignore_all"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
).stdout == 1:
    print(
        "ISCMP is disabled"
    )
    exit(1)

l = 0
r = 9001 - 28

while l < r - 1:
    mid = (l + r) // 2
    type_of_com = ["ping", args.parse_args().host, "-M", "do", "-s", str(mid), "-c", "3"]
    res: subprocess.CompletedProcess = subprocess.run(type_of_com, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,)
    if res.returncode:
        r = mid
    elif not res.returncode:
        l = mid
    else:
        exit(res.stderr)

print("MTU =", l + 28)
