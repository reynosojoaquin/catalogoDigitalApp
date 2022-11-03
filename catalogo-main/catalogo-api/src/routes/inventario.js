import { Router } from 'express';
import inventarioController from '../controllers/InventarioController';

const router = Router();
/**
* @swagger
* /api/Banca:
*   get:
*     description: Consulta de todos las bancas
*     responses:
*       200:
*         description: Retorna un objeto json con todos los bancas registrados en el sistema. para registrar una banca debe existir primero un ciente  y un consorcio
*         schema:
*           type: object
*           properties:
*             id:
*               type: integer
*               description: ID del usuario.
*               example: 1
*             nombre_banca:
*               type: string
*               description: nombres de la banca.
*               example: Leanne valery
*             direccion:
*               type: string
*               description: direccion de la banca
*               example: smit
*             emailbanca:
*               type: string
*               description: correo electronico de la banca
*               example: correobanca@gmail.com
*             estadobanca:
*               type: string
*               description: activa o no activa, es el estado, 1 y 0 , activo y no activo
*               example: 1  
*             franquiciano:
*               type: string
*               description: numero de franquicia de la banca
*               example: Femenino
*             idconsorcio:
*               type: integer
*               description:  id del consorcio , es requerido para crear una banca. 
*               example:  
*       400:
*         description: Invalid request 
*         schema:
*           type: object
*           properties:   
*             error:
*              type: string
*       
*/


/**
 * @swagger
 * /api/banca:
 *  post:
 *   summary: create team
 *   description: create team
 *   parameters:
 *    - in: body
 *      name: body
 *      required: true
 *      description: body banca 
 *      schema:
 *      nombre_banca :  
 *        type : string   
 *      direccion : 
 *        type :  string    
 *      emailbanca : 
 *        type :  string 
 *      estadobanca : 
 *        type :  string
 *      franquiciano : 
 *        type :  string
 *      idconsorcio :  
 *        type :  integer 
 *   requestBody:
 *    content:
 *     application/json:
 *      schema:       
 *   responses:
 *    200:
 *     description: success
 *    500:
 *     description : error 
 */


router.get('/', inventarioController.getAll);
router.get('/:id', inventarioController.getById);
router.put('/:id', inventarioController.update);
router.post('/', inventarioController.create);
router.delete('/:id', inventarioController.delete);

export default router;