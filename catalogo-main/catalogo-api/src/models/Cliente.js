/**
 * @swagger
 *  components:
 *     schemas:
 *      client:
 *        type: object
 *        required:
 *            - nombres
 *            - apellidos
 *            - cedula
 *            - sexo
 *        properties:
 *          id:
 *            type: integer
 *            description: ID del cliente.
 *          nombres:
 *            type: string
 *            description: nombres del cliente.
 *          apellidos:
 *            type: string
 *            description: apellidos del cliente.
 *          cedula:
 *            type: string
 *            description: numero de cedula del cliente.
 *          correo:
 *            type: string
 *            description: correo electronico del cliente.
 *          sexo:
 *            type: string
 *            description: sexo 
 *          Url:
 *            type: string
 *            description: Url Imagen cliente.
 *        example:
 *          id: 1
 *          nombres: Joaquin 
 *          apellidos: Reynoso  
 *          cedula: 000-0000000-0
 *          correo: Leanne@gmail.com
 *          sexo: femenino 
 *          imagen: https://picsum.photos/200/300
 */
/**
*@swagger
*tags: 
*  name: Clients 
*  Description: Model to the clients of the company.
*/
import Sequelize from 'sequelize';
import { sequelize } from '../database/database';
import Persona from './Persona';


const Cliente = sequelize.define('cliente', {
  id: {
    type: Sequelize.INTEGER, 
    primaryKey: true ,
    autoIncrement: true  
  } 
   
}, {timestamps:false});
Persona.hasOne(Cliente,{ onDelete: 'cascade' },{ onUpdate: 'cascade' });
Cliente.belongsTo(Persona,{ onDelete: 'cascade' },{ onUpdate: 'cascade' }); 
 
export default Cliente;