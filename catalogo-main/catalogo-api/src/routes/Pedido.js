import {Router} from 'express';
import pedidoController from '../controllers/PedidoController';

const router = Router();
/**
 * @swagger
 * /api/Permiso:
 *   get:
 *     description: Consulta de todos los permisos
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todos los permisos registrados en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del permiso.
 *               example: 1
 *             id_rol:
 *               type: integer
 *               description: id de rol.
 *               example: 1
 *            desc_ruta:
 *               type: string
 *               description: describir ruta.
 *               example: /admini/user
 *             estado:
 *               type: string
 *               description: si está activado o desactivado. 0 y 1 
 *               example: 1
 *             icono:
 *               type: string
 *               description: 
 *               example:  /foto.jpg
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */




router.get('/', pedidoController.getAll );
router.get('/:id', pedidoController.getById );
router.put('/:id', pedidoController.update );
router.post('/', pedidoController.create );
router.delete('/:id', pedidoController.delete);

export default router;