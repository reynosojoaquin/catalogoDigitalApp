import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Cliente from './Cliente';

const Consorcio = sequelize.define('consorcio', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  nom_consorcio: {
    type: Sequelize.TEXT,
    allowNull: false
  },

  direccion_fisica: {
    type: Sequelize.TEXT,
    allowNull: false
  },
  emailconsorcio: {
    type: Sequelize.TEXT,
    allowNull: false
  },
  estadoconsorcio: {
    type: Sequelize.TEXT,
    allowNull: false
  },
  clienteId : {
    type: Sequelize.INTEGER,
    allowNull: false,
    unique:true
  }
}, {}); 
  
Cliente.hasMany(Consorcio ) ; 
Consorcio.belongsTo(Cliente );
export default Consorcio;