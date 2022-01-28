import {Router} from 'express';
import loteria from '../controllers/LoteriaController';

const router = Router();
/**
 * @swagger
 * /api/Loteria:
 *   get:
 *     description: Consulta de todas las Loterias
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todas las Loterias registradas en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID de la loteria.
 *               example: 1
 *             nombre:
 *               type: string
 *               description: nombre de la loteria.
 *               example: loteka
 *             hora_ini:
 *               type: string
 *               description: Hora inicial.
 *               example: 10:00PM
 *             hora_fin:
 *               type: string
 *               description: Hora de conclusión.
 *               example: 11:00PM
 *             Estado:
 *               type: string
 *               description: Si está activada o desactivada. 1 o 0
 *               example: 1       
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */




router.get('/', loteria.getAll );
router.get('/:id', loteria.getById );
router.put('/:id', loteria.update );
router.post('/', loteria.create );
router.delete('/:id', loteria.delete);

export default router;