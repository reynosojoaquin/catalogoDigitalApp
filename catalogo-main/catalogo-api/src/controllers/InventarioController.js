import InventarioService from '../services/InventarioService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class InventarioController {

  static async create(req, res) {
    let newInventario= req.body;
    try {      
               
      const InventarioEntidad =await InventarioService.create(newInventario);          
      return res.json(Response.get('inventario  creado', InventarioEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando el inventario'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await InventarioService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Listado inventario', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const inventario = await InventarioService.getById(req.params.id);

      if (inventario) {
        return res.json(Response.get('Inventario encontrado', inventario));
      }
      return res.json(Response.get('Inventario no encontrado', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updateInventario = await InventarioService.update(id, name);

      return res.json(Response.get('Inventario actualizado', updateInventario));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando el inventario'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await InventarioService.delete(req.params.id);
      return res.json(Response.get('inventario eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando el inventario', error, 500));
    }
  }
}

export default InventarioController;