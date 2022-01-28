import {Router} from 'express';
import TipoJuegoController from '../controllers/TipoJuegoController';

const router = Router();
/**
 * @swagger
 * /api/TipoJuego:
 *   get:
 *     description: Consulta de todos los tipo de juegos
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todos los tipos de juegos registrados en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del telefono o registro actual 
 *               example: 1
 *             descripcion:
 *               type: string
 *               description:  tipo de juego, pale, quiniela. etc. 
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
router.get('/', TipoJuegoController.getAll );
router.get('/:id', TipoJuegoController.getById );
router.put('/:id', TipoJuegoController.update );
router.post('/', TipoJuegoController.create );
router.delete('/:id', TipoJuegoController.delete);

export default router;