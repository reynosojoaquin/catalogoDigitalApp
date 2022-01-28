import {Router} from 'express';
import terminalController from '../controllers/TerminalController';

const router = Router();
/**
 * @swagger
 * /api/Terminal:
 *   get:
 *     description: Consulta de todas las terminales
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todas las terminales registradas en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del telefono o registro actual 
 *               example: 1
 *             estado:
 *               type: string
 *               description:  estado 1 o 0  estado activo , desactivado
 *               example: 1
 *             emei:
 *               type: string
 *               description: emei del equipo 
 *               example: SANCHEZ PEÑA
 *             idbanca:
 *               type: integer
 *               description:  id de la banca 
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

router.get('/', terminalController.getAll );
router.get('/:id', terminalController.getById );
router.put('/:id', terminalController.update );
router.post('/', terminalController.create );
router.delete('/:id', terminalController.delete);

export default router;