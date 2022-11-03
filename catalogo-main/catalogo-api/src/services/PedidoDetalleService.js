import PedidoDetalle from '../models/PedidoDetalle';

class PedidoDetalleService {

  static async create(newPedidoDetalle) {
    try {
        const pedidoDetalleCreated = await  PedidoDetalle.bulkCreate(newPedidoDetalle);
      return pedidoDetalleCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,nombre) {
    try {
      await PedidoDetalle.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await PedidoDetalle.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const pedido = await PedidoDetalle.findOne({ where: { id:id } });
      return pedido;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await PedidoDetalle.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default PedidoDetalleService;