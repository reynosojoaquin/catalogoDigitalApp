import Usuario from '../models/Banca';

class UsuarioService {

  static async create(newUsuario) {
    try {
      const entityCreated = await Usuario.create(newUsuario);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, usuario) {
    try {
      await Usuario.update(usuario, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Usuario.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const usuario = await Usuario.findOne({ where: { id } });
      return usuario;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Usuario.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default UsuarioService;