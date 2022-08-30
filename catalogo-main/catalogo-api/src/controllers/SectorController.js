import SectorService from '../services/SectorService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class SectorController {

  static async create(req, res) {
    let newSector= req.body;
    try {      
               
      const sectorEntidad =await SectorService.create(newSector);          
      return res.json(Response.get('Sector creada', sectorEntidad));      
      
    } catch (error) {
       
      res.status(500).json({
        message: 'se generado un error creando la Sector'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await SectorService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('listado de sectores', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('se ha producido un error', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const sector = await SectorService.getById(req.params.id);

      if (sector) {
        return res.json(Response.get('sector encontrada', sector));
      }
      return res.json(Response.get('sector no encontrada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const sector = req.body;

    try {
      console.log(id);
      const updatesector = await SectorService.update(id, sector);

      return res.json(Response.get('sector actualizada', updatesector));
    } catch (error) {
      return res.json(Response.get('Se ha producido un error actualizando la sector', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await SectorService.delete(req.params.id);
      return res.json(Response.get('sector eliminada', {}));
    } catch (error) {
      return res.json(Response.get('Se ha produciodo un error eliminando la sector', error, 500));
    }
  }
}

export default SectorController;