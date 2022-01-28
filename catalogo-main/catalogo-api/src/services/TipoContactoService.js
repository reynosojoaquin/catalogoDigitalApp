import TipoContacto from '../models/tipoContacto';

class TipoContactoService {

  static async create(newTipoContacto) {
    try {
      const entityCreated = await TipoContacto.create(newTipoContacto);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, tipoContacto) {
    try {
      await TipoContacto.update(tipoContacto, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await TipoContacto.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const tipoContacto = await TipoContacto.findOne({ where: { id } });
      return tipoContacto;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await TipoContacto.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default TipoContactoService;