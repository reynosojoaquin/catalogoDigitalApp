import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
 

const Persona = sequelize.define('persona', {
  id: {
    type: Sequelize.INTEGER,
   primaryKey: true,
    autoIncrement: true,

  },
  nombres: {
    type: Sequelize.TEXT,
    allowNull: false
  },

  apellidos: {
    type: Sequelize.TEXT,
    allowNull: false
  },

  cedula: {
    type: Sequelize.TEXT,
   unique:true,
    allowNull: false
     
  },
  estado: {
    type: Sequelize.TEXT,
    allowNull: true
  },
  correo: {
    type: Sequelize.TEXT,
    allowNull: true
  },

  sexo: {
    type: Sequelize.TEXT,
    allowNull: true
  }, 
  url: {
    type: Sequelize.TEXT,
    allowNull: true
  }

}, {
  freezeTableName: true
});


export default Persona;