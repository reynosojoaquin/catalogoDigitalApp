import Cliente from '../models/Cliente';
import Persona from '../models/Persona';
import Telefono from '../models/Telefono';
import Contacto from '../models/Contacto';
import Direccion from '../models/Direccion';
import PersonaService from '../services/PersonaService';
class ClienteService {
 

  static async create(persona) {
    try {

         let cliente =  { };
         cliente['persona_id'] = 0;
      const entityPersonaCreate = await PersonaService.create(persona);
      cliente.persona_id = entityPersonaCreate.id;
      
      console.log('Desplegando datos del cliente: '+JSON.stringify(cliente));
      const entityCreated = await Cliente.create(cliente);
      return await this.getById(entityCreated.id);
    } catch (error) {
      throw error;
    }
  }

  static async update(cliente) {
    try {
      const entityPersonaUpdate = await PersonaService.update(cliente);
      console.log(entityPersonaUpdate);
      return await this.getById(entityPersonaUpdate.id);
    } catch (error) {
      console.log('error en el servicio del cliente');
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
      const rowCount = await Cliente.destroy({
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

export default ClienteService;