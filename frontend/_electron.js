const {app, BrowserWindow, ipcMain, dialog} = require('electron');
const path = require('path');
const {spawn} = require('child_process');
const isDev = require('electron-is-dev');
const dotenv = require('dotenv');
const envPath = path.resolve(__dirname, '..', '.env');
const stripAnsi = require('strip-ansi').default;
dotenv.config({path: envPath});
const FLASK_PORT = process.env.FLASK_PORT || 5008;
const FLASK_HOST = process.env.FLASK_HOST || 'localhost';
const VITE_PORT = process.env.VITE_PORT || 5173;
const VITE_HOST = process.env.VITE_HOST || 'localhost';
const VITE_URL = `http://${VITE_HOST}:${VITE_PORT}`;

console.log('VITE_URL:', VITE_URL);
console.log('FLASK_PORT:', FLASK_PORT);

// Mantieni un riferimento globale dell'oggetto window
let mainWindow;
let backendProcess;
let viteProcess;
let backendProcesses = [];
let heartbeatPid = null;

/*
 * Ottiene il PID del processo heartbeat dal backend
 */
async function getHeartbeatPid() {
    const axios = require('axios');

    try {
        const response = await axios.get(`http://${FLASK_HOST}:${FLASK_PORT}/api/heartbeat_pid`);
        heartbeatPid = response.data.heartbeat_pid;
        console.log('Heartbeat PID ottenuto:', heartbeatPid);
        return heartbeatPid;
    } catch (error) {
        console.error('Errore nell\'ottenere il PID heartbeat:', error.message);
        return null;
    }
}

/**
 * Ferma il processo heartbeat tramite PID
 */
function stopHeartbeatByPid(pid) {
    if (!pid) return;

    console.log(`Stopping heartbeat process with PID: ${pid}`);

    try {
        if (process.platform === 'win32') {
            // Su Windows
            spawn('taskkill', ['/pid', pid.toString(), '/f', '/t'], {stdio: 'ignore'});
        } else {
            // Su Unix/Linux/macOS
            process.kill(pid, 'SIGTERM');
        }

        console.log('Heartbeat process terminated');
    } catch (error) {
        console.error('Error stopping heartbeat process:', error);
    }
}

/**
 * Ferma il backend in modo elegante tramite heartbeat
 */
async function stopBackendGracefully() {
    console.log('Initiating graceful backend shutdown...');

    // Prima ottieni il PID del heartbeat se non lo abbiamo già
    if (!heartbeatPid) {
        console.log('Getting heartbeat PID from backend...');
        await getHeartbeatPid();

        // Aspetta un po' per assicurarsi che il backend sia pronto
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Ferma il heartbeat, causando la chiusura automatica del backend
    if (heartbeatPid) {
        stopHeartbeatByPid(heartbeatPid);
        console.log('Heartbeat stopped, backend should shutdown automatically');

        // Aspetta un po' per permettere al backend di fare cleanup
        await new Promise(resolve => setTimeout(resolve, 3000));
    } else {
        console.log('No heartbeat PID available, falling back to direct termination');
        // Fallback al metodo originale
        stopBackend();
    }
}


/**
 * Avvia il server Vite in modalità development
 */
function startViteServer() {
    if (!isDev) return Promise.resolve();

    return new Promise((resolve, reject) => {
        console.log('Starting Vite development server...');

        viteProcess = spawn('npm', ['run', 'dev'], {
            cwd: __dirname,
            stdio: 'pipe',
            shell: true
        });

        let serverReady = false;

        viteProcess.stdout.on('data', (data) => {
            const output = stripAnsi(data.toString());
            console.log('Vite: ', output);

            // Rileva quando il server è pronto
            if (output.includes('Local:') && !serverReady) {
                serverReady = true;
                console.log('Vite server is ready!');
                resolve();
            }
        });

        viteProcess.stderr.on('data', (data) => {
            console.error('Vite error:', data.toString());
        });

        viteProcess.on('close', (code) => {
            console.log(`Vite process exited with code ${code}`);
        });

        viteProcess.on('error', (err) => {
            console.error('Failed to start Vite server:', err);
            reject(err);
        });

        // Timeout dopo 30 secondi
        setTimeout(() => {
            if (!serverReady) {
                console.log('Vite server timeout, proceeding anyway...');
                resolve();
            }
        }, 30000);
    });
}

/**
 * Ferma il server Vite
 */
function stopViteServer() {
    if (viteProcess) {
        console.log('Stopping Vite server...');
        if (process.platform === 'win32') {
            // Su Windows, forza la terminazione
            spawn('taskkill', ['/pid', viteProcess.pid, '/f', '/t'], {stdio: 'ignore'});
        } else {
            // Su Unix/Linux/macOS
            viteProcess.kill('SIGTERM');
        }

        console.log('Stopped Vite server...');
    }
}

/**
 * Crea la finestra principale dell'applicazione
 */
function createWindow() {
    // Crea la finestra del browser
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, 'preload.js'),
            webSecurity: true
        },
        icon: path.join(__dirname, 'assets', 'icon.png'), // Opzionale: aggiungi un'icona se hai
        show: false, // Non mostrare finché non è pronta
        titleBarStyle: 'default',
        backgroundColor: '#121212' // Colore di sfondo scuro per evitare flash bianco
    });

    // URL da caricare
    const startUrl = isDev
        ? `${VITE_URL}`
        : `file://${path.join(__dirname, '../dist/index.html')}`;

    // Carica l'app
    mainWindow.loadURL(startUrl);

    // Mostra la finestra quando è pronta
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();

        // Apri DevTools solo in development
        if (isDev) {
            mainWindow.webContents.openDevTools();
        }
    });

    // Gestisce la chiusura della finestra
    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    // Gestisce i link esterni
    mainWindow.webContents.setWindowOpenHandler(({url}) => {
        require('electron').shell.openExternal(url);
        return {action: 'deny'};
    });

    // Gestisce errori di caricamento
    mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
        console.error('Failed to load:', errorCode, errorDescription);

        // Se è in development e il server Vite non è ancora pronto, riprova
        if (isDev && errorCode === -102) {
            setTimeout(() => {
                mainWindow.loadURL(startUrl);
            }, 1000);
        }
    });
}

/**
 * Avvia il backend Flask
 */
function startBackend() {
    if (backendProcess) return;
    // Check if uv is available
    const fs = require('fs');
    let useUv = false;
    // Check if we have a uv.lock or pyproject.toml (indicators of uv usage)
    const uvLockPath = path.join(__dirname, '..', 'uv.lock');
    const pyprojectPath = path.join(__dirname, '..', 'pyproject.toml');

    if (fs.existsSync(uvLockPath) || fs.existsSync(pyprojectPath)) {
        useUv = true;
        console.log('UV project detected, using uv run');
    }
    let pythonCmd, pyargs;
    const backendPath = isDev
    ? path.join(__dirname, '..', 'flask_app.py')
    : path.join(process.resourcesPath, 'flask_app.py');
    if (useUv) {
        pythonCmd = 'uv';
        /*
        Per usare gli argomenti --host e --port bisogna adattare il codice python perché accetti gli argomenti
        pyargs = ['run', 'python', backendPath, '--host', FLASK_HOST, '--port', FLASK_PORT];
         */
        pyargs = ['run', backendPath];
    }
    else {
        // Percorso all'ambiente virtuale
        const venvPath = path.join(__dirname, '..', '.venv');

        // Comando per avviare il backend
        if (process.platform === 'win32') {
            // Windows
            pythonCmd = path.join(venvPath, 'Scripts', 'python.exe');
        } else {
            // macOS/Linux
            pythonCmd = path.join(venvPath, 'bin', 'python');
        }
        pyargs = [backendPath];
    }

    try {


        console.log('Starting Flask backend from:', backendPath);


        backendProcess = spawn(pythonCmd, pyargs, {
            stdio: ['pipe', 'pipe', 'pipe'],
            env: {...process.env, FLASK_ENV: 'production'}
        });
        backendProcesses.push(backendProcess);
        // Gestisce l'output del backend
        backendProcess.stdout.on('data', (data) => {
            console.log('Backend stdout:', data.toString());

            // Notifica al frontend che il backend è pronto
            if (mainWindow && data.toString().includes('Running on')) {
                mainWindow.webContents.send('backend-status', {status: 'ready'});
                // Ottieni il PID del heartbeat dopo un breve delay
                setTimeout(async () => {
                    await getHeartbeatPid();
                }, 2000);

            }
        });

        backendProcess.stderr.on('data', (data) => {
            console.error('Backend stderr:', data.toString());

            // Notifica al frontend di errori del backend
            if (mainWindow) {
                mainWindow.webContents.send('backend-status', {
                    status: 'error',
                    message: data.toString()
                });
            }
        });

        backendProcess.on('close', (code) => {
            console.log(`Backend process exited with code ${code}`);
            backendProcess = null;

            // Notifica al frontend che il backend si è fermato
            if (mainWindow) {
                mainWindow.webContents.send('backend-status', {status: 'stopped'});
            }
        });

        backendProcess.on('error', (err) => {
            console.error('Failed to start backend:', err);

            // Mostra dialog di errore
            if (mainWindow) {
                dialog.showErrorBox('Backend Error',
                    'Failed to start the Python backend. Please ensure Python is installed and flask_app.py is available.');
            }
        });

    } catch (error) {
        console.error('Error starting backend:', error);
    }
}

/**
 * Ferma il backend Flask
 */
function stopBackend() {
    let buffer = [...backendProcesses]
    for (let i = 0; i < buffer.length; i++) {
        let backend = buffer[i];
        console.log(`Stopping backend process with PID: ${backend.pid}`);
        if (process.platform === 'win32') {
            // Su Windows, usa taskkill per terminare forzatamente
            spawn('taskkill', ['/pid', backend.pid, '/f', '/t'], {stdio: 'ignore'});
        } else {
            // Su Unix/Linux/macOS
            backend.kill('SIGTERM');

            // Se non si ferma, forza la terminazione dopo 5 secondi
            setTimeout(() => {
                if (backend && !backend.killed) {
                    backend.kill('SIGKILL'); // questo non funziona in windows
                }
            }, 5000);
        }
    }
}

// Gestisce gli eventi dell'app
app.whenReady().then(async () => {
    try {
        // Avvia il server Vite solo in development
        if (isDev) {
            await startViteServer();
        }

        // Avvia il backend
        startBackend();

        // Aspetta un po' prima di creare la finestra
        setTimeout(() => {
            createWindow();
        }, isDev ? 2000 : 0);

    } catch (error) {
        console.error('Error during app initialization:', error);
        // Crea la finestra comunque
        createWindow();
    }
    // Su macOS, ricrea la finestra quando l'icona nel dock viene cliccata
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// Chiudi l'app quando tutte le finestre sono chiuse
app.on('window-all-closed', async () => {
    // Su macOS, lascia l'app attiva anche senza finestre
    if (process.platform !== 'darwin') {
        console.log('All windows closed, initiating graceful shutdown...');

        try {
            await stopBackendGracefully();
            stopViteServer();
            app.quit();
        } catch (error) {
            console.error('Error during graceful shutdown:', error);
            console.log('Graceful shutdown failed, proceeding with normal shutdown...');
            // Fallback alla chiusura normale
            stopBackend();
            stopViteServer();
            app.quit();
        }

    }
});

// Gestisce la chiusura dell'app
app.on('before-quit', async (event) => {
    if (event){
        // Previeni la chiusura immediata
        event.preventDefault();
    }

    try {
        await stopBackendGracefully();
        stopViteServer();

        // Ora chiudi veramente l'app
        app.exit(0);
    } catch (error) {
        console.error('Error during graceful shutdown:', error);
        // Fallback alla chiusura normale
        stopBackend();
        stopViteServer();
        app.exit(1);
    }

});

// Gestisce gli handler IPC
ipcMain.handle('get-app-version', () => {
    return app.getVersion();
});
// Aggiungi un handler IPC per ottenere il heartbeat PID dal frontend se necessario
ipcMain.handle('get-heartbeat-pid', async () => {
    if (!heartbeatPid) {
        await getHeartbeatPid();
    }
    return heartbeatPid;
});

// Passo le variabili ambientali al preload che non può usare il modulo path
ipcMain.handle('get-env', () => {
    return {
        FLASK_PORT: FLASK_PORT,
        FLASK_HOST: FLASK_HOST,
        VITE_PORT: VITE_PORT,
        VITE_HOST: VITE_HOST
    };
});


ipcMain.on('open-dev-tools', () => {
    if (mainWindow) {
        mainWindow.webContents.openDevTools();
    }
});

// Gestisce i protocolli personalizzati se necessario
app.setAsDefaultProtocolClient('mcp-client');

// Gestisce i messaggi di sicurezza
app.on('web-contents-created', (event, contents) => {
    contents.on('new-window', (event, navigationUrl) => {
        event.preventDefault();
        require('electron').shell.openExternal(navigationUrl);
    });
});

// Gestisce CSP (Content Security Policy)
app.on('web-contents-created', (event, contents) => {
    contents.on('dom-ready', () => {
        contents.insertCSS(`
      * {
        -webkit-user-select: text !important;
        -webkit-user-drag: auto !important;
      }
    `);
    });
});

// Previene la navigazione non autorizzata
app.on('web-contents-created', (event, contents) => {
    contents.on('will-navigate', (event, navigationUrl) => {
        const parsedUrl = new URL(navigationUrl);

        // Permetti solo localhost in development
        if (isDev && parsedUrl.origin === `${VITE_URL}`) {
            return;
        }

        // Blocca tutte le altre navigazioni
        event.preventDefault();
    });
});

// Log delle informazioni di debug
console.log('Electron app starting...');
console.log('isDev:', isDev);
console.log('__dirname:', __dirname);
console.log('process.resourcesPath:', process.resourcesPath);