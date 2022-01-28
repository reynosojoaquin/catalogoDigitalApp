import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Persona from './Persona';

const Vendedor = sequelize.define('vendedor', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    foreignKey: true
  },
  estado: {
    type: Sequelize.TEXT, // se ha contemplado 0 y 1 para activo o no 
    allowNull: false
  },
  cedula: {
    type: Sequelize.TEXT,
    allowNull: false
  }
}, {
  freezeTableName: true
});



Persona.hasOne(Vendedor, { onDelete: 'cascade' });
Vendedor.belongsTo(Persona, { onDelete: 'cascade' });
export default Vendedor;