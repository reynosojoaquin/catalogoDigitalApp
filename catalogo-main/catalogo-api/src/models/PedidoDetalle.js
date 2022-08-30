import Sequelize from 'sequelize';
import { sequelize } from '../database/database';

const pedidoDetalle = sequelize.define('PedidoDetalle', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {});

export default pedidoDetalle;