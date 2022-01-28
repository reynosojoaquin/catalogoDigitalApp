import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
//import Consorcio from './Consorcio';
const Permiso = sequelize.define('permisos', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  id_rol: {
    type: Sequelize.INTEGER,
    allowNull: false,
  },
  desc_ruta: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  estado: {
    type: Sequelize.TEXT,
    allowNull: false,
    
  },
  icono: {
    type: Sequelize.TEXT,
    allowNull: false,
   
  }
 

  
}, {});

export default Permiso;