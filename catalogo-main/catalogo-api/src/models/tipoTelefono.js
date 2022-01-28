import Sequelize from 'sequelize';
import { sequelize } from '../database/database';

const tipoTelefono = sequelize.define('tipoTelefono', {
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


export default tipoTelefono;