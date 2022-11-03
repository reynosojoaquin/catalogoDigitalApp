import UnidadMedida from '../models/UnidadMedida';

class UnidadMedidaService {

  static async create(newUnidadMedida) {
    try {
        const UnidadMedidaCreated = await UnidadMedida.bulkCreate(newUnidadMedida);
      return UnidadMedidaCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,nombre) {
    try {
      await UnidadMedida.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await UnidadMedida.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const unidadMedida = await UnidadMedida.findOne({ where: { id:id } });
      return unidadMedida;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await UnidadMedida.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default UnidadMedidaService;