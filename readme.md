# BCI Training Platform #
--------------------------------

** Códigos em python para treinamento de usuário para Interface Cérebro-Máquina **

Mover a pasta bci_training_platform para dentro da pasta catkin_ws/src

Abrir um terminal e navegar até o diretório de workspace do catkin e executar os seguintes comandos:

$ catkin_make

$ cd src/bci_training_platform/scripts

$ chmod +x gui.py

$ chmod +x manager.py

$ chmod +x samples.py

$ chmod +x bci_training_platform.launch


Para rodar executar:

$ roslaunch bci_training_platform bci_training_platform.launch

OBS. Quando o programa se iniciar, para ativá-lo maximize a janela

Criar novo usuário:

START -> NEW USER -> CREATE USER -> digite o usuário e aperte enter -> BACK

Calibração:

START -> EXISTING USER -> digite o usuário e aperte enter

GUIDE  prove instruções sobre a calibração
NEW cria uma nova calibração

o bloco quer fornece as amostrar fornece números pseudo-randomicos por isso o cálculo dos parametros (csp e lda) no node Manager.py não está ativo

quando for fechar, feche a interface gráfica antes de finalizar no terminal o launch














