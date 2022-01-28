import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
//import Consorcio from './Consorcio';
const juego = sequelize.define('juegos', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  descripcion: {
    type: Sequelize.INTEGER,
    allowNull: false,
  }
}, {});
//Banca.hasMany(Consorcio);
//Consorcio.belongsTo(Banca);
//Vendedor.hasMany(Banca);
//Banca.belongsTo(vendedor);
export default juego;