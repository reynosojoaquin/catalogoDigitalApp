import ClienteService from './services/ClienteService';
//import Response from '../utils/response';
//import querystringConverterHelper from '../utils/querystringConverterHelper';
import PersonaService from './services/PersonaService';
const datos = [];
class DataExample {
    
    static async create() {
        var obj;
        obj['datos'].push({

            'nombre_banca': 'BANCA LA PRIMERA',
            'direccion': 'C4 URB. TORIBIO ',
            'email': 'SINCORREO@SINCORREO.COM',
            'estado': '1',
            'franquiciano': '23434331',
            'nom_consorcio': 'BANCAS LAS PODEROSAS',
            'direccion_fisica': 'CALLE M 5, SANTIAGO, CIUDAD',
            'emailb': 'bpoderosas@sincorreo.com',
            'estadob': '1',
            'cedula': '05601053290'

        });



        try {
            await PersonaService.create(obj);
            await ClienteService.create(obj);
            console.log(datos);


        } catch (error) {
                console.log(error);
            
        }

    }
}
export default DataExample;