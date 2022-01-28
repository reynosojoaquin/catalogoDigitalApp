import express, { json } from 'express';
import morgan from 'morgan';
import dotenv from 'dotenv';
import router from './routes/routes';

//import DataExample from './ControllerInicial';
import cors from 'cors';

// Load env file
dotenv.config();

// Initialization
const app = express();
const swaggerJSDoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');


// Middlewares
app.use(morgan('dev'));
app.use(json());
app.use(cors({
  origin: '*'
}));

// CREANDO LA ESPESIFICACION DE LA API



const swaggerDefinition = {
  info: {
    title: 'Lotery 2.0',
    version: '1.0.0',
    description: 'Sistema para la administracion de consorcios de loteria'
  }
};


const options = {
  swaggerDefinition,
  // Paths to files containing endpoints definitions
  apis: ['./src/routes/Cliente.js','./src/routes/Contacto.js',
         './src/routes/Banca.js','./src/routes/Consorcio.js'
  ,'./src/routes/DestalleJugada.js','./src/routes/Direccion.js'
  ,'./src/routes/InventarioBanca.js' ,'./src/routes/InventarioTerminal.js',
  './src/routes/Jugada.js','./src/routes/Loteria.js','./src/routes/Permiso',
  './src/routes/Persona.js', './src/routes/Rol.js','./src/routes/Telefono.js',
  './src/routes/Terminal.js','./src/routes/TipoJuego.js',    
  './src/routes/Usuario.js','./src/routes/Vendedor.js','./src/models/Cliente.js'      

],
  
    servers: [
     {url: 'http://localhost:'+process.env.PORT+'/api'}
    ],
};


const swaggerSpec = swaggerJSDoc(options);


// Define Routes
app.use('/api', router);
var explorer = {
  explorer: true
};

app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec,explorer));
 


export default app;