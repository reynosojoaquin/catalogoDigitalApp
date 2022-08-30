import Sequelize from 'sequelize';
import { sequelize } from '../database/database';


const Pedido = sequelize.define('pedido', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {});

export default Pedido;