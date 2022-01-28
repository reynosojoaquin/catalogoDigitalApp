import {Router} from 'express';
import inventarioterminal from '../controllers/InventarioTerminalController';

const router = Router();
/**
 * @swagger
 * /api/InventarioTerminal:
 *   get:
 *     description: Consulta del InventarioTerminal
 *     responses:
 *       200:
 *         description: Retorna un objeto json con el InventarioTerminal registrado en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del inventario de esa terminal.
 *               example: 1
 *             id_terminal:
 *               type: integer
 *               description: id del terminal.
 *               example: 1
 *             id_juegoTipo:
 *               type: integer
 *               description: id de JuegoTipo
 *               example: 1
 *             nombre_juego:
 *               type: string
 *               description: nombre de juego.
 *               example: 1
 *             limite_monto:
 *               type: double
 *               description: limite del monto.
 *               example: 
 *             fech_ult_act:
 *               type: date
 *               description: fecha de la ultima actualización.
 *               example: 11/5/2021
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */





router.get('/', inventarioterminal.getAll );
router.get('/:id', inventarioterminal.getById );
router.put('/:id', inventarioterminal.update );
router.post('/', inventarioterminal.create );
router.delete('/:id', inventarioterminal.delete);

export default router;