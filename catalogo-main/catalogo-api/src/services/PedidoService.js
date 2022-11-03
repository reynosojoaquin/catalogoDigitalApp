import Pedido from '../models/Pedido';

class PedidoService {

  static async create(newPedido) {
    try {
        const pedidoCreated = await  Pedido.bulkCreate(newPedido);
      return pedidoCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,nombre) {
    try {
      await Pedido.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Pedido.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const pedido = await Pedido.findOne({ where: { id:id } });
      return pedido;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Pedido.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default PedidoService;