import Terminal from '../models/Terminal';
 //import Consorcio from '../models/Consorcio';
//import Vendedor from '../models/Vendedor';
 import Banca from '../models/Banca';
class TerminalService {

  static async create(newTerminal) {
    try {
      const entityCreated = await Terminal.create(newTerminal);
      return entityCreated;
    } catch (error) {
      throw error;
    }
  }

  static async update(id, terminal) {
    try {
      await Terminal.update(terminal, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Terminal.findAndCountAll({
        ...criterions, include: [{
          //EM ESTA PARTE INCLUIMOS LOS DATOS DE LAS TABLAS RELACIONADAS
          model:    Banca ,
          // attributes: ['nombres', 'apellidos','estado','correoe','sexo'],      //campos especifinos, si no, todo lo del modelo
          required: true  
             
       
        }]  
              
          


      });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const terminal = await Terminal.findOne({ where: { id } });
      return terminal;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Terminal.destroy({
        where: { id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }

}

export default TerminalService;