import ProductoTipoService from '../services/ProductoTipoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class ProductoTipoController {

  static async create(req, res) {
    let newProductoTipo = req.body;
    try {      
      const ProductoTipoEntidad =await ProductoTipoService.create(newProductoTipo);          
      return res.json(Response.get('tipo producto creado', ProductoTipoEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando el tipo producto'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await ProductoTipoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de tipo productos', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const tipoProducto = await ProductoTipoService.getById(req.params.id);

      if (tipoProducto) {
        return res.json(Response.get('tipo producto encontrado', tipoProducto));
      }
      return res.json(Response.get('tipo producto no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updateTipoProducto = await ProductoTipoService.update(id, name);

      return res.json(Response.get('tipo producto actualizado', updateTipoProducto));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando tipo producto'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await ProductoTipoService.delete(req.params.id);
      return res.json(Response.get('tipo producto eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando el tipo producto', error, 500));
    }
  }
}

export default ProductoTipoController;