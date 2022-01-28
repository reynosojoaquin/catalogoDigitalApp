import Sector from '../models/sector';

class SectorService {

  static async create(newsector) {
    try {
        const sectorCreated = await  Sector.bulkCreate(newsector);
        return sectorCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, sector) {
    try {
      await sector.update(Sector, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Sector.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const sector = await Sector.findOne({ where: { id } });
      return sector;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Sector.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default SectorService;