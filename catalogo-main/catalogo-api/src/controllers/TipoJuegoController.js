import TipoJuegoService from '../services/TipoJuegoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class TipoJuegoController {

  static async create(req, res) {
    const newTipoJuego= req.body;
    try {
      const entityCreated = await TipoJuegoService.create(newTipoJuego);
      return res.json(Response.get('new play type created', entityCreated));
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
      const { rows, count, total } = await TipoJuegoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('play type list', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const tipoJuego = await TipoJuegoService.getById(req.params.id);

      if (tipoJuego) {
        return res.json(Response.get('play type found', tipoJuego));
      }
      return res.json(Response.get('play type not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const banca = req.body;

    try {
      const updateTipoJuego = await TipoJuegoService.update(id, banca);

      return res.json(Response.get('play type Updated', updateTipoJuego));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await TipoJuegoService.delete(req.params.id);
      return res.json(Response.get('play type deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default TipoJuegoController;