import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Consorcio from './Consorcio';
const Banca = sequelize.define('bancas', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  nombre_banca: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  direccion: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  emailbanca: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  estadobanca: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  franquiciano: {
    type: Sequelize.TEXT,
    allowNull: false,
    unique: true
  },
  idconsorcio: {
    type: Sequelize.INTEGER,
    allowNull: false,
    unique: false

  }
}, {
  freezeTableName: true
});
Consorcio.hasMany(Banca, { foreignKey: 'idconsorcio' }, { onDelete: 'cascade' });
Banca.belongsTo(Consorcio, {
  as: 'myconsorcio',
  foreignKey: 'idconsorcio',
  constraints: true
}, { onDelete: 'cascade' });


export default Banca;