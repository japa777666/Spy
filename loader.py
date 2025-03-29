import sys
import time
import zipfile
import os
import shutil
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class InstallerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Instalador de Aplicativo")
        self.setGeometry(300, 200, 900, 500)
        self.setWindowIcon(QIcon("icon.png"))

        # Estilo da janela com fundo escuro e bordas arredondadas
        self.setStyleSheet("""
            background-color: #1e1e1e;
            border-radius: 10px;
            color: #ffffff;
        """)

        layout = QVBoxLayout()

        # Título estilizado com fonte alterada
        self.label = QLabel("Clique abaixo para iniciar o processo de instalação", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))  # Fonte alterada para Arial
        self.label.setStyleSheet("color: #ffffff;")
        layout.addWidget(self.label)

        # Layout para o botão e barra de progresso
        button_layout = QHBoxLayout()

        # Botão para iniciar a instalação
        self.install_button = QPushButton("Iniciar Instalação", self)
        self.install_button.setFont(QFont("Courier New", 16, QFont.Weight.Bold))
        self.install_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 15px;
                border-radius: 12px;
                border: 2px solid #2980b9;
                font-size: 18px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border: 2px solid #1f6391;
                transform: scale(1.1);
            }
            QPushButton:pressed {
                background-color: #1f6391;
                border: 2px solid #1a4f77;
                transform: scale(0.95);
            }
        """)
        self.install_button.clicked.connect(self.start_installation)
        button_layout.addWidget(self.install_button)

        # Barra de progresso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #34495e;
                border-radius: 10px;
                height: 20px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #16a085;
                border-radius: 10px;
            }
        """)
        button_layout.addWidget(self.progress_bar)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def start_installation(self):
        self.label.setText("Instalação em andamento...")
        self.install_button.setEnabled(False)

        # Efeito visual no botão durante a instalação
        self.install_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                padding: 18px;
                border-radius: 12px;
                border: 2px solid #e67e22;
                font-size: 18px;
            }
        """)

        # Alterar o texto do botão
        self.install_button.setText("Instalando...")

        # Animação para a barra de progresso
        self.progress_bar.setValue(0)
        for i in range(101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()  # Atualiza a interface durante o loop
            time.sleep(0.05)

        # Criar o arquivo Painel.bat após a instalação
        self.create_bat_file()

        # Quando a instalação terminar, mudar o fundo e o botão
        self.label.setText("Instalação concluída!")
        self.progress_bar.setValue(100)
        self.install_button.setEnabled(True)

        # Mudando o botão para verde e alterando o texto
        self.install_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 18px;
                border-radius: 12px;
                border: 2px solid #27ae60;
                font-size: 18px;
            }
        """)
        self.install_button.setText("Instalação Completa!")

    def create_bat_file(self):
        bat_content = r'''@echo off
cls
echo ==========================================
echo    Painel de Limpeza e Otimizacao do PC
echo ==========================================
echo.
echo 1 - Limpar arquivos temporarios
echo 2 - Limpar cache do navegador
echo 3 - Limpar a lixeira
echo 4 - Desfragmentar o disco
echo 5 - Sair
echo.

set /p opcao="Escolha uma opcao (1-5): "

if "%opcao%"=="1" goto limpar_temp
if "%opcao%"=="2" goto limpar_cache
if "%opcao%"=="3" goto limpar_lixeira
if "%opcao%"=="4" goto desfragmentar
if "%opcao%"=="5" exit

:limpar_temp
echo.
echo Limpando arquivos temporarios...
del /q /f /s %temp%\*
rd /s /q %temp%
md %temp%

del /q /f /s C:\Windows\Temp\*
rd /s /q C:\Windows\Temp
md C:\Windows\Temp

echo Arquivos temporarios limpos com sucesso!
pause
goto menu

:limpar_cache
echo.
echo Limpando cache do navegador...
del /q /f /s "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\Cache\*"
del /q /f /s "C:\Users\%USERNAME%\AppData\Local\Microsoft\Edge\User Data\Default\Cache\*"
echo Cache do navegador limpo com sucesso!
pause
goto menu

:limpar_lixeira
echo.
echo Limpando a lixeira...
rd /s /q C:\$Recycle.bin
echo Lixeira limpa com sucesso!
pause
goto menu

:desfragmentar
echo.
echo Iniciando desfragmentacao do disco...
defrag C: /O
echo Desfragmentacao concluida!
pause
goto menu

:menu
cls
echo ==========================================
echo    Painel de Limpeza e Otimizacao do PC
echo ==========================================
echo.
echo 1 - Limpar arquivos temporarios
echo 2 - Limpar cache do navegador
echo 3 - Limpar a lixeira
echo 4 - Desfragmentar o disco
echo 5 - Sair
echo.
set /p opcao="Escolha uma opcao (1-5): "

if "%opcao%"=="1" goto limpar_temp
if "%opcao%"=="2" goto limpar_cache
if "%opcao%"=="3" goto limpar_lixeira
if "%opcao%"=="4" goto desfragmentar
if "%opcao%"=="5" exit
'''
        # Caminho onde o arquivo .bat será criado no Desktop
        bat_file_path = os.path.join(os.getenv('USERPROFILE'), 'Desktop', 'Painel.bat')

        # Escrever o conteúdo no arquivo .bat
        with open(bat_file_path, 'w') as bat_file:
            bat_file.write(bat_content)

        print(f"{bat_file_path} criado com sucesso!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstallerApp()
    window.show()
    sys.exit(app.exec())
