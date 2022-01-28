import {Router} from 'express';
import inventarioBanca from '../controllers/InventarioBancaController';

const router = Router();
/**
 * @swagger
 * /api/InventarioBanca:
 *   get:
 *     description: Consulta del InventarioBanca
 *     responses:
 *       200:
 *         description: Retorna un objeto json con el InventarioBanca registrado en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del inventario
 *               example: 1
 *             numero:
 *               type: string
 *               description: todos los numeros tendran una entrada aqui, desde 0 al 99
 *               example: 3
 *             id_banca:
 *               type: integer
 *               description: id de banca asociada a dicho inventario 
 *               example: 21
 *             id_juego:
 *               type: integer
 *               description: id de juego al que se estara limitando con dicho inventario. 
 *               example:
 *             limite:
 *               type: integer
 *               description: limite de InventarioBanca.
 *               example: 100         
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */


router.get('/', inventarioBanca.getAll );
router.get('/:id', inventarioBanca.getById );
router.put('/:id', inventarioBanca.update );
router.post('/', inventarioBanca.create );
router.delete('/:id', inventarioBanca.delete);

export default router;