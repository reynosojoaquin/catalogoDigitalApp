import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import producto from './Producto';

const UnidadMedida = sequelize.define('UnidadMedida', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }
}, {
  timestamps:false
});

UnidadMedida.hasMany(producto,{foreignKey:'unidad_id'});

export default UnidadMedida;