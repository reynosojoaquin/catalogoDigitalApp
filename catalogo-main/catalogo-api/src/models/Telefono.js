import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Persona from './Persona';
import tipoTelefono from './tipoTelefono';
const Telefono = sequelize.define('telefono', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    unique:true
  },
  numero: {
    type: Sequelize.TEXT,
    allowNull: false,
  },   
  persona_id: {
    type: Sequelize.INTEGER,
    allowNull: true,
    primaryKey:true
    
  },


}, {});
Persona.hasMany(Telefono,{foreingKey:'persona_id'});
Telefono.belongsTo(Persona); 
tipoTelefono.hasMany(Telefono,{foreignKey:'tipo_id'});
Telefono.belongsTo(tipoTelefono,{foreignKey:'tipo_id'}); 


export default Telefono;