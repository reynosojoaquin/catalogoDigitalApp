import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import tipoDireccion from './tipoDireccion';
import ciudad from './Ciudad';
import sector from './Sector';
import provincia from  './provincia';
import Persona from './Persona';


const Direccion = sequelize.define('direccione', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    unique:true
  },
  calle: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  numero: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  apartamento: {
    type: Sequelize.TEXT,
    allowNull: true,
    unique:false
  },
  longitud: {
    type: Sequelize.TEXT,
    allowNull: true,
    unique:false
    
  },
  latitude: {
    type: Sequelize.TEXT,
    allowNull: true,
    unique:false
    
  },
  persona_id: {
    type: Sequelize.INTEGER,
    allowNull: true,
    primaryKey:true
  },


}, {});
Persona.hasMany(Direccion,{foreignKey:'persona_id'});
Direccion.belongsTo(Persona);
tipoDireccion.hasMany(Direccion,{foreignKey:'tipo_id'});
Direccion.belongsTo(tipoDireccion,{foreignKey:'tipo_id'}); 
Direccion.belongsTo(provincia,{foreignKey:'provincia_id'});
Direccion.belongsTo(ciudad,{foreignKey:'ciudad_id'});
Direccion.belongsTo(sector,{foreignKey:'sector_id'});





export default Direccion;