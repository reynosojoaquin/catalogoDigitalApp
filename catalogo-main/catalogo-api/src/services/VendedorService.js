import Vendedor from '../models/Vendedor';
import Persona from '../models/Persona';
import Telefono from '../models/Telefono';
import Contacto from '../models/Contacto';
import Direccion from '../models/Direccion';
class VendedorService {

  static async create(newVendedor) {
    try {
      const entityCreated = await Vendedor.create(newVendedor);
     
       return await this.getById(entityCreated.id);//devuelve el json de lo guardado
    } catch (error) {
      throw error;
    }
  }

  static async update(id, vendedor) {
    try {
      await Vendedor.update(vendedor, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }
  static async getAll(params) {
    const { criterions } = params;

    try {// AQUI SE HACE EL JOIN CON LA TABLA PERSONA PARA TRAER LOS DATOS GENERALES. 
      const { rows } = await Vendedor.findAndCountAll({
        ...criterions,
        include: [{
          model: Persona,
          include: [{
            model: Telefono,
            required: false,
          },
          {
            model: Contacto,
            required: false
          },
          {
            model: Direccion,
            required: false
          }
          ]
        }]
      });


      return { rows, count: rows.length };
    } catch (error) {
      console.log(error);
      throw error;
    }
  }

  static async getById(id) {
    try {
    const vendedor = await vendedor.findOne({
      where: { id },
      include: [{
        model: Persona,
        include: [{
          model: Telefono,
          required: false,
        },
        {
          model: Contacto,
          required: false
        },
        {
          model: Direccion,
          required: false
        }
        ]
      }]
    });} catch (error) {
      console.log(error);
      throw error;


    }
  
    return Vendedor;
  }

  static async delete(id) {
    try {
      const rowCount = await Vendedor.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}


export default VendedorService;