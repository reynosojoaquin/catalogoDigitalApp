import marca from '../models/productoMarca';
import ProductoMarca from '../models/productoMarca';

class productoMarcaService {

  static async create(newMarca) {
    try {
        const marcaCreated = await  marca.bulkCreate(newMarca);
      return marcaCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,nombre) {
    try {
      await ProductoMarca.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await ProductoMarca.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const ciudad = await ProductoMarca.findOne({ where: { id:id } });
      return ciudad;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await ProductoMarca.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default productoMarcaService;