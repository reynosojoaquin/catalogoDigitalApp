import Telefono from '../models/Telefono';

class TelefonoService {

  static async create(newTelefono) {
    try {
     // if (validaTelefono(newTelefono.numero)) {
        
      const entityCreated = await Telefono.create(newTelefono);
      return entityCreated;
     // }

    } catch (error) {
      console.log(error);
      throw error;
    }
  }

  static async update(id, telefono) {
    try {
      await Telefono.update(telefono, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Telefono.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const telefono = await Telefono.findOne({ where: { id } });
      return telefono;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Telefono.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }
  


  
}

/*
function validaTelefono(str) {

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
}*/
export default TelefonoService;