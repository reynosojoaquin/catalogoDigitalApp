import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import provincia from '../models/provincia';

const Ciudad = sequelize.define('Ciudad', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {});

Ciudad.belongsTo(provincia,{foreignKey:'provincia_id'});
export default Ciudad;