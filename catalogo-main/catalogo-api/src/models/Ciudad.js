import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import provincia from '../models/provincia';

const Ciudade = sequelize.define('Ciudade', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
   Nombre: {
    type: Sequelize.TEXT,
    allowNull: false  }

}, {timestamps:false});

Ciudade.belongsTo(provincia,{foreignKey:'provincia_id'});
export default Ciudade;