import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import inventario from './Inventario';

const suplidor = sequelize.define('suplidore', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   nombre: {
     type: Sequelize.TEXT,
     allowNull: false
    },
    telefono: {
      type:Sequelize.TEXT,
      allowNull:true
    },
    ubicacion: {
      type:Sequelize.TEXT,
      allowNull:true
    },
    contacto:{
      type:Sequelize.TEXT,
      allowNull:true},
    documento:{
      type:Sequelize.TEXT,
      allowNull:true
    },
    tipo_documento:{
      type:Sequelize.TEXT
    }
}, {
  timestamps:false
});

suplidor.hasMany(inventario,{foreignKey:'suplidor_id'});

export default suplidor;