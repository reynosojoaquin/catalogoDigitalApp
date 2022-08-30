import ProvinciaService from '../services/provinciaService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class ProvinciaController {

  static async create(req, res) {
    let newProvincia= req.body;
    try {      
        
     const provinciaEntidad = await ProvinciaService.create(newProvincia);          
      return res.json(Response.get('provincia creada', provinciaEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'Something goes wrong'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await ProvinciaService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de provincias', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const provincia = await ProvinciaService.getById(req.params.id);

      if (provincia) {
        return res.json(Response.get('Provincia encontrada', provincia));
      }
      return res.json(Response.get('provincia no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const provincia = req.body;
     
    try {
      
      const updateProvincia = await ProvinciaService.update(id, provincia);
      return res.json(Response.get('Provincia actualizada', updateProvincia));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando la provincia'+error, error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await ProvinciaService.delete(req.params.id);
      return res.json(Response.get('provincia eliminada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando la provincia', error, 500));
    }
  }
}

export default ProvinciaController;