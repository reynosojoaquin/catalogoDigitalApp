import loteria from '../models/Loteria';

class LoteriaService {

  static async create(newLoteria) {
    try {
      const entityCreated = await loteria.create(newLoteria);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, Loteria) {
    try {
      await Loteria.update(Loteria, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await loteria.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const Loteria = await Loteria.findOne({ where: { id } });
      return Loteria;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await loteria.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default LoteriaService;