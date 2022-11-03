import ProductoService from '../services/ProductoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class ProductoController {

  static async create(req, res) {
    let newProducto= req.body;
    try {      
               
      const productoEntidad =await ProductoService.create(newProducto);          
      return res.json(Response.get('producto creado', productoEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando el producto'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await ProductoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de Productos', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const producto = await ProductoService.getById(req.params.id);

      if (producto) {
        return res.json(Response.get('producto encontrado', producto));
      }
      return res.json(Response.get('producto no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updateProducto = await ProductoService.update(id, name);

      return res.json(Response.get('producto actualizado', updateProducto));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando el producto'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await ProductoService.delete(req.params.id);
      return res.json(Response.get('Producto eliminada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando el producto', error, 500));
    }
  }
}

export default ProductoController;