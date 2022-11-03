import inventario from '../models/Inventario';

class InventarioService {

  static async create(newInventario) {
    try {
        const inventarioCreated = await  inventario.bulkCreate(newInventario);
      return inventarioCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,precio,costo,flete,suplidor_id,existencia) {
    try {
      await inventario.update(precio,costo,flete,suplidor_id,existencia, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await inventario.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const Inventario = await inventario.findOne({ where: { id:id } });
      return Inventario;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await inventario.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default InventarioService;