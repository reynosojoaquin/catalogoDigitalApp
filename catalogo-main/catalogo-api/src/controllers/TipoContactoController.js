import TipoContactoService from '../services/TipoContactoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';



class TipoContactoController {

  static async create(req, res) {
    let newTipoContacto = req.body;
    try {
      const tipoContactoEntidad = await TipoContactoService.create(newTipoContacto);
      return res.json(Response.get('Tipo Contacto created', tipoContactoEntidad));

    } catch (error) {

      res.status(500).json({
        message: 'Ha ocurrido un error al crear el tipo de contacto' + error,
        data: error
      });
    }
  }

  static async getAll(req, res) {
    const { query } = req;

    let { where, limit, offset, order } = querystringConverterHelper.parseQuery(query);

    try {
      const { rows, count, total } = await TipoContactoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Tipo Contacto listado', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Ha ocurrido un error al solicitar el listado  tipo de contacto', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const user = await TipoContactoService.getById(req.params.id);

      if (user) {
        return res.json(Response.get('tipo contacto no encontrado', user));
      }
      return res.json(Response.get('tipo contacto no encontrado', {}));
    } catch (error) {
      return res.json(Response.get('Ha ocurrido un error al solicitar  el tipo de contacto', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const tipoContacto = req.body;

    try {
      const updateDireccion = await TipoContactoService.update(id, tipoContacto);

      return res.json(Response.get('Direccion Updated', updateDireccion));
    } catch (error) {
      return res.json(Response.get('Ha ocurrido un error al actualizar el tipo de contacto', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await TipoContactoService.delete(req.params.id);
      return res.json(Response.get('Tipo contacto eliminado', {}));
    } catch (error) {
      return res.json(Response.get('Ha ocurrido un error al eliminar el tipo de contacto', error, 500));
    }
  }
}

export default TipoContactoController;