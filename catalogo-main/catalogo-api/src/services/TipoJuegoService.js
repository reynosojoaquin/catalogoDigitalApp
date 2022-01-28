import TipoJuego from '../models/TipoJuego';

class TipoJuegoService {

  static async create(newTipoJuego) {
    try {
      const entityCreated = await TipoJuego.create(newTipoJuego);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, tipoJuego) {
    try {
      await TipoJuego.update(tipoJuego, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await TipoJuego.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const tipoJuego = await TipoJuego.findOne({ where: { id } });
      return tipoJuego;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await TipoJuego.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default TipoJuegoService;