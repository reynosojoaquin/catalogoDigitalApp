import Sequelize from 'sequelize';
import { sequelize } from '../database/database';


const Producto = sequelize.define('Producto', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   nombre: {
    type: Sequelize.TEXT,
    allowNull: false  },
    codigoInterno:{
      type: Sequelize.DECIMAL
    },
    codigoBarras:{
      type:Sequelize.TEXT,
      allowNull:true
    },
    activo:{
      type:Sequelize.BOOLEAN,     
      allowNull:true
    },
    descripcion:{
      type:Sequelize.STRING,
      allowNull:true
    },
    exento:{
      type:Sequelize.BOOLEAN,
      allowNull:true
    },
    imgUrl:{
      type:Sequelize.STRING,
      allowNull:true
    },
    reorden:{
      type:Sequelize.INTEGER,
      allowNull:true
    },
    marca_id:{
      type:Sequelize.INTEGER,
      allowNull:false
    },
    modelo_id:{
      type:Sequelize.INTEGER,
      allowNull:false
    },
    tipo_id:{
      type:Sequelize.INTEGER,
      allowNull:false
    },
    unidad_id:{
      type:Sequelize.INTEGER,
      allowNull:false
    }
}, {
  timestamps:false
});

export default Producto;