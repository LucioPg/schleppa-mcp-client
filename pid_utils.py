import os
import json
import time
import sys
import subprocess
import psutil
from pathlib import Path
from logging import getLogger
import threading

logger = getLogger(__name__)

PID_FILE = Path(__file__).parent / 'backend.pid'
STATUS_FILE = Path(__file__).parent / 'backend_status.json'

# Variabili globali per il heartbeat
heartbeat_process = None
heartbeat_pid = None
heartbeat_monitor_thread = None  # <-- MANCAVA QUESTA
heartbeat_running = True         # <-- MANCAVA QUESTA
shutdown_callback = None         # <-- MANCAVA QUESTA


def write_pid_file(flask_port):
    """Scrive il PID del processo corrente nel file"""
    try:
        pid_data = {
            'pid': os.getpid(),
            'port': flask_port,
            'timestamp': time.time()
        }

        with open(PID_FILE, 'w') as f:
            json.dump(pid_data, f)

        # Scrive anche lo status
        status_data = {
            'status': 'running',
            'pid': os.getpid(),
            'port': flask_port,
            'timestamp': time.time()
        }

        with open(STATUS_FILE, 'w') as f:
            json.dump(status_data, f)

        logger.info(f"PID file created: {PID_FILE.absolute()}")
        logger.info(f"Status file created: {STATUS_FILE.absolute()}")

    except Exception as e:
        logger.error(f"Error writing PID file: {e}")


def __cleanup_pid_file(flask_port):
    """Rimuove il file PID alla chiusura del processo"""
    try:
        # if PID_FILE.exists():
        #     PID_FILE.unlink()
        #     logger.info(f"PID file removed: {PID_FILE.absolute()}")

        if STATUS_FILE.exists():
            # Aggiorna lo status invece di rimuovere
            status_data = {
                'status': 'stopped',
                'pid': None,
                'port': flask_port,
                'timestamp': time.time()
            }

            with open(STATUS_FILE, 'w') as f:
                json.dump(status_data, f)

            logger.info(f"Status file updated: {STATUS_FILE.absolute()}")
    except Exception as e:
        logger.error(f"Error cleaning up PID file: {e}")


def start_heartbeat():
    """Avvia il processo heartbeat"""
    global heartbeat_process, heartbeat_pid
    
    if heartbeat_process is not None:
        return heartbeat_pid
    
    try:
        # Determina come avviare il processo heartbeat
        current_dir = os.path.dirname(os.path.abspath(__file__))
        heartbeat_path = os.path.join(current_dir, "heartbeat.py")
        
        logger.info(f"Directory corrente: {current_dir}")
        logger.info(f"Path heartbeat: {heartbeat_path}")
        
        # Controlla se il file esiste
        if not os.path.exists(heartbeat_path):
            logger.error(f"File heartbeat.py non trovato: {heartbeat_path}")
            return None
        
        # Usa lo stesso metodo di avvio del backend
        # if os.path.exists(os.path.join(current_dir, 'uv.lock')) or \
        #    os.path.exists(os.path.join(current_dir, 'pyproject.toml')):
        #     # Usa UV
        #     cmd = ["uv", "run", heartbeat_path]
        # else:
        #     # Usa Python direttamente
        #     cmd = [sys.executable, heartbeat_path]
        cmd = [sys.executable, heartbeat_path]
        logger.info(f"Avvio processo heartbeat: {' '.join(cmd)}")
        
        heartbeat_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        heartbeat_pid = heartbeat_process.pid
        logger.info(f"Processo heartbeat avviato con PID: {heartbeat_pid}")
        
        # Verifica che il processo sia effettivamente avviato
        time.sleep(0.5)  # Piccola pausa
        if heartbeat_process.poll() is not None:
            # Il processo è già terminato
            stdout, stderr = heartbeat_process.communicate()
            logger.error(f"Heartbeat process terminated immediately")
            logger.error(f"STDOUT: {stdout}")
            logger.error(f"STDERR: {stderr}")
            heartbeat_process = None
            heartbeat_pid = None
            return None
        
        # Avvia il monitoraggio del heartbeat
        start_heartbeat_monitor()  # <-- QUESTA CHIAMATA MANCAVA
        
        return heartbeat_pid
        
    except Exception as e:
        logger.error(f"Errore nell'avvio del processo heartbeat: {e}", exc_info=True)
        return None


def stop_heartbeat():
    """Ferma il processo heartbeat"""
    global heartbeat_process, heartbeat_pid, heartbeat_running
    
    # Ferma il monitoraggio
    heartbeat_running = False
    
    if heartbeat_process is not None:
        try:
            logger.info(f"Terminando processo heartbeat PID: {heartbeat_pid}")
            heartbeat_process.terminate()
            
            # Aspetta un po' per la terminazione graceful
            try:
                heartbeat_process.wait(timeout=5)
                logger.info("Processo heartbeat terminato gracefully")
            except subprocess.TimeoutExpired:
                # Se non si termina, forza la terminazione
                logger.warning("Forzando terminazione processo heartbeat")
                heartbeat_process.kill()
                heartbeat_process.wait(timeout=2)
                logger.info("Processo heartbeat terminato forzatamente")
                
        except Exception as e:
            logger.error(f"Errore nella terminazione del processo heartbeat: {e}")
        finally:
            heartbeat_process = None
            heartbeat_pid = None


def start_heartbeat_monitor():
    """Avvia il thread di monitoraggio del heartbeat"""
    global heartbeat_monitor_thread, heartbeat_running
    
    if heartbeat_monitor_thread is not None and heartbeat_monitor_thread.is_alive():
        logger.info("Thread di monitoraggio heartbeat già in esecuzione")
        return
    
    heartbeat_running = True
    heartbeat_monitor_thread = threading.Thread(target=monitor_heartbeat, daemon=True)
    heartbeat_monitor_thread.start()
    logger.info("Thread di monitoraggio heartbeat avviato")


def monitor_heartbeat():
    """Monitora il processo heartbeat e chiama la callback se non esiste più"""
    global heartbeat_pid, heartbeat_running, shutdown_callback

    logger.info("Inizio monitoraggio heartbeat...")

    while heartbeat_running:
        try:
            if heartbeat_pid and not psutil.pid_exists(heartbeat_pid):
                logger.warning(f"Processo heartbeat {heartbeat_pid} non più in esecuzione")
                logger.info("Avvio shutdown automatico del backend...")

                # Ferma il monitoraggio
                heartbeat_running = False

                # Chiama la callback di shutdown se impostata
                if shutdown_callback:
                    logger.info("Chiamando callback di shutdown...")
                    try:
                        shutdown_callback()
                    except Exception as e:
                        logger.error(f"Errore nella callback di shutdown: {e}")

                # Forza l'uscita dopo un breve delay se la callback non funziona
                def force_exit():
                    time.sleep(3)
                    logger.info("Forzando l'uscita del processo...")
                    os._exit(0)

                exit_thread = threading.Thread(target=force_exit, daemon=True)
                exit_thread.start()
                break

        except Exception as e:
            logger.error(f"Errore nel monitoraggio heartbeat: {e}")

        # Check ogni 2 secondi
        time.sleep(2)

    logger.info("Thread di monitoraggio heartbeat terminato")


def get_heartbeat_pid():
    """Restituisce il PID del processo heartbeat, avviandolo se necessario"""
    global heartbeat_pid
    
    if heartbeat_pid is None:
        # Se il heartbeat non è ancora stato avviato, avvialo ora
        heartbeat_pid = start_heartbeat()
    
    if heartbeat_pid is not None:
        # Verifica che il processo sia ancora vivo
        if psutil.pid_exists(heartbeat_pid):
            return heartbeat_pid
        else:
            logger.warning("Processo heartbeat non più esistente, riavviando...")
            heartbeat_process = None  # Reset del processo
            heartbeat_pid = start_heartbeat()
            return heartbeat_pid
            
    logger.error("Impossibile avviare o ottenere il processo heartbeat")
    return None


def get_heartbeat_status():
    """Verifica lo status del processo heartbeat"""
    global heartbeat_pid
    
    if heartbeat_pid is None:
        return {"status": "not_started", "heartbeat_pid": None}
    
    if psutil.pid_exists(heartbeat_pid):
        return {"status": "running", "heartbeat_pid": heartbeat_pid}
    else:
        return {"status": "dead", "heartbeat_pid": heartbeat_pid}


def set_shutdown_callback(callback):
    """Imposta la callback da chiamare quando il heartbeat muore"""
    global shutdown_callback
    shutdown_callback = callback
    logger.info("Callback di shutdown impostata")


def register_heartbeat_process(process):
    """Registra il processo heartbeat per la gestione"""
    global heartbeat_process, heartbeat_pid
    heartbeat_process = process
    heartbeat_pid = process.pid


# Modifica atexit per includere la pulizia del PID e del heartbeat
def cleanup_all(flask_port, cleanup_func=None, *args, **kwargs):
    # Ferma il heartbeat prima
    stop_heartbeat()
    
    # Esegui la funzione di cleanup personalizzata se fornita
    if cleanup_func is not None:
        cleanup_func(*args, **kwargs)
    
    # Cleanup del PID file
    __cleanup_pid_file(flask_port)


def cleanup_processes(processes):
    """Rimuove i processi specificati"""
    for process in processes:
        try:
            if process and process.poll() is None:  # Processo ancora in esecuzione
                logger.info(f"Terminating process PID: {process.pid}")
                process.terminate()
                
                # Aspetta un po' per la terminazione graceful
                try:
                    process.wait(timeout=5)
                    logger.info(f"Process PID {process.pid} terminated gracefully")
                except subprocess.TimeoutExpired:
                    # Se non si termina, forza la terminazione
                    logger.warning(f"Force killing process PID: {process.pid}")
                    process.kill()
                    try:
                        process.wait(timeout=2)
                        logger.info(f"Process PID {process.pid} force killed")
                    except subprocess.TimeoutExpired:
                        logger.error(f"Failed to kill process PID: {process.pid}")
        except Exception as e:
            logger.error(f"Error terminating process: {e}")