import Jugada from '../models/jugada';

class JugadaService {

  static async create(newJugada) {
    try {
      const entityCreated = await Jugada.create(newJugada);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, jugada) {
    try {
      await Jugada.update(jugada, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Jugada.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const jugada = await Jugada.findOne({ where: { id } });
      return jugada;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Jugada.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default JugadaService;