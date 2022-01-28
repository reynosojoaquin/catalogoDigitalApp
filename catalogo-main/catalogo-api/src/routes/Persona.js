import {Router} from 'express';
import personasController from '../controllers/PersonasController';

const router = Router();
/**
 * @swagger
 * /api/Persona:
 *   get:
 *     description: Consulta de todas las personas
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todas las personas registradas en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID de la persona.
 *               example: 1
 *             nombres:
 *               type: string
 *               description: Nombres de la Persona.
 *               example: Enmanuel Gabriel
 *             Apellidos:
 *               type: string
 *               description: Apellidos de la persona.
 *               example: SANCHEZ PEÑA
 *             Cedula:
 *               type: string
 *               description: cedula de la persona.
 *               example: 000-0000000-0
 *             Estado:
 *               type: string
 *               description: Si la persona está activada o desactivada. 0 y 1 , 1 activo
 *               example: 1
 *             Correo:
 *               type: string
 *               description: Correo electronico de la persona.
 *               example: enmanuelsp23@gmail.com
 *             Sexo:
 *               type: integer
 *               description: Sexo de la persona
 *               example:  M
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */





router.get('/', personasController.getAll );
router.get('/:id', personasController.getById );
router.put('/:id', personasController.update );
router.post('/', personasController.create );
router.delete('/:id', personasController.delete);

export default router;