import SuplidorService from '../services/suplidorService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class SuplidorController {

  static async create(req, res) {
    let newSuplidor= req.body;
    try {      
               
      const suplidorEntidad =await SuplidorService.create(newSuplidor);          
      return res.json(Response.get('suplidor creado', suplidorEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando el suplidor'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await SuplidorService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de Suplidores', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const suplidor = await SuplidorService.getById(req.params.id);

      if (suplidor) {
        return res.json(Response.get('Suplidor encontrada', suplidor));
      }
      return res.json(Response.get('Suplidor no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const name = req.body;

    try {
      const updateSuplidor = await SuplidorService.update(id, name);

      return res.json(Response.get('suplidor actualizada', updateSuplidor));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando el suplidor'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await SuplidorService.delete(req.params.id);
      return res.json(Response.get('Suplidor eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando el suplidor', error, 500));
    }
  }
}

export default SuplidorController;