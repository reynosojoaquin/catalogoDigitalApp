import Ciudad from '../models/ciudad';

class CiudadService {

  static async create(newciudad) {
    try {
        const ciudadCreated = await  Ciudad.bulkCreate(newciudad);
      return ciudadCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id,nombre) {
    try {
      await Ciudad.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Ciudad.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const ciudad = await Ciudad.findOne({ where: { id:id } });
      return ciudad;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Ciudad.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default CiudadService;