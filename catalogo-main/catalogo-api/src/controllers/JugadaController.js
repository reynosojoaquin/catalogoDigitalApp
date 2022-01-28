import JugadaService from '../services/JugadaService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';
import DetalleJugadaService from '../services/DetalleJugadaService';



class JugadaController {

  static async create(req, res) {
    const newJugada = req.body;
    try {
      const entityCreated = await JugadaService.create(newJugada);
      newJugada.idjugada = entityCreated.id;//agarramos el id de la jugada 
      await DetalleJugadaService.create(newJugada);//savamos el detalle con el mismo json 
      return res.json(Response.get('Game created', entityCreated));
    } catch (error) {

      res.status(500).json({
        message: 'Something goes wrong' + error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await JugadaService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('User list', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const user = await JugadaService.getById(req.params.id);

      if (user) {
        return res.json(Response.get('Play found', user));
      }
      return res.json(Response.get('Play not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const banca = req.body;

    try {
      const updateJugada = await JugadaService.update(id, banca);

      return res.json(Response.get('Play Updated', updateJugada));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await JugadaService.delete(req.params.id);
      return res.json(Response.get('Play deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default JugadaController;