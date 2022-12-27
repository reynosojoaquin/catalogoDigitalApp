import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import pedido from './Pedido';

const status = sequelize.define('statu', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   descripcion: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {timestamps:false});

pedido.belongsTo(status,{foreignKey:'status_id'});
export default status;