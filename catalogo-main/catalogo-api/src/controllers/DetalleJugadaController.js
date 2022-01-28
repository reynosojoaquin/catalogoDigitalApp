import DetalleJugadaService from '../services/DetalleJugadaService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class DetalleJugadaController {

  static async create(req, res) {
    const newDetallejugada= req.body;
    try {
      const entityCreated = await DetalleJugadaService.create(newDetallejugada);
      return res.json(Response.get('detaille created', entityCreated));
    } catch (error) {
       
      res.status(500).json({
        message: 'Something goes wrong'+' error'+ error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await DetalleJugadaService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Detail list', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const user = await DetalleJugadaService.getById(req.params.id);

      if (user) {
        return res.json(Response.get('Detail found', user));
      }
      return res.json(Response.get('Detail not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const detalleJugada = req.body;

    try {
      const updateDetalle = await DetalleJugadaService.update(id, detalleJugada);

      return res.json(Response.get('User Updated', updateDetalle));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await DetalleJugadaService.delete(req.params.id);
      return res.json(Response.get('User deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default DetalleJugadaController;