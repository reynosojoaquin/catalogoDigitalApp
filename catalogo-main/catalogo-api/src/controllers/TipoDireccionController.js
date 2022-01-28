import TipoDireccionService from '../services/TipoDireccionService';
//import ConsorcioService from '../services/ConsorcioService';
import Response from '../utils/response';
import querystringConverterHelper from '../utils/querystringConverterHelper';



class TipoDireccionController {

  static async create(req, res) {
    let newTipoDireccion= req.body;
    try {      
      //const consorcioEntidad = await ConsorcioService.create(newBanca);    
       //newBanca.idconsorcio=consorcioEntidad.id;  
           
     const tipoDireccion =await TipoDireccionService.create(newTipoDireccion);          
      return res.json(Response.get('tipo Direccion created', tipoDireccion));      
      
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
      const { rows, count, total } = await TipoDireccionService.getAll({
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
      const tipoDireccion = await TipoDireccionService.getById(req.params.id);

      if (tipoDireccion) {
        return res.json(Response.get('Tipo Direccion found', tipoDireccion));
      }
      return res.json(Response.get('Tipo Direccion not found', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async update(req, res) {
    const { id } = req.params;
    const tipoDireccion = req.body;

    try {
      const updateTipoDireccion = await TipoDireccionService.update(id, tipoDireccion);

      return res.json(Response.get('Tipo Dirreccion Updated', updateTipoDireccion));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }

  static async delete(req, res) {
    try {
      await TipoDireccionService.delete(req.params.id);
      return res.json(Response.get('Tipo direccion  deleted', {}));
    } catch (error) {
      return res.json(Response.get('Something goes wrong', error, 500));
    }
  }
}

export default TipoDireccionController;