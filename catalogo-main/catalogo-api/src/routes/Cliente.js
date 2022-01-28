import {Router} from 'express';
import clienteController from '../controllers/ClienteController';
const router = Router();

 /**
 * @swagger
 * /api/cliente:
 *   get:
 *     description: Consulta de todos los clientes
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todos los clientes registrados en el sistema. un cliente es una persona que servira para 
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del cliente.
 *               example: 1
 *             nombres:
 *               type: string
 *               description: nombres del cliente.
 *               example: Leanne valery
 *             apellidos:
 *               type: string
 *               description: apellidos del cliente.
 *               example: smit
 *             cedula:
 *               type: string
 *               description: numero de cedula del cliente.
 *               example: 000-0000000-0
 *             correo:
 *               type: string
 *               description: correo electronico del cliente.
 *               example: Leanne@gmail.com
 *             sexo:
 *               type: string
 *               description: sexo 
 *               example: Femenino
 *             Url:
 *               type: string
 *               description: Url Imagen cliente.
 *               example: https://picsum.photos/200/300
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */
 
router.get('/', clienteController.getAll );
router.get('/:id', clienteController.getById );
router.put('/', clienteController.update );
/**
* @swagger
*  path:
*  /api/cliente:
*  post:
*   summary: create Clients
*   description: create clients for the company
*   parameters:
*     - in: formData
*       name: nombres
*       type: String
*       description: nombres del cliente
*       required: true
*     - in: formData
*       name: apellidos
*       type: String
*       description: apellido del cliente
*       required: true
*     - in: formData
*       name: cedula
*       type: String
*       description: Cedula del cliente
*       required: true
*     - in: formData
*       name:  correo
*       type: String 
*       description: correo electronico del cliente
*       required: true
*     - in: formData
*       name: sexo
*       type: String
*       description: sexo del cliente
*       required: true
*     - in: formData
*       name: Url
*       type: String
*       description: url imagen del cliente
*       required: true
*   tags: [Clients]
*   responses:
*       200:
*         description: resgistra una nueva entidad cliente
*         schema:
*           type: object
*           properties:
*             id:
*               type: integer
*               description: ID del cliente.
*               example: 1
*             nombres:
*               type: string
*               description: nombres del cliente.
*               example: Leanne valery
*             apellidos:
*               type: string
*               description: apellidos del cliente.
*               example: smit
*             cedula:
*               type: string
*               description: numero de cedula del cliente.
*               example: 000-0000000-0
*             correo:
*               type: string
*               description: correo electronico del cliente.
*               example: Leanne@gmail.com
*             sexo:
*               type: string
*               description: sexo 
*               example: Femenino
*             Url:
*               type: string
*               description: Url Imagen cliente.
*               example: https://picsum.photos/200/300
*/
router.post('/', clienteController.create );
router.delete('/:id', clienteController.delete);

 

export default router;