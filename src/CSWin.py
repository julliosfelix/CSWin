import subprocess
import time
import os
import sys
import re
import ctypes
import tkinter as tk

# --- CONFIGURAÇÕES GERAIS ---
NOME_APP = "CSWin by InnovFly"
PORTA_PADRAO = "5555" 

# Constantes para MessageBox
MB_OK = 0x00
MB_OKCANCEL = 0x01
MB_ICONEXCLAMATION = 0x30
MB_ICONINFORMATION = 0x40
ID_OK = 1

# --- NOVA CLASSE: TELA DE CARREGAMENTO (SPLASH) ---
class SplashLoading:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#f0f0f0")
        
        largura, altura = 300, 80
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (largura // 2)
        y = (screen_height // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")
        
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="raised")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=NOME_APP, font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#333").pack(pady=(10, 0))
        
        self.status_label = tk.Label(frame, text="Iniciando...", font=("Segoe UI", 10), bg="#ffffff", fg="#666")
        self.status_label.pack(pady=5)
        
        self.root.update()

    def update_text(self, text):
        self.status_label.config(text=text)
        self.root.update()

    def close(self):
        self.root.destroy()

# --- FUNÇÕES DE INTERFACE ---
def show_message(titulo, mensagem, icone=MB_ICONINFORMATION):
    return ctypes.windll.user32.MessageBoxW(0, mensagem, titulo, icone)

def show_question(titulo, mensagem):
    return ctypes.windll.user32.MessageBoxW(0, mensagem, titulo, MB_ICONEXCLAMATION | MB_OKCANCEL)

def show_success_countdown(ip_detectado):
    root = tk.Tk()
    root.title("Sucesso")
    
    largura, altura = 340, 180
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (largura // 2)
    y = (screen_height // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.attributes('-topmost', True) 

    tk.Label(root, text="Configurado e Salvo!", font=("Segoe UI", 11, "bold"), fg="#28a745").pack(pady=(15, 5))
    tk.Label(root, text=f"IP Gravado: {ip_detectado}", font=("Segoe UI", 10)).pack()
    tk.Label(root, text="O cabo USB já pode ser removido.", font=("Segoe UI", 9), fg="#666").pack(pady=5)

    lbl_timer = tk.Label(root, text="Iniciando em 5s...", font=("Segoe UI", 10, "bold"), fg="#0066cc")
    lbl_timer.pack(pady=5)

    def close_window():
        root.destroy()

    tk.Button(root, text="OK (Iniciar Agora)", command=close_window, width=20, bg="#dddddd").pack(pady=5)

    count = 5
    def update_timer():
        nonlocal count
        if count > 0:
            lbl_timer.config(text=f"Iniciando em {count}s...")
            count -= 1
            root.after(1000, update_timer)
        else:
            close_window()

    root.after(1000, update_timer)
    root.mainloop()

# --- FUNÇÕES DE MEMÓRIA ---
def get_config_path():
    r""" Retorna o caminho: %AppData%\InnovFly\CSWin\config.txt """
    appdata = os.getenv('APPDATA')
    pasta_config = os.path.join(appdata, "InnovFly", "CSWin")
    
    if not os.path.exists(pasta_config):
        try: os.makedirs(pasta_config)
        except: pass
            
    return os.path.join(pasta_config, "config.txt")

def load_ip():
    path = get_config_path()
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                ip = f.read().strip()
                if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
                    return ip
        except: pass
    return None

def save_ip(ip):
    if not ip: return
    path = get_config_path()
    try:
        with open(path, "w") as f:
            f.write(ip)
    except: pass

# --- FUNÇÕES ADB ---
def run_command(command_list, wait=True, timeout=None):
    CREATE_NO_WINDOW = 0x08000000
    try:
        if wait:
            # encoding='utf-8' ajuda a ler nomes com acentos
            result = subprocess.run(
                command_list, creationflags=CREATE_NO_WINDOW, 
                capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=timeout
            )
            return result.stdout + result.stderr
        else:
            subprocess.Popen(command_list, creationflags=CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "Launched"
    except subprocess.TimeoutExpired:
        return "ERROR_TIMEOUT"
    except FileNotFoundError:
        return "ERROR_NOT_FOUND"

def get_device_ip_via_usb():
    output = run_command(["adb", "shell", "ip", "route"], wait=True)
    match = re.search(r"src (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", output)
    if match: return match.group(1)
    return None

def get_device_friendly_name():
    """ Tenta descobrir o nome amigável do celular (ex: S23 de Jullios) """
    # Tentativa 1: Nome definido pelo usuário
    nome = run_command(["adb", "shell", "settings", "get", "global", "device_name"], wait=True)
    nome = nome.strip()
    
    # Valida se veio algo útil (às vezes retorna 'null' ou vazio)
    if nome and "null" not in nome.lower() and "error" not in nome.lower():
        return nome
    
    # Tentativa 2: Modelo do aparelho (ex: SM-S901E)
    modelo = run_command(["adb", "shell", "getprop", "ro.product.model"], wait=True)
    return modelo.strip()

def configurar_via_usb(motivo_erro):
    msg = (
        f"{motivo_erro}\n\n"
        "Vamos configurar automaticamente via USB?\n"
        "1. Conecte o cabo USB agora.\n"
        "2. Clique em OK."
    )
    resp = show_question("Configuração Necessária", msg)
    if resp != ID_OK: return None

    loading = SplashLoading()
    loading.update_text("Buscando celular no USB...")

    devices = run_command(["adb", "devices"], wait=True)
    if "device\n" not in devices.replace("List of devices attached", ""):
        loading.close()
        show_message("Erro", "Celular não detectado.\nVerifique cabo e Depuração USB.", MB_ICONEXCLAMATION)
        return None

    loading.update_text("Lendo IP do dispositivo...")
    novo_ip = get_device_ip_via_usb()
    
    loading.update_text("Abrindo porta 5555...")
    run_command(["adb", "tcpip", "5555"], wait=True)
    time.sleep(2) 
    
    loading.close() 

    if novo_ip:
        save_ip(novo_ip)
        show_success_countdown(novo_ip)
        return novo_ip
    else:
        return "MANTER"

def main():
    splash = SplashLoading()
    splash.update_text("Lendo configurações...")

    ip_atual = load_ip()
    
    run_command(["taskkill", "/F", "/IM", "scrcpy.exe"], wait=True)
    run_command(["adb", "disconnect"], wait=True)

    resultado_conexao = ""
    
    # TENTATIVA AUTOMÁTICA
    if ip_atual:
        splash.update_text(f"Conectando a {ip_atual}...")
        address = f"{ip_atual}:{PORTA_PADRAO}"
        resultado_conexao = run_command(["adb", "connect", address], wait=True, timeout=5)
        
        if "ERROR_NOT_FOUND" in resultado_conexao:
            splash.close()
            show_message("Erro Fatal", "ADB ou Scrcpy não encontrados.", MB_ICONEXCLAMATION)
            sys.exit()

    conectado = "connected" in resultado_conexao.lower()
    
    # RECUPERAÇÃO / SETUP USB
    if not conectado:
        splash.close() 
        motivo = "IP não salvo." if not ip_atual else "Falha ao conectar no IP salvo."
        novo_ip = configurar_via_usb(motivo)
        
        if novo_ip and novo_ip != "MANTER":
            ip_atual = novo_ip
        
        if ip_atual:
            splash = SplashLoading() 
            splash.update_text("Finalizando conexão...")
            address = f"{ip_atual}:{PORTA_PADRAO}"
            resultado_conexao = run_command(["adb", "connect", address], wait=True, timeout=5)
    
    if "connected" not in resultado_conexao.lower():
        try: splash.close() 
        except: pass
        sys.exit()

    # --- NOVO: Obtendo o nome do dono ---
    splash.update_text("Identificando usuário...")
    nome_celular = get_device_friendly_name()
    
    # Se não achou nome nenhum, usa o IP
    if not nome_celular:
        nome_celular = ip_atual

    # Monta o título da janela: "CSWin - S23 de Jullios"
    titulo_janela = f"{NOME_APP} - {nome_celular}"
    
    splash.close()

    # LANÇAR SCROPY COM O NOME CERTO
    scrcpy_args = [
        "scrcpy", 
        "--turn-screen-off", 
        "--stay-awake", 
        "--window-title", titulo_janela
    ]
    run_command(scrcpy_args, wait=True)

    run_command(["adb", "disconnect"], wait=True)
    run_command(["adb", "kill-server"], wait=True)

if __name__ == "__main__":
    main()