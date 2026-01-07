# CSWin - Control Smartphone in Windows 📱💻

Ferramenta leve e automática para espelhar e controlar seu Android no Windows via Scrcpy.

## 🚀 Funcionalidades
- **Auto-conexão:** Detecta IP do dispositivo pelo nome do arquivo ou usa fallback.
- **Limpeza:** Encerra processos `scrcpy` e `adb` travados antes de iniciar.
- **Modo Foco:** Inicia com a tela do celular desligada (economia de bateria) e mantém o PC acordado.
- **Ícone Personalizado:** Aplica ícone nativo na janela do espelhamento.

## 📋 Pré-requisitos
1. **Scrcpy:** Deve estar instalado e configurado no PATH do Windows.
2. **ADB:** Deve estar habilitado no celular (Depuração USB/Wireless).

## 🛠️ Como Usar (Dev)
1. Instale a dependência de compilação:
    pip install -r requirements.txt
2. Execute o script:
    python src/CSWin.py
3. Como Compilar (.exe)
    pyinstaller --noconsole --onefile --icon=assets/CSWin.ico --add-data "assets/CSWin.ico;." --name="CSWin-192.168.1.83" src/CSWin.py
4. O executável ficará na pasta dist/.

Desenvolvido por Jullios Felix (Innovfly)
"testado no Samsung Galaxy S23 (SM-S916B), Android 16, One UI 16, em 06/01/2026"
