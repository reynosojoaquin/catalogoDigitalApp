import Modelo from '../models/productoModelo';

class ProductoModeloService {

  static async create(newModelo) {
    try {
        const modeloCreated = await Modelo.bulkCreate(newModelo);
      return modeloCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,nombre) {
    try {
      await Modelo.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Modelo.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const ciudad = await Modelo.findOne({ where: { id:id } });
      return ciudad;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Modelo.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default ProductoModeloService;