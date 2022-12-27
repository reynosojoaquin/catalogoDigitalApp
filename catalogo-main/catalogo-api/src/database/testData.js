/*import cliente from '../models/Cliente';
import persona from '../models/Persona';
import telefono from '../models/Telefono';
import contacto from '../models/Contacto';
import direccion from '../models/Direccion';


*/
import cliente from '../services/ClienteService';
import provincia from '../services/ProvinciaService';
import ciudad from '../services/CiudadService';
import sector from '../services/SectorService';
import tipoContacto from '../models/tipoContacto';
import tipoDireccion from '../models/tipoDireccion';
import tipoTelefono from '../models/tipoTelefono';
import productoMarca from '../models/productoMarca';
import productoModelo from '../models/productoModelo';
import productoTipo from '../models/ProductoTipo';
import productoUnidadMedida from '../models/UnidadMedida';
import producto from '../models/Producto';
import vendedor from '../services/VendedorService';
import suplidor from '../services/SuplidorService';
import inventario from '../services/InventarioService';
import statusPedido from '../services/EstatusPedidoService';
import pedidos from '../services/PedidoService';
import detallePedido from '../services/PedidoDetalleService';
// Import model only for setup the initial data
import { sequelize } from './database';


/**
 * Development only!
 */
const force = process.env.FORCE_SYNC;
const TEST_DATA = process.env.TEST_DATA;
const testData = () => {

    sequelize.sync({force: force})
        .then(async () => {

            if(TEST_DATA==='true'){
                console.log('Registrando data de prueba');

                // registrando cliente de ejemplo


                //PROVINCIAS
                let provincia_data =   [
                    {Nombre:'Santiago'},
                    {Nombre:'Santo Domingo'},
                    {Nombre:'Puerto Plata'},
                    {Nombre:'La Altagracia'},
                    {Nombre:'Duarte'},
                    {Nombre:'San Cristóbal'},
                    {Nombre:'San pedro de Macoris'},
                    {Nombre:'Santo domingo'},
                    {Nombre:'La Vega'},
                    {Nombre:'La Romana'},
                    {Nombre:'Espaillat'},
                    {Nombre:'San Cristóbal'},
                    {Nombre:'San Juan de La Maguana'},
                    {Nombre:'San Cristóbal'},
                    {Nombre:'Monseñor Nouel'},
                    {Nombre:'Sánchez Ramírez'},
                    {Nombre:'Peravia'},
                    {Nombre:'Barahona'},
                    {Nombre:'Azua'},
                    {Nombre:'Santo Domingo'},
                    {Nombre:'La Romana'},
                    {Nombre:'Valverde Mao'},
                    {Nombre:'Santiago Rodríguez'},
                    {Nombre:'El Seibo'},
                    {Nombre:'María Trinidad Sanchez'},
                    {Nombre:'Hato Mayor'},
                    {Nombre:'Monte plata'},
                    {Nombre:'Monte Plata'}
                ];
             //CREANDO PROVINCIAS
             await provincia.create(provincia_data);
      
              // REGISTRANDO LOS TIPOS DE CONTATOS

              let contactoTipo = [
                {Descripcion: 'Esposa(o)'},
                {Descripcion: 'Hijo(a)'},
                {Descripcion: 'Hermano(a)'},
            ];
           
            await  tipoContacto.bulkCreate(contactoTipo);
            
           // FIN DEL REGISTRO DE TIPO CONTACTOS

           
            await ciudad.create([
                 {Nombre:'San Francisco Macoris',provincia_id: 1},
                 {Nombre:'Pimentel',provincia_id: 1},
                 {Nombre:'Las Guaranas',provincia_id: 1},
                 {Nombre:'Tenares',provincia_id: 1},
                 {Nombre:'San jose de conuco',provincia_id: 1},
                 {Nombre:'Villa Tapia',provincia_id: 2},
                 {Nombre:'El Factor',provincia_id: 2},
                 {Nombre:'El indio',provincia_id: 2},
                 {Nombre:'matanza',provincia_id: 2}
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

            // iNICIO DEL REGISTRO DEL TIPO TELEFONOS

            let tipos_tlefonos=[
                {Descripcion:'Residencial'},
                {Descripcion:'Celular'},
                {Descripcion:'Trabajo'}
            ];

           await tipoTelefono.bulkCreate(tipos_tlefonos);
          // FIN DE L REGISTRO DEL TIPO TELEFONO  

         // REGISTRANDO TIPO PROUDCTOS

         let tipos_productos =[
            {nombre:'Teclados'},
            {nombre:'Bocinas'},
            {nombre:'Laptops'},
            {nombre:'Desktop'}
         ];
            
         await productoTipo.bulkCreate(tipos_productos);

         // FIN DEL REGISTRO DE LOS TIPOS DE  PRODUCTOS

         // REGISTRANDO LAS MARCAS DE LOS PROUCTOS

         let marcas_productos =[
            {nombre:'Sony'},
            {nombre:'Apple'},
            {nombre:'Logitech'}
         ];
         await productoMarca.bulkCreate(marcas_productos);

         // FIN DEL REGISTRO DE LOS PRODUCTOS

         // REGISTRO DE MODELOS PRODUCTOS

         let Modelos =[
              {nombre:'TEC089',marca_id:1},
              {nombre:'TEC486',marca_id:1},
              {nombre:'a1314',marca_id:2}  
         ];
          await productoModelo.bulkCreate(Modelos);


            }


        // Registrando las unidades de medida

        let unidades_medida = [
            {nombre:'Unidad'},
            {nombre:'cajas'},
            {nombre:'libras'}
        ];
            console.log(unidades_medida);
        await productoUnidadMedida.bulkCreate(unidades_medida);

              
            var objClient = {};
            objClient = {'persona':{
                    'nombres': 'JUANA ANTONIA',
                     'apellidos': 'TAVERAS PEREZ',
                     'cedula': '05601098345',
                     'activo': true,
                     'correo':'PJUANA@gmil.com',
                     'sexo': 'M',
                     'url' : '',
                     'persona_id':0,
                     'telefonos':[{
                         'numero':'8095883613',
                         'persona_id':0,
                         'tipo_id':'1'
                     }],
                     'direcciones':[{
                         'calle':'L',
                         'numero':'76',
                         'apartamento':'',
                         'longitud':'000000000',
                         'latitude':'111111111',
                         'persona_id':0,
                         'tipo_id':'1',
                         'provincia_id': '1',
                         'ciudad_id':'1',
                         'sector_id':'1'
                     }],
                     'contactos':[{
                         'nombre':'chamel',
                         'apellido':'reynoso',
                         'telefono':'8098891264',
                         'direccion':'calle l 76',
                         'persona_id':0,
                         'tipo_id':'1'
                     }]
           
         }
        };
         await cliente.create(objClient);

         let productos = [
            {
                nombre: 'Teclado USB',
                codigoInterno : 1,
                codigoBarras: '0000000000000000000', 
                activo:  true,
                descripcion: 'producto generico de prueba',
                exento:true,
                imgUrl: '/images/',
                reorden: 5,
                marca_id: 1,
                modelo_id:1,
                tipo_id: 1,
                unidad_id:1
              }    ];

          await producto.bulkCreate(productos);
          var objVendendor ={};
          objVendendor = {'persona':{
            'nombres': 'Jhon',
             'apellidos': 'snow',
             'cedula': '05500014500',
             'activo': true,
             'correo':'PJUANA@gmil.com',
             'sexo': 'M',
             'url' : '',
             'persona_id':0,
             'telefonos':[{
                 'numero':'8095883613',
                 'persona_id':0,
                 'tipo_id':'1'
             }],
             'direcciones':[{
                 'calle':'L',
                 'numero':'76',
                 'apartamento':'',
                 'longitud':'000000000',
                 'latitude':'111111111',
                 'persona_id':0,
                 'tipo_id':'1',
                 'provincia_id': '1',
                 'ciudad_id':'1',
                 'sector_id':'1'
             }],
             'contactos':[{
                 'nombre':'chamel',
                 'apellido':'reynoso',
                 'telefono':'8098891264',
                 'direccion':'calle l 76',
                 'persona_id':0,
                 'tipo_id':'1'
             }]
   
             }
            };
        await vendedor.create(objVendendor);
        // RESGISTRANDO DATOS DE MUESTRA DEL SUPLIDOR
        var objSuplidor = {};
        objSuplidor = {
            'nombre':'COMPUMISCEL',
            'telefono':'8092200000',
            'ubicacion':'calle castillo 21',
            'contacto':'Jose el Hage',
            'documento':'05601098345',
            'tipo_documento':'cedula'
        };

        await suplidor.create(objSuplidor);

        // REGISTRANDO DATOS DE MUESTRA DEL INVENTARIO

        var objInventario ={};
        objInventario = [{
            'producto_id': 1,
            'precio': 207.50,
            'costo': 150.00,
             'flete': 50,
            'suplidor_id':1,
            'existencia': 200,
            'margen':  5 
        }];
        await inventario.create(objInventario);

        // REGISTRANDO DATOS DE MUESTRA DE LOS ESTADOS DE LOS PEDIDOS
        var objStatus = {};
        objStatus =[
        { 'descripcion': 'Solicitado al suplidor'},
        {'descripcion':  'En almacen'},
        {'descripcion':  'pendiente de entrega'}    
        ];
        await statusPedido.create(objStatus);

        var objPedidos = {};
        objPedidos =[
            {
                'fecha': '2022-12-09',
                'status_id': 1,
                'vendedor_id': 1,
                'total':2000,
                'cliente_id':1,
                 'activo':true
             }
        ];
        await pedidos.create(objPedidos);


        var objDetallePedido={};
        objDetallePedido = [{
            'producto_id': 1,
            'pedido_id':1,
            'cantidad':20,
            'precio':100,
            'total':2000
        }];

       await  detallePedido.create(objDetallePedido);
    console.log('sincronisacion completa');
    })
    .catch(error => {
        console.log(error);

    });
   
};

export default testData;