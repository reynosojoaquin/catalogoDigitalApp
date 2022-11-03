import ProductoTipo from '../models/ProductoTipo';

class productoTipoService {

  static async create(newTipo) {
    try {
        const tipoCreated = await  ProductoTipo.bulkCreate(newTipo);
        return tipoCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,nombre) {
    try {
      await ProductoTipo.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await ProductoTipo.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const tipo = await ProductoTipo.findOne({ where: { id:id } });
      return tipo;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await ProductoTipo.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default productoTipoService;