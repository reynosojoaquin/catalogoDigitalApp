import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Cliente from '../models/Cliente';
import Vendedor  from './Vendedor';


const Pedido = sequelize.define('pedido', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   fecha: {
    type: Sequelize.DATE,
    allowNull: false  },
   status_id:{
    type:Sequelize.INTEGER,
    allowNull:false
   },
   total:{
    type:Sequelize.DECIMAL,
    allowNull:true
   },
   cliente_id:{
      type:  Sequelize.INTEGER, 
      allowNull:false
   },
   vendedor_id:{
    type:Sequelize.INTEGER,
    allowNull:false
   },
   activo:{
    type:Sequelize.BOOLEAN
   }

}, {});
Pedido.belongsTo(Cliente,{foreignKey:'cliente_id'});
Pedido.belongsTo(Vendedor,{foreignKey:'vendedor_id'});
export default Pedido;