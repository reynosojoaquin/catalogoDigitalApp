import Sequelize from 'sequelize';
import { sequelize } from '../database/database';


const Ciudad = sequelize.define('Tipo', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {timestamps:false});

export default Ciudad;