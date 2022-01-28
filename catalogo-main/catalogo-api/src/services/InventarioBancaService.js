import inventarioBanca from '../models/InventarioBanca';

class InventarioTerminalService {

  static async create(newInventarioBanca) {
    try {
      const entityCreated = await inventarioBanca.create(newInventarioBanca);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, InventarioBanca) {
    try {
      await inventarioBanca.update(InventarioBanca, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await inventarioBanca.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const Banca = await Banca.findOne({ where: { id } });
      return Banca;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await inventarioBanca.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default InventarioTerminalService;