const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 5000;

// Configura CORS para permitir solicitudes del frontend
app.use(cors());
app.use(bodyParser.json()); // Añade el middleware para parsear JSON

// Ruta de prueba
app.get('/test', (req, res) => {
    res.send('Backend is working!');
});

// Endpoint para ejecutar los scripts
app.post('/run/:script', (req, res) => {
    const { script } = req.params;
    const params = req.body; // Obtén los parámetros del cuerpo de la solicitud
    let command = `python src/${script}`;

    // Añadir parámetros al comando si están presentes
    if (params.name) {
        command += ` ${params.name}`; // Añadir el nombre como argumento
    }

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send('Error executing script');
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send('Error executing script');
        }
        console.log(`stdout: ${stdout}`);
        res.send('Script executed successfully');
    });
});

// Servir la aplicación React
app.use(express.static(path.join(__dirname, 'client/build')));

// Iniciar el servidor Flask para transmitir el video
const startFlaskServer = () => {
    exec('python src/stream_video.py', (error) => {
        if (error) {
            console.error(`Error: ${error.message}`);
        }
    });
};
startFlaskServer();

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
