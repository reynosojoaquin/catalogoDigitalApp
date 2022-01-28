import Rol from '../models/Rol';

class RolService {

  static async create(newRol) {
    try {
      const entityCreated = await Rol.create(newRol);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, rol) {
    try {
      await Rol.update(rol, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Rol.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const rol = await Rol.findOne({ where: { id } });
      return rol;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Rol.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default RolService;