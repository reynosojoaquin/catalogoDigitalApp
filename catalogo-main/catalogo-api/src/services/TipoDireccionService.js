import TipoDireccion from '../models/tipoDireccion';

class TipoDireccionService {

  static async create(newTipoDireccion) {
    try {
      const entityCreated = await TipoDireccion.create(newTipoDireccion);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, TipoDireccion) {
    try {
      await TipoDireccion.update(TipoDireccion, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await TipoDireccion.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const tipoDireccion = await TipoDireccion.findOne({ where: { id } });
      return tipoDireccion;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await TipoDireccion.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default TipoDireccionService;