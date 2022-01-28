import Sequelize from 'sequelize';
import { sequelize } from '../database/database';

const Rol = sequelize.define('roles', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  id_usuario: {
    type: Sequelize.INTEGER,
    allowNull: false,
  },
  nombre_rol: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  id_permisos: {
    type: Sequelize.INTEGER,
    allowNull: false,
    
  }
 
  
}, {});
//Banca.hasMany(Consorcio);
//Consorcio.belongsTo(Banca);
//Vendedor.hasMany(Banca);
//Banca.belongsTo(vendedor);
export default Rol;