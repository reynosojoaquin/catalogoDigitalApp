import {Router} from 'express';
import consorcioController from '../controllers/ConsorcioController';

const router = Router();
/**
 * @swagger
 * /api/Consorcio:
 *   get:
 *     description: Consulta del Consorcio
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todos los Consorcios registrados en el sistema. se recuerda que un consorcio pertenece a un cliente, por tanto debe existir un cliente antes de crearlo. 
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del usuario.
 *               example: 1
 *             nom_consorcio:
 *               type: string
 *               description: Nombre del consorcio.
 *               example: Consorcio Enmanuel
 *             direccion_fisica:
 *               type: string
 *               description: Direccion fisica de consorcio.
 *               example: Los Rieles, SFM
 *             emailconsorcio:
 *               type: string
 *               description: Email del consorcio
 *               example: consorcio@gmail.com
 *             estadoconsorcio:
 *               type: string
 *               description: si el consorcio está activado o desactivado.
 *               example: activo
 *             clienteid:
 *               type: integer
 *               description: Id de cliente.
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



router.get('/', consorcioController.getAll );
router.get('/:id', consorcioController.getById );
router.put('/:id', consorcioController.update );
router.post('/', consorcioController.create );
router.delete('/:id', consorcioController.delete);

export default router;