import ProductoModeloService from '../services/productoModeloService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class ProductoModeloController {

  static async create(req, res) {
    let newProductoModelo= req.body;
    try {      
               
      const productoModeloEntidad =await ProductoModeloService.create(newProductoModelo);          
      return res.json(Response.get('Modelo creado', productoModeloEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando el modelo'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await ProductoModeloService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de Modelos', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error al consultar los modelos de producto', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const modelo = await ProductoModeloService.getById(req.params.id);

      if (modelo) {
        return res.json(Response.get('Modelo encontrado', modelo));
      }
      return res.json(Response.get('Modelo no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error al consultar un modelo', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updatemodelo = await ProductoModeloService.update(id, name);

      return res.json(Response.get('Modelo actualizado', updatemodelo));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando el modelo'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await ProductoModeloService.delete(req.params.id);
      return res.json(Response.get('modelo eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando el modelo', error, 500));
    }
  }
}

export default ProductoModeloController;