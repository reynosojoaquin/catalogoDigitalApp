import Sequelize from 'sequelize';
import { sequelize } from '../database/database';


const Modelo = sequelize.define('Modelo', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {});


export default Modelo;