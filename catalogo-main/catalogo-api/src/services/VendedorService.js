import Vendedor from '../models/Vendedor';
import Persona from '../models/Persona';
import Telefono from '../models/Telefono';
import Contacto from '../models/Contacto';
import Direccion from '../models/Direccion';
import PersonaService from '../services/PersonaService';
class VendedorService {
 

  static async create(persona) {
    try {

         let vendedor =  { };
         vendedor['persona_id'] = 0;
      const entityPersonaCreate = await PersonaService.create(persona);
      vendedor.persona_id = entityPersonaCreate.id;
      const entityCreated = await Vendedor.create(vendedor);
      return await this.getById(entityCreated.id);
    } catch (error) {
      throw error;
    }
  }

  static async update(vendedor) {
    try {
      const entityPersonaUpdate = await PersonaService.update(vendedor);
      console.log(entityPersonaUpdate);
      return await this.getById(entityPersonaUpdate.id);
    } catch (error) {
      console.log('error en el servicio del vendedor');
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
    const vendedor = await Vendedor.findOne({
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
     return vendedor;
  }

  static async delete(id) {
    try {
      //recuperando el cliente de la base de datos
      var client =  await this.getById(id);

      console.log('print data client =======> '+client);
      //asignando el id de la persona a la variable global 
      var personid = client.persona_id;
       //eliminando los telefonos registrados a la persona
       await Telefono.destroy({
        where:{
           persona_id:id
        },force:true            
      });
      // eliminnado las direcciones registradas a la persona
      await Direccion.destroy({
         where:{
           persona_id:id
         } ,force:true           
      });
      // eliminando los contactos registrados a la persona
      await Contacto.destroy({
          where:{
          persona_id:id
          },force:true
      });
      //eliminando el cliente de la base de datos
      const rowCount = await Vendedor.destroy({
        where: { id }
      });
      
      // eliminando la persona relacionada al clente de la base de datos
      await Persona.destroy({
          where: { id:personid}
      });

    
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default VendedorService;