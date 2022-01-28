import Permiso from '../models/Permiso';

class PermisoService {

  static async create(newPermiso) {
    try {
      const entityCreated = await Permiso.create(newPermiso);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, permiso) {
    try {
      await Permiso.update(permiso, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Permiso.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const permiso = await Permiso.findOne({ where: { id } });
      return permiso;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Permiso.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default PermisoService;