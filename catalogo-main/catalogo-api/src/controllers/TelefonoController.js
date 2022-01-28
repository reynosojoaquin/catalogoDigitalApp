import TelefonoService from '../services/TelefonoService';
//import ConsorcioService from '../services/ConsorcioService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';



class TelefonoController {

  static async create(req, res) {
    let newTelefono = req.body;
    try {
      const telefonoEntidad = await TelefonoService.create(newTelefono);
      return res.json(Response.get('Telefono created', telefonoEntidad));

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
      const { rows, count, total } = await TelefonoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Telefono list', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const user = await TelefonoService.getById(req.params.id);

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
    const telefono = req.body;

    try {
      const updateDireccion = await TelefonoService.update(id, telefono);

      return res.json(Response.get('Direccion Updated', updateDireccion));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await TelefonoService.delete(req.params.id);
      return res.json(Response.get('Direccion deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default TelefonoController;