<template>
  <q-page padding>

  <q-card class="q-mt-md q-gutter-sm" >
      <q-card-section >
        <div class="text-h6 text-grey-8">
        Indice  Contactos
        <span class="float-right">
            <q-btn
              round
              color="primary"
              icon="person"
              @click="agregarContacto()"
            />
          </span>
      </div>
      </q-card-section>
      <q-card-section class="q-pa-none q-mb-sm" >
        <q-table
          title="Busqueda"
          :rows="detailContacto"
          :columns="columns"
          row-key="id"
          :filter="filter"
         
        >
          <template v-slot:top-right>
            <q-input v-if="show_filter" filled borderless dense debounce="300" v-model="filter" placeholder="Search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>
          <q-btn class="q-ml-sm" icon="filter_list" @click="show_filter=!show_filter" flat/>
          </template>
          

          <template v-slot:body-cell-Action="props">
            <q-td :props="props">
              <q-btn icon="edit"
              @click="editContact(props.row.id)"
               size="sm" 
               flat dense/>
              <q-btn icon="delete" 
                     size="sm" 
                     class="q-ml-sm" 
                     flat dense
                     @click="removeContact(props.row)"
                     />
            </q-td>
          </template>


        </q-table>
      </q-card-section>
        <q-btn
        class="q-mt-sm q-mb-sm q-ml-sm"
        push
        color="accent"
        icon="cancel"
        label="Cancelar"
        @click="terminar()"
      />
       <q-btn
        class="q-mt-sm q-mb-sm q-ml-sm"
        push
        color="blue-grey"
        icon="check_circle_outline"
        label="Aplicar"
        @click="aplicar()"
      />

       
  </q-card>
   <q-card class="q-mt-sm"  v-show="ShowRegistrationModule">
          <ContactosCreate  
          :key ="reCreateComponet" 
          @getContacto="getContactoData">
          </ContactosCreate>
    </q-card>  

  </q-page>
  
</template>

<script>
import ContactosCreate from "../contactos/contactos-create";
import helpers from "../../../mixins/helpers"
export default {
 props:{setContactosData:{type:Array,default:()=>[]}},
 name: 'Index',
 mixins:[helpers],
 components: { ContactosCreate},
 data(){
   return {
       columns: [
                    {name: 'Nombre', label: 'NOMBRE', field: 'nombre', sortable: true, align: 'left'},
                    {name: 'apellido', label: 'APELLIDO', field: 'apellido', sortable: true, align: 'left'},
                    {name: 'tipo', label: 'TIPO', field: 'tipo', sortable: true, align: 'left'},
                    {name: 'Action', label: 'ACCIONES', field: 'Action', sortable: false, align: 'center'},
                ],
                 contactos: [
                    
                ],
                 filter: '',
                show_filter: false,
                addContact:false,
                tipoContacto:[
        {label:'Esposa(o)',id:1},
        {label:'Hijo(a)',id:2},
        {label:'Hermano(a)',id:3}],
        detailContacto:[],
        reCreateComponet:0,
        ShowRegistrationModule: false,
        tempData:[],
        clienteID:0
    }
 },
 created(){
     console.log('REGISTRO CONTACTOS MOUNTED')
     this.setup()
     if(this.tempData.length > 0){
       this.showDetailContact(this.tempData) 
     }
    
 },methods:{
   agregarContacto(){
     this.$store.commit('Contacts/SET_REGISTRO_STATE', 'creating');
     this.currentContact = null
     this.ShowRegistrationModule = true; 
   },
   forceRender(){
      this.reCreateComponet += 1
   },
   removeContact(data){
     this.tempData.forEach(function(item, index, object) {
        if (item.id === data.id) {
              object.splice(index, 1);
         }
      }); 
       this.detailContacto.forEach(function(item, index, object) {
        if (item.id === data.id) {
              object.splice(index, 1);
         }
      }); 
   },
   terminar(){
       this.$emit('getContacto',null)
   },
    getContactoData(data) {
      if (data != null) {
        let objContacto = JSON.parse(JSON.stringify(data));
        let id = this.getMaxID(this.tempData,'id') + 1;
        let localContactType   = JSON.parse(JSON.stringify(this.tipoContacto));
         let estado = this.$store.getters['Contacts/getStateRegistro']
         if(estado == 'editing'){
           this.tempData.forEach(function(item,index,object){
                if(item.id == objContacto.id){
                                 
                    item.nombre     = objContacto.nombre
                    item.apellido   = objContacto.apellido
                    item.telefono   = objContacto.telefono
                    item.tipo_id    = objContacto.tipo_id
                    item.direccion  = objContacto.direccion
                    
                }
            })
             for(let i=0;i<this.detailContacto.length;i++){
                if(this.detailContacto[i].id == objContacto.id){
                   this.detailContacto[i].tipo        =   this.filtrarJson(localContactType,'id',objContacto.tipo_id)[0].label
                   this.detailContacto[i].nombre      =   objContacto.nombre
                   this.detailContacto[i].apellido    =   objContacto.apellido
              }
             }
                       
         }else if(estado == 'creating' ){
            objContacto.id =  0; 
            objContacto.persona_id = this.clienteID;
            this.tempData.push(objContacto);
            this.detailContacto.push(this.createDetailContact(objContacto))  
          
         }
         
         this.$store.commit('Contacts/SET_REGISTRO_STATE', '');
        this.ShowRegistrationModule = false 
        this.$emit('getContacto',this.tempData);
      } else {
        this.ShowRegistrationModule = false
      }
    },   
   editContact(id){
     
      let  currentContact = {
            id:       null,
            nombre:   null,
            apellido: null,
            telefono: null,
            tipo_id:  null,
            direccion:null
          }

      for(let i = 0; i<this.tempData.length;i++){
         if(this.tempData[i].id == id){
            currentContact.id        =  id
            currentContact.nombre    =  this.tempData[i].nombre
            currentContact.apellido  =  this.tempData[i].apellido
            currentContact.telefono  =  this.tempData[i].telefono
            currentContact.tipo_id   =  this.tempData[i].tipo_id
            currentContact.direccion =  this.tempData[i].direccion
          }
       }   
     this.$store.commit('Contacts/SET_REGISTRO_STATE', 'editing');
     this.$store.commit('Contacts/SET_CURRENT_CONTACT',currentContact);
     this.forceRender();
     this.ShowRegistrationModule = true; 
   },
   showCreateContactModule(){
           this.ShowRegistrationModule= true   
   },
   createContact(){
     this.$store.commit('Contact/SET_REGISTRO_STATE', 'creating');
     this.showCreateContactModule()
   },
   showDetailContact(data){
     console.log('show detail contact...')
     let i; 
 
     let localContact = JSON.parse(JSON.stringify(data))
     for(i = 0; i < localContact.length;i++){
         let description      = {id:'',nombre:'',apellido:'',tipo:''}  
         description = this.createDetailContact(localContact[i])
         this.detailContacto.push(description)
     }
   },
   createDetailContact(data){
         let description        = {id:'',nombre:'',apellido:'',tipo:''}  
         let localContactType   = JSON.parse(JSON.stringify(this.tipoContacto));
         description.id         = data.id
         description.nombre     = data.nombre
         description.apellido   = data.apellido
         description.tipo       = this.filtrarJson(localContactType,'id',data.tipo_id)[0].label
         return description
   },
   aplicar(){
     this.contactos = JSON.parse(JSON.stringify(this.tempData)); 
        this.$emit("getContacto", this.contactos);
   },
   setup(){
        let objData  =  JSON.parse(JSON.stringify(this.$store.getters["clients/getCurrentClient"]))
        if (this.contactos.length == 0) {
            this.contactos = objData.persona.contactos
            this.tempData = JSON.parse(JSON.stringify(this.contactos))
        }
      console.log(JSON.stringify(this.tempData))
      this.clienteID = objData.id
    
   }
 }
}
</script>
<style scoped>
     .imgbtnsize{
       font-size: 1.900em;
     }
</style>