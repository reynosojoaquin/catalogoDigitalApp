import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
const provincia = sequelize.define('provincia', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false},
},
 {timestamps:false});


export default provincia;