import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Vendedor from './Vendedor';
import Banca from './Banca';
const Terminal = sequelize.define('terminal', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,  
    autoIncrement: true
  },
   
   
  estado: {
    type: Sequelize.TEXT,
    allowNull: true
  },
  emei: {
    type: Sequelize.TEXT,
    allowNull: false,
    unique:true
  },
  idbanca: {
    type: Sequelize.TEXT,
    allowNull: false
  }
   
  
});
Vendedor.hasOne(Terminal);  
Banca.hasMany(Terminal);  
Terminal.belongsTo(Vendedor);
Terminal.belongsTo(Banca);
export default Terminal; 