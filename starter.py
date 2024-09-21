import os
import subprocess
from time import sleep
from datetime import datetime

# Função para iniciar uma sessão


def start_session(sessions_info):
    try:
        for session_info in sessions_info:
            session_name, tarefa = session_info

            # Verifique se a sessão do Screen está ativa
            if session_name in subprocess.getoutput("screen -ls"):
                print(f"A sessão {session_name} está ativa.")
            else:
                print(f"A sessão {session_name} não está ativa. Iniciando...")

                # Inicie a sessão do Screen com o nome especificado e a tarefa correspondente,
                # redirecionando a saída e os erros para o arquivo de log
                command = f"screen -S {session_name} -d -m python3 {tarefa}"
                subprocess.run(command, shell=True)

                print(f"Sessão {session_name} iniciada com a tarefa: {tarefa}")

                # Registre a data e hora em que a sessão foi iniciada no arquivo de log correspondente
                
                    
    except Exception as e:
        print(f"Erro ao iniciar sessão: {e}")

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    sessions_info = []


    sessions_info.append(["trans_prd", path+"/trans.py"])

    start_session(sessions_info)

    