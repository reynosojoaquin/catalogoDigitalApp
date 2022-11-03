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
  Costo:{
    type:Sequelize.DECIMAL,
    allowNull:true
    },
  flete:{
    type:Sequelize.DECIMAL,
    allowNull:true
    },
  Suplidor_id:{
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
    },
    suplidor_id:{
      type:Sequelize.INTEGER,
      allowNull:false
    }

}, {timestamps:false});


export default inventario;