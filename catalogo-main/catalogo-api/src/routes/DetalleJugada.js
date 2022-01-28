import {Router} from 'express';
import DetalleJugadaController from '../controllers/DetalleJugadaController';

const router = Router();
/**
 * @swagger
 * /api/DetalleJugada:
 *   get:
 *     description: Consulta de todos los DetalleJugada
 *     responses:
 *       200:
 *         description: el detalle guarda todo tipo de datos de la jugada, datos repetitivos. 
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del detalle de la jugada
 *               example: 1
 *             idjugada:
 *               type: string
 *               description: Id de Jugada maestra de la cual depende este detalle 
 *               example:
 *             monto:
 *               type: string
 *               description: Monto de DetalleJugada o linea de la jugada, es decir de ese detalle
 *               example: 
 *             idjuego:
 *               type: string
 *               description: Id del tipo de juego en el detalle, ej. pale, quiniela, tripleta, etc. 
 *               example: 
 *             idloteria: id de la loteria
 *               type: string
 *               description: Id de Loteria., ej. loteka, nacional, leidsa, etc. 
 *               example: Loteka
 *             num1:
 *               type: string
 *               description: el primer numero de la jugada, 
 *               example: 10
 *             num2:
 *               type: integer
 *               description: segundo numero de la jugada.
 *               example:  
 *             num3:
 *               type: integer
 *               description:  tercer numero de la jugada
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



router.get('/', DetalleJugadaController.getAll );
router.get('/:id', DetalleJugadaController.getById );
router.put('/:id', DetalleJugadaController.update );
router.post('/', DetalleJugadaController.create );
router.delete('/:id', DetalleJugadaController.delete);

export default router;