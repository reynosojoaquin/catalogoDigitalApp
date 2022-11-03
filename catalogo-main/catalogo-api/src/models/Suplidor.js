import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import inventario from './Inventario';

const suplidor = sequelize.define('suplidor', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  },
    Telefono:{type:Sequelize.TEXT,
    allowNull:true},
    ubicacion:{type:Sequelize.TEXT,
    contacto:{type:Sequelize.TEXT},
    allowNull:true
    }

}, {
  timestamps:false
});

suplidor.hasMany(inventario,{foreignKey:'suplidor_id'});

export default suplidor;