import Provincia from '../models/provincia';

class ProvinciaService {

  static async create(newProvincia) {
    try {
   
       const ProvinciaCreated = await  Provincia.bulkCreate(newProvincia);
      return ProvinciaCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, Provincia) {
    try {
      await Provincia.update(Provincia, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Provincia.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const provincia = await Provincia.findOne({ where: { id } });
      return provincia;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Provincia.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default ProvinciaService;