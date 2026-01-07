import subprocess
import time
import os
import sys
import re
import ctypes

# --- FUNÇÕES AUXILIARES ---
def show_error(titulo, mensagem):
    ctypes.windll.user32.MessageBoxW(0, mensagem, titulo, 0x10)

def get_ip_from_filename():
    if getattr(sys, 'frozen', False):
        filename = os.path.basename(sys.executable)
    else:
        filename = os.path.basename(__file__)
    
    match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", filename)
    return match.group(1) if match else None

def run_command(command_list, wait=True, timeout=None):
    """ Executa comandos com suporte a Timeout (limite de tempo) """
    CREATE_NO_WINDOW = 0x08000000
    try:
        if wait:
            # Tenta executar respeitando o timeout
            result = subprocess.run(
                command_list, 
                creationflags=CREATE_NO_WINDOW, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return result.stdout + result.stderr
        else:
            subprocess.Popen(command_list, creationflags=CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "Launched"
            
    except subprocess.TimeoutExpired:
        return "ERROR_TIMEOUT" # Retorna erro se demorar demais
    except FileNotFoundError:
        return "ERROR_NOT_FOUND"

# --- MAIN ---
def main():
    IP_CELULAR = get_ip_from_filename()
    
    if not IP_CELULAR:
        IP_CELULAR = "192.168.1.82"

    PORTA = "5555"
    NOME_APP = "CSWin"
    titulo_janela = f"{NOME_APP} | {IP_CELULAR}"

    # Limpeza (rápida, sem timeout específico)
    run_command(["taskkill", "/F", "/IM", "scrcpy.exe"], wait=True)
    run_command(["adb", "disconnect"], wait=True)

    # --- CONEXÃO COM TIMEOUT DE 5 SEGUNDOS ---
    address = f"{IP_CELULAR}:{PORTA}"
    # Se não conectar em 5s, ele aborta
    resultado = run_command(["adb", "connect", address], wait=True, timeout=5)

    if "ERROR_NOT_FOUND" in resultado:
        show_error("Erro Grave", "ADB ou Scrcpy não encontrados no PATH do Windows.")
        sys.exit()

    # Verifica se conectou OU se deu timeout
    if "connected" not in resultado.lower():
        mensagem_erro = (
            f"Falha ao conectar em {IP_CELULAR}, tempo esgotado.\n\n"
            
            "Verifique o ip do Smartphone:\n"
            "1. Renomeie o arquivo com o IP correto\n"
            " Ex: CSWin-192.168.1.83.exe\n"
            "2. Verifique se o celular está na mesma rede Wi-Fi"
        )
        show_error("CSWin - Falha na Conexão", mensagem_erro)
        sys.exit()

    time.sleep(1)
    
    scrcpy_args = [
        "scrcpy", 
        "--turn-screen-off", 
        "--stay-awake", 
        "--window-title", titulo_janela
    ]
    
    run_command(scrcpy_args, wait=False)

if __name__ == "__main__":
    main()