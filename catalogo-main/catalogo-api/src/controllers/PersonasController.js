import PersonaService from '../services/PersonaService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class PersonaController {

  /**
 * @swagger
 * /cliente:
 *   get:
 *     summary: Retrieve a list of JSONPlaceholder users
 *     description: Retrieve a list of users from JSONPlaceholder. Can be used to populate a list of fake users when prototyping or testing an API.
*/
  static async create(req, res) {
    const newPersona= req.body;
    try {
      const entityCreated = await PersonaService.create(newPersona);
      return res.json(Response.get('Persona created', entityCreated));
    } catch (error) {
       
      res.status(500).json({
        message: 'Something goes wrong'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await PersonaService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Cliente list', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const persona = await PersonaService.getById(req.params.id);

      if (persona) {
        return res.json(Response.get('Persona found', persona));
      }
      return res.json(Response.get('Persona   not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const persona = req.body;

    try {
      const updatePersona = await PersonaService.update(id, persona);

      return res.json(Response.get('Persona Updated', updatePersona));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await PersonaService.delete(req.params.id);
      return res.json(Response.get('Persona deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default PersonaController;