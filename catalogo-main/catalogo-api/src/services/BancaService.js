import Banca from '../models/Banca';

class BancaService {

  static async create(newBanca) {
    try {
      const entityCreated = await Banca.create(newBanca);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, banca) {
    try {
      await Banca.update(banca, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Banca.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const banca = await Banca.findOne({ where: { id } });
      return banca;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Banca.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default BancaService;