import {Router} from 'express';
import usuarioController from '../controllers/UsuarioController';

const router = Router();
/**
 * @swagger
 * /api/Usuario:
 *   get:
 *     description: Consulta de todas los usuarios
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todas los usuarios registrados en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del telefono o registro actual 
 *               example: 1
 *             nombre_usr:
 *               type: string
 *               description:  nombre del usuario,  
 *               example: rtaveras
 *             pwd:
 *               type: string
 *               description:  contrasena incriptada 
 *               example: "@#$%^&*(23434)(*&^%4545$%^&*()(*&^%$se))"
 *             id_rol:
 *               type: integer
 *               description:  rol del usuario actual
 *               example: 1
 *             id_persona:
 *               type: integer
 *               description: id de la persona. 
 *               example: 1
 *             nombre:
 *               type: string
 *               description:  nombre del usuario
 *               example: 1
 *             cedula:
 *               type: string
 *               description: cedula del usuario 
 *               example: 056-03238778-9 
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */
router.get('/', usuarioController.getAll );
router.get('/:id', usuarioController.getById );
router.put('/:id', usuarioController.update );
router.post('/', usuarioController.create );
router.delete('/:id', usuarioController.delete);

export default router;