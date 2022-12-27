import PedidoDetalleService from '../services/PedidoDetalleService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class PedidoDetalleController {

  static async create(req, res) {
    let newPedidoDetalle = req.body;
    try {      
               
      const pedidoDetalleEntidad =await PedidoDetalleService.create(newPedidoDetalle);          
      return res.json(Response.get('pedido detalle creado', pedidoDetalleEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando el detalle pedido'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await PedidoDetalleService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de los detalles de un pedidos', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const pedido = await PedidoDetalleService.getById(req.params.id);

      if (pedido) {
        return res.json(Response.get('detalle pedido encontrado', pedido));
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
      const updatePedido = await PedidoDetalleService.update(id, name);

      return res.json(Response.get('pedido actualizado', updatePedido));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando el pedido'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await PedidoDetalleService.delete(req.params.id);
      return res.json(Response.get('pedido eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando el detalle del pedido', error, 500));
    }
  }
}

export default PedidoDetalleController;