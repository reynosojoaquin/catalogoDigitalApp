import Suplidor from '../models/Suplidor';

class SuplidorService {

  static async create(newsuplidor) {
    try {
         if(validarDocumento(newsuplidor.tipo_documento,newsuplidor.documento))
         {
            const suplidorCreated = await  Suplidor.create(newsuplidor);
            return suplidorCreated;
         }else   throw {name: 'error validando documento', message: 'Documento no válido!'};
      } catch (error) {
       throw error;
      }
    }

  static async update(id,nombre) {
    try {
      await Suplidor.update(nombre, { where: { id: id } });
      return await this.getById(id);
    } catch (error) {
      throw error;
    }
  }

  static async getAll(params) {
    const { criterions } = params;

    try {
      const { rows } = await Suplidor.findAndCountAll({ ...criterions });
      return { rows, count: rows.length };
    } catch (error) {
      throw error;
    }
  }

  static async getById(id) {

    try {
      const suplidor = await Suplidor.findOne({ where: { id:id } });
      return suplidor;
    } catch (error) {
      throw error;
    }
  }

  static async delete(id) {
    try {
      const rowCount = await Suplidor.destroy({
        where: { id:id }
      });
      return { count: rowCount };
    } catch (error) {
      throw error;
    }
  }






  

}
 /**
     * Este método valida si el RNC de la República Dominicana es válida,
     *No se pasan guiones en el  argumento.
     * 
     * @since 1.1v
     * @param rnc es un arreglo de char numérico
     * @return true si el rnc es válido
     */
  function  validarRNC(rnc){
    var peso = ['7','9','8','6','5','4','3','2'];
    let suma = 0;
    let division = 0;
    
    if (rnc.length != 9)
        return false;
    else
    {
        for (let i = 0; i < 8; i++) {
            //para verificar si es un dígito o no
            if (!isNaN(rnc[i]))
                return false;
            
            suma = suma  + (rnc[i] * peso[i] );
        }
        
        division = suma / 11;
        let resto = suma - (division * 11);
        let digito = 0;
        
        if (resto == 0 )
            digito = 2;
        else if (resto == 1)
            digito = 1;
        else 
            digito = 11 - resto;
        
        if (digito != rnc[8] )
            return false;            
    }      
    
    return true;
}    

/***
 * Metodo que valida el numero de cedula
 * @param tipo este valor indetifica el tipo de documento que sera validado
 * @param documento documento que sera validado
 */
function validateCedula(str) {

  var regex = new RegExp('^[0-9]{3}-?[0-9]{7}-?[0-9]{1}$');
  if (!regex.test(str)) {
    return false;
  } else {
    str = str.replace(/-/g, '');
    return CheckDigit(str);

  }


}

function CheckDigit(str) {
  let sum = 0;
  for (var i = 0; i < 10; ++i) {
    var n = ((i + 1) % 2 !== 0 ? 1 : 2) * parseInt(str.charAt(i));
    sum += (n <= 9 ? n : n % 10 + 1);
  }
  var dig = ((10 - sum % 10) % 10);
  return dig === parseInt(str.charAt(10));
}
function validarDocumento(tipo,documento){
  if(tipo === 'cedula'){
    return validateCedula(documento);
  }else{
    return validarRNC(documento);
  }
}

export default SuplidorService;