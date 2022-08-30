import TipoTelefono from '../models/tipoTelefono';

class TipoTelefonoService {

  static async create(newTipoTelefono) {
    try {
      const entityCreated = await TipoTelefono.bulkCreate(newTipoTelefono);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, tipoTelefono) {
    try {
      await TipoTelefono.update(tipoTelefono, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await TipoTelefono.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const tipoTelefono = await TipoTelefono.findOne({ where: { id } });
      return tipoTelefono;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await TipoTelefono.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default TipoTelefonoService;