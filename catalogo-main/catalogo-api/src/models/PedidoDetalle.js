import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import producto from '../models/Producto';
import pedido from '../models/Pedido';
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




}, {
  freezeTableName: true,
  timestamps:false
});
pedidoDetalle.belongsTo(producto,{foreignKey:'producto_id'});
pedidoDetalle.belongsTo(pedido,{foreignKey:'pedido_id'});
export default pedidoDetalle;