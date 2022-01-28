import DireccionService from '../services/DireccionService';
//import ConsorcioService from '../services/ConsorcioService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';



class DireccionController {

  static async create(req, res) {
    let newDireccion = req.body;
    try {

      const direccionEntidad = await DireccionService.create(newDireccion);
      return res.json(Response.get('Direccion created', direccionEntidad));

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
      const { rows, count, total } = await DireccionService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Direccion list', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const user = await DireccionService.getById(req.params.id);

      if (user) {
        return res.json(Response.get('Direccion found', user));
      }
      return res.json(Response.get('Direccion not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const direccion = req.body;

    try {
      const updateDireccion = await DireccionService.update(id, direccion);

      return res.json(Response.get('Direccion Updated', updateDireccion));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await DireccionService.delete(req.params.id);
      return res.json(Response.get('Direccion deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default DireccionController;