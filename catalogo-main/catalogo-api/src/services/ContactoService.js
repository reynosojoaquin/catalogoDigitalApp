import Contacto from '../models/Contacto';

class ContactoService {

  static async create(newConsorcio) {
    try {
      const entityCreated = await Contacto.create(newConsorcio);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, contacto) {
    try {
      await Contacto.update(contacto, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Contacto.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const contacto = await Contacto.findOne({ where: { id } });
      return contacto;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Contacto.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  } 
}

export default ContactoService;