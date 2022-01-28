import {Router} from 'express';
import RolController from '../controllers/RolController';

const router = Router();
/**
 * @swagger
 * /api/Rol:
 *   get:
 *     description: Consulta de los roles 
 *     responses:
 *       200:
 *         description: un rol es permisos que contiene un perfil de usuario. 
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID del rol.
 *               example: 1
 *             id_usuario:
 *               type: integer
 *               description: id del usuario al que pertenece el rol
 *               example: 1
 *             nombre_rol:
 *               type: string
 *               description: nombre del rol
 *               example: operador
 *             id_permisos:
 *               type: integer
 *               description: id del permiso, correspondiente la tabla permisos
 *               example: 
 *             
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */

router.get('/', RolController.getAll );
router.get('/:id', RolController.getById );
router.put('/:id', RolController.update );
router.post('/', RolController.create );
router.delete('/:id', RolController.delete);

export default router;