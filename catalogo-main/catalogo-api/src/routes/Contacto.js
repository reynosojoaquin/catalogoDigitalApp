import {Router} from 'express';
import contactoController from '../controllers/ContactoController';

const router = Router();
/**
 * @swagger
 * /api/Contacto:
 *   get:
 *     description: Consulta de todos los contactos, un contacto es una persona de referencia de una persona. 
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todos los contactos registrados en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del contacto
 *               example: 1
 *             nombre:
 *               type: string
 *               description: nombres 
 *               example: Leanne valery
 *             apellido:
 *               type: string
 *               description: apellidos 
 *               example: smit
 *             telefono:
 *               type: string
 *               description: telfono
 *               example: 8095557777
 *             tipo:
 *               type: string
 *               description: celular o fijo
 *               example: 1 
 *             direccion:
 *               type: string
 *               description: direccion del contacto 
 *               example: calle m numero 4
 *             personaId:
 *               type: integer
 *               description:  
 *               example:  1
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */


 

router.get('/', contactoController.getAll );
router.get('/:id', contactoController.getById );
router.put('/:id', contactoController.update );
router.post('/', contactoController.create );
router.delete('/:id', contactoController.delete);

export default router;