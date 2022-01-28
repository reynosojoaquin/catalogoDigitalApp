import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Terminal from './Terminal';
const Jugada = sequelize.define('jugada', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  idglobal: {
    type: Sequelize.TEXT,
    allowNull: false,
    unique:true
  },   
  estado: {
    type: Sequelize.BOOLEAN,
    allowNull: false,   
  }
  
}, {});
Terminal.hasMany(Jugada);  
Jugada.belongsTo(Terminal);
 
export default Jugada;