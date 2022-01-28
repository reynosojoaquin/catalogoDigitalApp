import ConsorcioService from '../services/ConsorcioService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class ConsorcioController {
  static async create(req, res) {
    const newConsorcio= req.body;
    try {
      const entityCreated = await ConsorcioService.create(newConsorcio);
      return res.json(Response.get('User created', entityCreated));
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
      const { rows, count, total } = await ConsorcioService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Cliente list', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const consorcio = await ConsorcioService.getById(req.params.id);

      if (consorcio) {
        return res.json(Response.get('Cliente found', consorcio));
      }
      return res.json(Response.get('Cliente not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const consorcio = req.body;

    try {
      const updateConsorcio = await ConsorcioService.update(id, consorcio);

      return res.json(Response.get('User Updated', updateConsorcio));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await ConsorcioService.delete(req.params.id);
      return res.json(Response.get('Cliente deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default ConsorcioController;