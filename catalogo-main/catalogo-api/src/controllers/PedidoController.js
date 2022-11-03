import PedidoService from '../services/PedidoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class PedidoController {

  static async create(req, res) {
    let newPedido= req.body;
    try {      
               
      const pedidoEntidad =await PedidoService.create(newPedido);          
      return res.json(Response.get('pedido creado', pedidoEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando el pedido'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await PedidoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de pedidos', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const pedido = await PedidoService.getById(req.params.id);

      if (pedido) {
        return res.json(Response.get('pedido encontrado', pedido));
      }
      return res.json(Response.get('pedido no encontrado', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updatePedido = await PedidoService.update(id, name);

      return res.json(Response.get('pedido actualizado', updatePedido));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando el pedido'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await PedidoService.delete(req.params.id);
      return res.json(Response.get('pedido eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando el pedido', error, 500));
    }
  }
}

export default PedidoController;