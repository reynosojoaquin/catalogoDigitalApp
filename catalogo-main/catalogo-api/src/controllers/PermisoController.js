import PermisoService from '../services/PermisoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class PermisoController {

  static async create(req, res) {
    const newPermiso= req.body;
    try {
      const entityCreated = await PermisoService.create(newPermiso);
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
      const { rows, count, total } = await PermisoService.getAll({
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
      const user = await PermisoService.getById(req.params.id);

      if (user) {
        return res.json(Response.get('User found', user));
      }
      return res.json(Response.get('User not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const permiso = req.body;

    try {
      const updatePermiso = await PermisoService.update(id, permiso);

      return res.json(Response.get('User Updated', updatePermiso));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await PermisoService.delete(req.params.id);
      return res.json(Response.get('User deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default PermisoController;