import ClienteService from '../services/ClienteService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';
import PersonaService from '../services/PersonaService';
class ClienteController {


  static async create(req, res) {
    const newBody = req.body;
    var persona_id = 0;
    try {
    
      const entityPersonaCreate = await PersonaService.create(newBody);
      persona_id = entityPersonaCreate.id;
      console.log(persona_id);
      const newCliente = await ClienteService.create({persona_id :persona_id});
      return res.json(Response.get('Cliente creado', newCliente));

    } catch (error) {

      res.status(500).json({
        message: 'Something goes wrong with cliente create: ' + error,
        data: error
      });


    }


  }

  static async getAll(req, res) { 

    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await ClienteService.getAll({


        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Cliente lista', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const cliente = await ClienteService.getById(req.params.id);

      if (cliente) {
        return res.json(Response.get('Cliente encontrado', cliente));
      }
      return res.json(Response.get('Cliente no encontrado', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
     const cliente = req.body;

    try {
      const entityPersonaUpdate = await PersonaService.update(cliente);
      const updateCliente = await ClienteService.update(entityPersonaUpdate.id, cliente);

      return res.json(Response.get('cliente actualizado', updateCliente));
    } catch (error) {
      return res.json(Response.get('Error actualisando el cliente ==> '+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await ClienteService.delete(req.params.id);
      return res.json(Response.get('Cliente eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }



  }


}
export default ClienteController;