import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
//import Consorcio from './Consorcio';
const inventarioterminal = sequelize.define('inventarioterminale', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  id_terminal: {
    type: Sequelize.INTEGER,
    allowNull: false,
  },
  id_juegoTipo: {
    type: Sequelize.INTEGER,
    allowNull: false,
  },
  nombre_juego: {
    type: Sequelize.TEXT,
    allowNull: false,
    
  },
  limite_monto: {
    type: Sequelize.DOUBLE,
    allowNull: false,
   
  },
  fech_ult_act: {
    type: Sequelize.DATE,
    allowNull: false,
   
  },
  
  
}, {});
//Banca.hasMany(Consorcio);
//Consorcio.belongsTo(Banca);
//Vendedor.hasMany(Banca);
//Banca.belongsTo(vendedor);
export default inventarioterminal;