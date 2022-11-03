import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import producto from '../models/Producto';

const ProductoTipo = sequelize.define('ProductoTipo', {
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

ProductoTipo.hasMany(producto,{foreignKey:'tipo_id'}); 

export default ProductoTipo;