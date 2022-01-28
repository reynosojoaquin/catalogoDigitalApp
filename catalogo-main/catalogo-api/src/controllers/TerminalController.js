import TerminalService from '../services/TerminalService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class TerminalController {

  static async create(req, res) {
    const newTerminal= req.body;
    try {
      const entityCreated = await TerminalService.create(newTerminal);
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
      const { rows, count, total } = await TerminalService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('List', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const user = await TerminalService.getById(req.params.id);

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
    const terminal = req.body;

    try {
      const updateTerminal = await TerminalService.update(id, terminal);

      return res.json(Response.get('User Updated', updateTerminal));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await TerminalService.delete(req.params.id);
      return res.json(Response.get('User deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default TerminalController;