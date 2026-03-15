# connectivity.py
import subprocess

def ping_check(ip):
    command = f"ping -c 4 -W 10 {ip}"
    try:
        result = subprocess.run(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)
        return result.returncode == 0
    except Exception:
        return False

if __name__ == "__main__":
    main()