import Cliente from '../models/Cliente';
import Persona from '../models/Persona';
import Telefono from '../models/Telefono';
import Contacto from '../models/Contacto';
import Direccion from '../models/Direccion';
class ClienteService {
 

  static async create(persona) {
    try {
      console.log(persona);
      const entityCreated = await Cliente.create(persona);
      return await this.getById(entityCreated.id);
    } catch (error) {
      throw error;
    }
  }

  static async update(id, cliente) {
    try {
      await Cliente.update(cliente, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {// AQUI SE HACE EL JOIN CON LA TABLA PERSONA PARA TRAER LOS DATOS GENERALES. 
      const { rows } = await Cliente.findAndCountAll({
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
    const cliente = await Cliente.findOne({
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
    });

    return cliente;
  }

  static async delete(id) {
    try {
      const rowCount = await Cliente.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default ClienteService;