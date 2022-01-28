import VendedorService from '../services/VendedorService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';
import PersonaService from '../services/PersonaService';
class VendedorController {
  static async create(req, res) {
    const newVendedor= req.body;
    try {
      
       const entityPersonaCreate=await PersonaService.create(newVendedor);
       newVendedor.personaId=entityPersonaCreate.id;
      const entityCreated = await VendedorService.create(newVendedor);

      return res.json(Response.get('User created', entityCreated));
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
      const { rows, count, total } = await VendedorService.getAll({
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
      const vendedor = await VendedorService.getById(req.params.id);

      if (vendedor) {
        return res.json(Response.get('Vendedor found', vendedor));
      }
      return res.json(Response.get('Vendedor not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const vendedor = req.body;

    try {
      const updateVendedor = await VendedorService.update(id, vendedor);

      return res.json(Response.get('User Updated', updateVendedor));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await VendedorService.delete(req.params.id);
      return res.json(Response.get('Cliente deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default VendedorController;