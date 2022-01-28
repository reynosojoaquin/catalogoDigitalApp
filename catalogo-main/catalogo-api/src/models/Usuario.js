import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Persona from './Persona';
const Usuario = sequelize.define('usuario', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  nombre_usr: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  pwd: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  id_rol: {
    type: Sequelize.INTEGER,
    allowNull: false,

  },
  id_persona: {
    type: Sequelize.INTEGER,
    allowNull: false,

  },
  nombre: {
    type: Sequelize.TEXT,
    allowNull: false,

  },
  cedula: {
    type: Sequelize.TEXT,
    allowNull: false,
    onDelete: 'CASCADE',
    reference: {
      model: 'Persona',
      key: 'cedula'
    }
  }

}, {});
Persona.hasOne(Usuario, { foreignKey: 'cedula', sourceKey: 'cedula', constraints: true, onDelete: 'cascade', hooks: true });

Usuario.belongsTo(Persona, { as: 'personaCedula', foreignKey: 'cedula' });

export default Usuario;