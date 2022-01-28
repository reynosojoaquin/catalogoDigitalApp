import Sequelize from 'sequelize';
import { sequelize } from '../database/database';

const tipoContacto = sequelize.define('tipoContacto', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  Descripcion: {
    type: Sequelize.TEXT,
    allowNull: false,
  }
 
});


export default tipoContacto;