import {Router} from 'express';
import direccionController from '../controllers/DireccionController';

const router = Router();
/**
 * @swagger
 * /api/Direccion:
 *   get:
 *     description: Consulta de todas las direcciones asociadas a una persona. 
 *     responses:
 *       200:
 *         description: Retorna un objeto json con todas las direcciones registradas en el sistema.
 *         schema:
 *           type: object
 *           properties:
 *             id:
 *               type: integer
 *               description: ID de la direccion 
 *               example: 1
 *             ciudad:
 *               type: string
 *               description: Ciudad.
 *               example: SAN FRANCISCO DE MACORIS
 *             provincia:
 *               type: string
 *               description: Provincia.
 *               example: DUARTE
 *             sector:
 *               type: string
 *               description: Sector.
 *               example: CENTRO DE LA CIUDAD
 *             municipio:
 *               type: string
 *               description: Municipio.
 *               example: SAN FRANCISCO DE MACORIS
 *             apartamento:
 *               type: string
 *               description: Apartamento.
 *               example: 302-A.
 *             longitud:
 *               type: integer
 *               description: Longitud.
 *               example:  100 metros
 *             latitude:
 *               type: integer
 *               description: Latitud.
 *               example: -12034
 *             PersonaId:
 *               type: integer
 *               description: Id de la persona.
 *               example:  1
 *       400:
 *         description: Invalid request 
 *         schema:
 *           type: object
 *           properties:   
 *             error:
 *              type: string
 *       
 */




router.get('/', direccionController.getAll );
router.get('/:id', direccionController.getById );
router.put('/:id', direccionController.update );
router.post('/', direccionController.create );
router.delete('/:id', direccionController.delete);

export default router;