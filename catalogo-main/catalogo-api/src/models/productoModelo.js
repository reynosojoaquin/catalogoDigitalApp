import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import producto from './Producto';

const Modelo = sequelize.define('modelo', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {timestamps:false});

Modelo.hasMany(producto,{foreignKey:'modelo_id'});
export default Modelo;