import Sequelize from 'sequelize';
import { sequelize } from '../database/database';

const tipoDireccion = sequelize.define('tipoDireccione', {
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


export default tipoDireccion;