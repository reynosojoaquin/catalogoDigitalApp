import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
//import Consorcio from './Consorcio';
const loteria = sequelize.define('loteria', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  nombre: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  hora_ini: {
    type: Sequelize.DATE,
    allowNull: false,
  },
  hora_fin: {
    type: Sequelize.DATE,
    allowNull: false,
    
  },
  estado: {
    type: Sequelize.BOOLEAN,
    allowNull: false,
   
  },
  
  
}, {});
//Banca.hasMany(Consorcio);
//Consorcio.belongsTo(Banca);
//Vendedor.hasMany(Banca);
//Banca.belongsTo(vendedor);
export default loteria;