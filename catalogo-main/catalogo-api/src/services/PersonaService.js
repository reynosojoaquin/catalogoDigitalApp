import Persona from '../models/Persona';
import Telefono from '../models/Telefono';
import Contacto from '../models/Contacto';
import Direccion from '../models/Direccion';


class PersonaService {
  static async create(newPersona) {
    try {
      console.log(newPersona.cliente.telefonos);
      if (validateCedula(newPersona.cliente.cedula)) {
        const entityCreated = await Persona.create(newPersona.cliente);
        
        const bulkTelefonos = newPersona.cliente.telefonos.map(telefono => {
          return { ...telefono, persona_id: entityCreated.id };
        }); 
        Telefono.bulkCreate(bulkTelefonos);
          const bulkDirecciones = newPersona.cliente.direcciones.map(direccion => {
          return { ...direccion, persona_id: entityCreated.id };
        });
        
        Direccion.bulkCreate(bulkDirecciones);

        const bulkContactos = newPersona.cliente.contactos.map(contacto => {
          return { ...contacto, persona_id: entityCreated.id };
        });       
        Contacto.bulkCreate(bulkContactos);
        
        
        console.log('comparativa contactos');
        console.log(newPersona.cliente.contactos);
        console.log('fin compartiva contactos');
        console.log(bulkContactos);


        

        return entityCreated;
      } else   throw {name: 'validation error', message: 'Cédula no válida!'};
     

    } catch (error) {
      throw error;
    }


  }

  static async update(persona,res) {
    try {
      console.log(JSON.stringify(persona));
      let personaId = persona.id;
      
      
        await Telefono.destroy({
            where:{
               personaId
            }            
        });
        await Direccion.destroy({
             where:{
               personaId
             }             
        });
        await Contacto.destroy({
              where:{
              personaId
              }
        });
       console.log(JSON.stringify(personaId));
      const bulkUpdateTelefonos = persona.telefonos.map(telefono => {
        return { ...telefono, persona_id: personaId };
      }); Telefono.bulkCreate(bulkUpdateTelefonos);

     
      const bulkUpdateDirecciones = persona.direcciones.map(direccion => {
        return { ...direccion, persona_id: personaId };
      });

      Direccion.bulkCreate(bulkUpdateDirecciones);

      const bulkUpdateContactos = persona.contactos.map(contacto => {
        return { ...contacto, persona_id: personaId };
      });
      Contacto.bulkCreate(bulkUpdateContactos);

      await Persona.update(persona, { where: { id: personaId } });
      return await this.getById(personaId);
    } catch (error) {
      res.status(500).json({
        message: 'Something goes wrong with cliente update: ' + error,
        data: error
      });
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Persona.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const persona = await Persona.findOne({ where: { id } });
      return persona;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Persona.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }



}





function validateCedula(str) {

  var regex = new RegExp('^[0-9]{3}-?[0-9]{7}-?[0-9]{1}$');
  if (!regex.test(str)) {
    return false;
  } else {
    str = str.replace(/-/g, '');
    return CheckDigit(str);

  }


}

function CheckDigit(str) {
  let sum = 0;
  for (var i = 0; i < 10; ++i) {
    var n = ((i + 1) % 2 !== 0 ? 1 : 2) * parseInt(str.charAt(i));
    sum += (n <= 9 ? n : n % 10 + 1);
  }
  var dig = ((10 - sum % 10) % 10);
  return dig === parseInt(str.charAt(10));
}

export default PersonaService;