import {Router} from 'express';
import telfonoController from '../controllers/TelefonoController';

const router = Router();
/**
 * @swagger
 * /api/Telefono:
 *   get:
 *     description: Consulta de todos los telefonos
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todos los telefonos registrados en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del telefono o registro actual 
 *               example: 1
 *             numero:
 *               type: string
 *               description: Nombres de la Persona.
 *               example: Enmanuel Gabriel
 *             tipo:
 *               type: string
 *               description: Apellidos de la persona.
 *               example: SANCHEZ PEÑA
 *             personaId:
 *               type: integer
 *               description: es el codigo id a quien pertenece dicho telefono. 
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




router.get('/', telfonoController.getAll );
router.get('/:id', telfonoController.getById );
router.put('/:id', telfonoController.update );
router.post('/', telfonoController.create );
router.delete('/:id', telfonoController.delete);

export default router;