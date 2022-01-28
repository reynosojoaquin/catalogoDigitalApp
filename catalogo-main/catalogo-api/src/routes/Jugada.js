import {Router} from 'express';
import jugadaController from '../controllers/JugadaController';

const router = Router();
/**
 * @swagger
 * /api/Jugada:
 *   get:
 *     description: Consulta de todas las Jugadas
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todas las Jugadas registradas en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID de la jugada
 *               example: 1
 *             id_global:
 *               type: integer
 *               description: id de global generado mediante un algoritmo 
 *               example: 
 *             estado:
 *               type: string
 *               description: si está activada o desactivada. 1 o 0 
 *               example: 1
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




router.get('/', jugadaController.getAll );
router.get('/:id', jugadaController.getById );
router.put('/:id', jugadaController.update );
router.post('/', jugadaController.create );
router.delete('/:id', jugadaController.delete);

export default router;