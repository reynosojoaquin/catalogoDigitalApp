import UsuarioService from '../service/UsuarioService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';
import sequelize from 'sequelize';
import Persona from '../models/Persona';
class UsuarioController {
  static async create(req, res) {
    const t = await sequelize.transaction();// realiza la instancia de transaction para asegurarnos el commit seguro
    const newUsuario = req.body;
    try {
      const entityCreated = await UsuarioService.create(newUsuario);
      return res.json(Response.get('User created', entityCreated),

        { transaction: t },//validamos y hacemos commit 
        await t.commit()
      );



    } catch (error) {
      await t.rollback();//si hay un error entonces hacemos rollback
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
      const { rows, count, total } = await UsuarioService.getAll({
        include: [{
    model: Persona
  }],
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
      const user = await UsuarioService.getById(req.params.id);

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
    const usuario = req.body;

    try {
      const updateUsuario = await UsuarioService.update(id, usuario);

      return res.json(Response.get('User Updated', updateUsuario));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await UsuarioService.delete(req.params.id);
      return res.json(Response.get('User deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default UsuarioController;