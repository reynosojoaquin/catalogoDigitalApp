import Sequelize from 'sequelize';
import { sequelize } from '../database/database';


const Ciudad = sequelize.define('Producto', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {});


export default Ciudad;