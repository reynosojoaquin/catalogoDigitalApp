import Sequelize from 'sequelize';
import { sequelize } from '../database/database';


const inventario = sequelize.define('inventario', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  producto_id:{
      type:Sequelize.INTEGER,
      allowNull:false
    },
  precio:{
    type: Sequelize.DECIMAL,
    allowNull:true
    },
  costo:{
    type:Sequelize.DECIMAL,
    allowNull:true
    },
  flete:{
    type:Sequelize.DECIMAL,
    allowNull:true
    },
  suplidor_id:{
    type:Sequelize.INTEGER,
    allowNull:true
    },
  existencia:{
    type:Sequelize.DECIMAL,
    allowNull:true
    },
    margen:{
       type:Sequelize.DECIMAL,
       allowNull:false
    }

}, {timestamps:false});


export default inventario;