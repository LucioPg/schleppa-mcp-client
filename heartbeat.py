"""
Processo dummy che funge da heartbeat per il backend Flask
Viene gestito dal backend e terminato dal frontend quando necessario
"""

import time
import sys
import os
import signal
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('heartbeat.log')
    ]
)
logger = logging.getLogger('heartbeat')

# Flag per la gestione della chiusura
running = True


def signal_handler(signum, frame):
    """Gestisce i segnali di terminazione"""
    global running
    logger.info(f"Heartbeat ricevuto segnale {signum}, terminando...")
    running = False


def main():
    """Loop principale del heartbeat"""
    global running

    # Registra i signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if hasattr(signal, 'SIGBREAK'):  # Windows
        signal.signal(signal.SIGBREAK, signal_handler)

    logger.info(f"Heartbeat processo avviato con PID: {os.getpid()}")

    try:
        while running:
            # Il processo non fa nulla, aspetta solo
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Heartbeat interrotto da KeyboardInterrupt")
    except Exception as e:
        logger.error(f"Errore nel heartbeat: {e}")
    finally:
        logger.info("Heartbeat processo terminato")


if __name__ == '__main__':
    main()
