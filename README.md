# CSWin - Control Smartphone on Windows 📱💻

Ferramenta inteligente e automática para espelhar e controlar seu Android no Windows via Scrcpy.
Diferente de soluções comuns, o **CSWin** gerencia a conexão ADB automaticamente, memoriza seu dispositivo e recupera a conexão Wi-Fi sozinho.

## 🚀 Funcionalidades Principais

- **🧠 Memória Inteligente:** Não é necessário renomear o arquivo ou digitar IPs. O CSWin salva as configurações automaticamente em `%AppData%`.
- **🔌 Auto-Configuração (USB-to-Wi-Fi):** Se a conexão falhar ou o IP mudar, o CSWin detecta o erro, solicita o cabo USB, descobre o novo IP, abre a porta 5555 e restaura o acesso sem fio automaticamente.
- **✨ UX Aprimorada:** Possui tela de carregamento (Splash Screen) flutuante que informa o status da conexão em tempo real.
- **🏷️ Identificação Personalizada:** Detecta o nome do dono do celular (ex: *"S23 de Jullios"*) e exibe na barra de título da janela.
- **🔋 Modo Foco:** Inicia com a tela do celular desligada (economia de bateria) enquanto mantém o PC acordado.
- **🧹 Auto-Limpeza:** Mata processos `scrcpy` ou `adb` travados antes de iniciar para garantir uma conexão limpa.

---

## 📦 Como Instalar (Para Usuários)

1. Baixe o instalador na aba [Releases](https://github.com/julliosfelix/CSWin/releases).
2. Execute o `Instalador_CSWin_v1.exe`.
3. O atalho será criado na Área de Trabalho e no Menu Iniciar.

> **Nota:** Na primeira execução, o Windows pode exibir o alerta "SmartScreen". Clique em **Mais Informações > Executar assim mesmo** (o app não possui assinatura digital da Microsoft ainda).

---

## 🛠️ Área do Desenvolvedor

Se você quiser modificar o código ou compilar por conta própria.

### Pré-requisitos
- Python 3.12+
- Inno Setup 6 (para criar o instalador)

### 1. Configuração do Ambiente
Clone o repositório e instale as dependências:
```bash
git clone https://github.com/julliosfelix/CSWin.git
cd CSWin
pip install -r requirements.txt 
```
### 2. Como Rodar (Modo Dev)
```bash
python src/CSWin.py
```
### 3. Como Compilar o Executável (.exe)
Para gerar o binário único com ícone embutido:

```Bash
pyinstaller --noconsole --onefile --icon=assets/CSWin.ico src/CSWin.py
```
O executável será gerado na pasta dist/.

### 4. Como Criar o Instalador
Certifique-se de ter a pasta Montagem_CSWin na raiz (com o CSWin.exe compilado e os arquivos do Scrcpy/ADB dentro).

Abra o arquivo Setup_Script.iss com o Inno Setup Compiler.

Clique em Compile.

O instalador final aparecerá na raiz do projeto.

📱 Testado Em
Dispositivo: Samsung Galaxy S23 (SM-S916B)

Sistema: Android 16 / One UI 8.0

Data: 06/01/2026

👨‍💻 Créditos
Desenvolvido por Jullios Felix (Innovfly).