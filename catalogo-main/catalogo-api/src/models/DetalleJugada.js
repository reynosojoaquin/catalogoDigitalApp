import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
 //import Jugada from './jugada';
const Detalle = sequelize.define('detalles', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  idjugada: {
    type: Sequelize.INTEGER,
    allowNull: false,
  },
  monto: {
    type: Sequelize.DOUBLE,
    allowNull: false,
  },
  idjuego: {
    type: Sequelize.INTEGER,
    allowNull: false,
  },
  idloteria: {
    type: Sequelize.INTEGER,
    allowNull: false,   
  },
   
  num1:{
    type: Sequelize.INTEGER,
    allowNull:false,
  },
  num2:{
    type: Sequelize.INTEGER,
    allowNull:false,
  },
  num3:{
    type: Sequelize.INTEGER,
    allowNull:false,
  },

}, {});
 
//Jugada.hasMany(Detalle);
//Detalle.belongsTo(Jugada);
export default Detalle;