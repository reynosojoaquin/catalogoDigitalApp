import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import producto from './Producto';
import modelo from './productoModelo';

const marca = sequelize.define('marca', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {timestamps:false});

marca.hasMany(producto,{foreignKey:'marca_id'});
marca.hasMany(modelo,{foreingnkey:'marca_id'});
export default marca;