import Suplidor from '../models/Suplidor';

class SuplidorService {

  static async create(newsuplidor) {
    try {
        const suplidorCreated = await  Suplidor.bulkCreate(newsuplidor);
      return suplidorCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,nombre) {
    try {
      await Suplidor.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Suplidor.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const suplidor = await Suplidor.findOne({ where: { id:id } });
      return suplidor;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Suplidor.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default SuplidorService;