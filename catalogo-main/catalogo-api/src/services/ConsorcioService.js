import Consorcio from '../models/Consorcio';

class ConsorcioService {

  static async create(newConsorcio) {
    try {
      const entityCreated = await Consorcio.create(newConsorcio);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, consorcio) {
    try {
      await Consorcio.update(consorcio, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Consorcio.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const consorcio = await Consorcio.findOne({ where: { id } });
      return consorcio;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Consorcio.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  } 
}

export default ConsorcioService;