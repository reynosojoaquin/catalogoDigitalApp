import ContactoService from '../services/ContactoService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';

class ContactoController {
  static async create(req, res) {
    const newConctato= req.body;
    try {
      const entityCreated = await ContactoService.create(newConctato);
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
      const { rows, count, total } = await ContactoService.getAll({
        criterions: {
          where,
          limit,
          offset,
          order,
        }
      });

      return res.json(Response.get('Contacto list', rows, 200, { count, total, offset }));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }


  static async getById(req, res) {
    try {
      const contacto = await ContactoService.getById(req.params.id);

      if (contacto) {
        return res.json(Response.get('Cliente found', contacto));
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
      const updateConsorcio = await ContactoService.update(id, consorcio);

      return res.json(Response.get('User Updated', updateConsorcio));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await ContactoService.delete(req.params.id);
      return res.json(Response.get('Cliente deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default ContactoController;