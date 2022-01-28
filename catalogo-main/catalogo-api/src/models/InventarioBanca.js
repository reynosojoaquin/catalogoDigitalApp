import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
//import Consorcio from './Consorcio';
const bancainventario = sequelize.define('bancasinventario', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  numero: {
    type: Sequelize.INTEGER,
    allowNull: false,
  },
  id_banca: {
    type: Sequelize.INTEGER,
    allowNull: false,
  },
  id_juego: {
    type: Sequelize.INTEGER,
    allowNull: false,
    
  },
  limite: {
    type: Sequelize.DOUBLE,
    allowNull: false,
   
  },

  
}, {});
//Banca.hasMany(Consorcio);
//Consorcio.belongsTo(Banca);
//Vendedor.hasMany(Banca);
//Banca.belongsTo(vendedor);
export default bancainventario;