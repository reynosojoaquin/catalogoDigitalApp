import DetalleJugada from '../models/DetalleJugada';

class DetalleJugadaService {

  static async create(newDetalleJugada) {
    try {
      const entityCreated = await DetalleJugada.create(newDetalleJugada);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, DetalleJugada) {
    try {
      await DetalleJugada.update(DetalleJugada, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await DetalleJugada.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const DetalleJugada = await DetalleJugada.findOne({ where: { id } });
      return DetalleJugada;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await DetalleJugada.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default DetalleJugadaService;