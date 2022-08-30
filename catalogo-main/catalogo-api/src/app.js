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
    title: 'Catalogo digital',
    version: '1.0.0',
    description: 'Sistema para la preventa y facturacion de productos fuera de una tienda'
  }
};


const options = {
  swaggerDefinition,
  // Paths to files containing endpoints definitions
  apis: ['./src/routes/Cliente.js','./src/routes/Contacto.js',
         './src/routes/Banca.js','./src/routes/Direccion.js',
  './src/routes/Permiso',
  './src/routes/Persona.js', './src/routes/Rol.js','./src/routes/Telefono.js',
  './src/routes/Terminal.js',   
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