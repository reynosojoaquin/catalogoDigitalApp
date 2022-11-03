import Sequelize from 'sequelize';
import { sequelize } from '../database/database';

const pedidoDetalle = sequelize.define('PedidoDetalle', {
  indice: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   producto_id: {
    type: Sequelize.INTEGER,
    allowNull: false  },
    pedido_id: {
      type: Sequelize.INTEGER,
      allowNull: false  },
    cantidad:{
      type: Sequelize.DECIMAL,
      allowNull: false
    },
    total:{
      type: Sequelize.DECIMAL,
      allowNull:false
    }




}, {});

export default pedidoDetalle;