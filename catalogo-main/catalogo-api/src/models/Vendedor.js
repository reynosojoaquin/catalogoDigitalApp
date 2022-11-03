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
   persona_id: {
    type: Sequelize.INTEGER,
    allowNull: true,
    primaryKey:true    
  }
  
}, {
  freezeTableName: true
});



Persona.hasOne(Vendedor, { onDelete: 'cascade' });
Vendedor.belongsTo(Persona, { onDelete: 'cascade' });
export default Vendedor;