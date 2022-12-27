import EstatusPedidoService from '../services/EstatusPedidoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class StatusController {

  static async create(req, res) {
    let newStatus= req.body;
    try {      
               
      const statusEntidad =await EstatusPedidoService.create(newStatus);          
      return res.json(Response.get('status creado', statusEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se a generado un error creando el status'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await EstatusPedidoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de estados pedido', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const status = await EstatusPedidoService.getById(req.params.id);

      if (status) {
        return res.json(Response.get('estado encontrada', status));
      }
      return res.json(Response.get('estado no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updateStatus = await EstatusPedidoService.update(id, name);

      return res.json(Response.get('estado actualizada', updateStatus));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando el estado'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await EstatusPedidoService.delete(req.params.id);
      return res.json(Response.get('estado pedido eliminada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error eliminando la ciudad', error, 500));
    }
  }
}

export default StatusController;