import TipoTelefonoService from '../services/TipoTelefonoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';



class TipoTelefonoController {

  static async create(req, res) {
    let newTipoTelefono = req.body;
    try {
      const tipoTelefonoEntidad = await TipoTelefonoService.create(newTipoTelefono);
      return res.json(Response.get('Tipo Contacto created', tipoTelefonoEntidad));

    } catch (error) {

      res.status(500).json({
        message: 'Ha ocurrido un error al crear el tipo telefono' + error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await TipoTelefonoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Tipo telefono listado', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Ha ocurrido un error al solicitar el listado  tipo de telefono', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const user = await TipoTelefonoService.getById(req.params.id);

      if (user) {
        return res.json(Response.get('tipo telefono no encontrado', user));
      }
      return res.json(Response.get('tipo telefono no encontrado', {}));
    } catch (error) {
      return res.json(Response.get('Ha ocurrido un error al solicitar  el tipo de telefono', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const tipoTelefono = req.body;

    try {
      const updateDireccion = await TipoTelefonoService.update(id, tipoTelefono);

      return res.json(Response.get('tipo telefono actualizado', updateDireccion));
    } catch (error) {
      return res.json(Response.get('Ha ocurrido un error al actualizar el tipo de telefono', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await TipoTelefonoService.delete(req.params.id);
      return res.json(Response.get('Tipo telefono eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Ha ocurrido un error al eliminar el tipo de telefono', error, 500));
    }
  }
}

export default TipoTelefonoController;