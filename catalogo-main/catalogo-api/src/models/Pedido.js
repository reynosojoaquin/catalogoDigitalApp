import Sequelize from 'sequelize';
import { sequelize } from '../database/database';


const Pedido = sequelize.define('pedido', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   fecha: {
    type: Sequelize.DATE,
    allowNull: false  },
   status:{
    type:Sequelize.TEXT,
    allowNull:false
   },
   total:{
    type:Sequelize.DECIMAL,
    allowNull:true
   },
   clienteID:{
      type:  Sequelize.INTEGER,
      allowNull:false
   },
   vendedorID:{
    type:Sequelize.INTEGER,
    allowNull:false
   },
   activo:{
    type:Sequelize.BOOLEAN
   }

}, {});

export default Pedido;