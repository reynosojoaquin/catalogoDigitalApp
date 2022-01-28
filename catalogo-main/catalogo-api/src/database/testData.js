import cliente from '../models/Cliente';
import persona from '../models/Persona';
import telefono from '../models/Telefono';
import contacto from '../models/Contacto';
import direccion from '../models/Direccion';
import provincia from '../services/ProvinciaService';
import ciudad from '../services/CiudadService';
import sector from '../services/SectorService';
import tipoContacto from '../models/tipoContacto';
import tipoDireccion from '../models/tipoDireccion';
import tipoTelefono from '../models/tipoTelefono';
// Import model only for setup the initial data
import { sequelize } from './database';

/**
 * Development only!
 */

const testData = () => {

    sequelize.sync({ force: process.env.FORCE_SYNC == 'true' ? true : false })
        .then(async () => {
            console.log('INSERTANDO DATOS DE EJEMPLO');
            if (process.env.INSERTTESTDATA == 'true') {
                // Put here all yout inserts (create)
                await persona.create({
                    nombres: 'RAFAEL ',
                    apellidos: 'TAVERAS',
                    cedula: '05601053290',
                    estado: '1',
                    correoe: 'taveras@gmil.com',
                    sexo: 'M'
                }
                );
                 await cliente.create({
                    personaId: '1'
                });

                   await persona.create(
                {
                    nombres: 'JOAQUIN',
                    apellidos: 'REYNOSO',
                    cedula: '056109834',
                    estado: '1',
                    correoe: 'REYNOSOJOAQUIN@gmil.com',
                    sexo: 'M'
                }
                );
                await cliente.create({
                    personaId: '2'
                });

                // REGISTRANDO LOS TIPOS DE CONTATOS

                let contactoTipo = [
                    {Descripcion: 'Esposa(o)'},
                    {Descripcion: 'Hijo(a)'},
                    {Descripcion: 'Hermano(a)'},
                ];
               
                await  tipoContacto.bulkCreate(contactoTipo);
                
               // FIN DEL REGISTRO DE TIPO CONTACTOS


                await contacto.create({

                    telefono: '8095555555',
                    nombre: 'JUAN',
                    apellido:'perencejo',
                    direccion: 'CALLE H NUMERO 4 EN LAS COLINAS',
                    personaId: '1',
                    tipo_id: '1'

                },
                {

                    telefono: '829641220',
                    nombre: 'CHAMEL',
                    apellido:'REYNOSO',
                    direccion: 'CALLE H NUMERO 4 EN LAS COLINAS',
                    personaId: '2',
                    tipo_id: '1'

                }
                );

                   await provincia.create([
                     {Nombre:'Duarte'},
                     {Nombre:'Hermanas Mirabal'},
                     {Nombre:'Maria Trinidad Sanches'}
                ]);
                
                await ciudad.create([
                     {Nombre:'San Francisco Macoris',provincia_id: 1},
                     {Nombre:'Pimentel',provincia_id: 1},
                     {Nombre:'Las Guaranas',provincia_id: 1},
                     {Nombre:'Tenares',provincia_id: 2},
                     {Nombre:'San jose de conuco',provincia_id: 2 },
                     {Nombre:'Villa Tapia',provincia_id: 2 },
                     {Nombre:'El Factor',provincia_id: 3},
                     {Nombre:'El indio',provincia_id: 3 },
                     {Nombre:'matanza',provincia_id: 3 }
                ]);
                await sector.create([
                    {Nombre:'Sector San Fco 1',ciudad_id: 1},
                    {Nombre:'Sector pimentel 2',ciudad_id: 2 },
                    {Nombre:'Sector las guaranas',ciudad_id: 3},
                    {Nombre:'Sector tenares',ciudad_id: 4},
                    {Nombre:'Sector San jose',ciudad_id: 5 },
                    {Nombre:'Sector villa tapia',ciudad_id: 6 },
                    {Nombre:'Sector Factor',ciudad_id:7},
                    {Nombre:'Sector del indio',ciudad_id: 8 },
                    {Nombre:'Sector de matanza',ciudad_id:9 }
               ]);
                
               // REGISTRANDO LOS TIPOS DE DIRECCIONES 
               let direccion_tipo = [
                   {Descripcion:'Residencial'},
                   {Descripcion:'Trabajo'},
               ];
               await  tipoDireccion.bulkCreate(direccion_tipo);
               // FIN DEL REGISTRO DE TIPO DE DIRECCION

                await direccion.create({
                    'provincia': 'Duarte',
                    'seccion': 'Ciudad',
                    'municipio': 'San Francisco de Macoris',
                    'calle': 'primera',
                    'apartamento': '2',
                    'longitud': '556432343',
                    'latitud': '-7098909909890',
                    'personaId': '1',
                    numero:20,
                    tipo_id:1,
                    provincia_id:1,
                    ciudad_id:1,
                    sector_id:1,
                });

            // iNICIO DEL REGISTRO DEL TIPO TELEFONOS

              let tipos_tlefonos=[
                  {Descripcion:'Residencial'},
                  {Descripcion:'Celular'},
                  {Descripcion:'Trabajo'}
              ];

             await tipoTelefono.bulkCreate(tipos_tlefonos);
            // FIN DE L REGISTRO DEL TIPO TELEFONO  


                await telefono.create({

                    'numero': '8095555555',
                    tipo_id: 1,
                    personaId: 1
                });
                 await telefono.create({
                    numero: '8296417220',
                    tipo_id: 1,
                    personaId: 2
                });



            }
             console.log('DATOS DE EJEMPLO INSETADOS CORRECTAMENTE');
        })
        .catch(error => {
            console.log(error);

        });









};

export default testData;