import {Router} from 'express';
import vendedorController from '../controllers/VendedorController';

const router = Router();
/**
 * @swagger
 * /api/Vendedor:
 *   get:
 *     description: Consulta de todos los vendedores 
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todos los vendedores registrados en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del telefono o registro actual 
 *               example: 1
 *             estado:
 *               type: string
 *               description:  estado  1 o 0 activo  o no 
 *               example: 1
 *             cedula:
 *               type: string
 *               description: cedula del vendedor
 *               example: 056-09098801-0         
 *            
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */
router.get('/', vendedorController.getAll );
router.get('/:id', vendedorController.getById );
router.put('/:id', vendedorController.update );
router.post('/', vendedorController.create );
router.delete('/:id', vendedorController.delete);

export default router;