import VendedorService from '../services/VendedorService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class VendedorController {

  static async create(req, res) {
    const newBody = req.body;
     try {
      const newVendedor = await VendedorService.create(newBody);
      return res.json(Response.get('Vendedor creado', newVendedor));

    } catch (error) {

      res.status(500).json({
        message: 'Something goes wrong vendedor create: ' + error,
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

      return res.json(Response.get('Vendedor lista', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const vendedor = await VendedorService.getById(req.params.id);

      if (vendedor) {
        return res.json(Response.get('Vendedor encontrado', vendedor));
      }
      return res.json(Response.get('Vendedor no encontrado', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
     const vendedor = req.body;

    try {
      
      const updateVendedor = await VendedorService.update(vendedor);
      return res.json(Response.get('Vendedor actualizado', updateVendedor));
    } catch (error) {
      return res.json(Response.get('Error actualisando el vendedor ==> '+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await VendedorService.delete(req.params.id);
      return res.json(Response.get('Vendedor eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }

  }


}
export default VendedorController;