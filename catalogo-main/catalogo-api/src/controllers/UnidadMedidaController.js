import UnidadMedidaService from '../services/UnidadMedidaService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class UnidadMedidaController {

  static async create(req, res) {
    let newUnidadMedida= req.body;
    try {      
               
      const UnidadMedidaEntidad =await UnidadMedidaService.create(newUnidadMedida);          
      return res.json(Response.get('ciudad creada', UnidadMedidaEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando la Unidad de medida'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await UnidadMedidaService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado unidad medida', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const UnidadMedida = await UnidadMedidaService.getById(req.params.id);

      if (UnidadMedida) {
        return res.json(Response.get('Unidad Medida encontrada', UnidadMedida));
      }
      return res.json(Response.get('Unidad Medida no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updateUnidadMedida = await UnidadMedidaService.update(id, name);

      return res.json(Response.get('Unidad Medida actualizada', updateUnidadMedida));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando la Unidad Medida'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await UnidadMedidaService.delete(req.params.id);
      return res.json(Response.get('Unidad Medida eliminada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando la Unidad Medida', error, 500));
    }
  }
}

export default UnidadMedidaController;