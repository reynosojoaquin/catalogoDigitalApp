import inventarioTerminal from '../models/InventarioTerminal';

class InventarioTerminalService {

  static async create(newInventarioTerminal) {
    try {
      const entityCreated = await inventarioTerminal.create(newInventarioTerminal);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, InventarioTerminal) {
    try {
      await inventarioTerminal.update(InventarioTerminal, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await inventarioTerminal.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const Terminal = await Terminal.findOne({ where: { id } });
      return Terminal;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await inventarioTerminal.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default InventarioTerminalService;