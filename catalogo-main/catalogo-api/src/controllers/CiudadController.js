import CiudadService from '../services/ciudadService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class CiudadController {

  static async create(req, res) {
    let newCiudad= req.body;
    try {      
               
      const ciudadEntidad =await CiudadService.create(newCiudad);          
      return res.json(Response.get('ciudad creada', ciudadEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando la ciudad'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await CiudadService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de ciudades', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const ciudad = await CiudadService.getById(req.params.id);

      if (ciudad) {
        return res.json(Response.get('ciudad encontrada', ciudad));
      }
      return res.json(Response.get('ciudad no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const ciudad = req.body;

    try {
      const updateciudad = await CiudadService.update(id, ciudad);

      return res.json(Response.get('ciudad actualizada', updateciudad));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando la ciudad', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await CiudadService.delete(req.params.id);
      return res.json(Response.get('ciudad eliminada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando la ciudad', error, 500));
    }
  }
}

export default CiudadController;