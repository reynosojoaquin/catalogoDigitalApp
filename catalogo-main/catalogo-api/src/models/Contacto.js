import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Persona from './Persona';
import tipoContacto from './tipoContacto';
const Contacto = sequelize.define('contacto', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    unique:true
  },
  persona_id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    
  },
  nombre: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  apellido: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  telefono: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  direccion: {
    type: Sequelize.TEXT,
    allowNull: true,
  }
}, {timestamps:false});

Persona.hasMany(Contacto,{ foreignKey:'persona_id'});
Contacto.belongsTo(Persona);
tipoContacto.hasMany(Contacto,{foreignKey:'tipo_id'});
Contacto.belongsTo(tipoContacto,{foreignKey:'tipo_id'});  


export default Contacto;