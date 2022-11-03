import ProductoMarcaService from '../services/productoMarcaService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class ProductoMarcaController {

  static async create(req, res) {
    let newProductoMarca= req.body;
    try {      
               
      const productoMarcaEntidad =await ProductoMarcaService.create(newProductoMarca);          
      return res.json(Response.get('Marca creada', productoMarcaEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando la marca'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await ProductoMarcaService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de Marcas', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const marca = await ProductoMarcaService.getById(req.params.id);

      if (marca) {
        return res.json(Response.get('marca encontrada', marca));
      }
      return res.json(Response.get('marca no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updatemarca = await ProductoMarcaService.update(id, name);

      return res.json(Response.get('marca actualizada', updatemarca));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando la marca'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await ProductoMarcaService.delete(req.params.id);
      return res.json(Response.get('marca eliminada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando la marca', error, 500));
    }
  }
}

export default ProductoMarcaController;