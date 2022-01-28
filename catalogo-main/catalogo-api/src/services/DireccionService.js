import Direccion from '../models/Direccion';

class DireccionService {

  static async create(newDireccion) {
    try {
      const entityCreated = await Direccion.create(newDireccion);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, direccion) {
    try {
      await Direccion.update(direccion, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Direccion.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const direccion = await Direccion.findOne({ where: { id } });
      return direccion;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Direccion.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default DireccionService;