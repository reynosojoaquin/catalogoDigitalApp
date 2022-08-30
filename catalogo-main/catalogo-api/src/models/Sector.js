import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Ciudad from './Ciudad';
const sector = sequelize.define('sector', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {timestamps:false});

sector.belongsTo(Ciudad,{foreignKey:'ciudad_id'});
export default sector;