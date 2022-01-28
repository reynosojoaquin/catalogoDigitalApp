<template>
  <q-page padding>
     <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6 text-grey-8">
        Indice  Telefonos
        <span class="float-right">
            <q-btn
              round
              color="primary"
              icon="add_ic_call"
              @click="createPhone()"
            />
          </span>
      </div>
      </q-card-section>
      <q-card-section class="q-pa-none">
        <q-table
          title="Busqueda"
          :rows="detailTelefono"
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
              <q-btn icon="edit" size="sm" 
               @click="editPhone(props.row.id)"
              flat dense/>
              <q-btn icon="delete" 
               size="sm" 
               class="q-ml-sm" 
                @click="removePhone(props.row)"
               flat dense/>
            </q-td>
          </template>


        </q-table>
      </q-card-section>
      <q-btn class="q-mt-sm q-mb-sm  q-ml-sm"   
              push
                color="blue-grey"
                icon="cancel"
                label="Terminar"
               @click="cancelar()"
              />
      <q-btn
        class="q-mt-sm q-mb-sm q-ml-sm"
        push
        color="accent"
        icon="check_circle_outline"
        label="Aplicar"
        @click="aplicar()"
      />
  </q-card>

      <q-card class="q-mt-sm"  v-show="ShowRegistrationModule">
           <TelefonoCreate 
            :key ="reCreateComponet" 
            @getTelefono="getTelefonoData"></TelefonoCreate>
    </q-card>     
  </q-page>
</template>

<script>
import TelefonoCreate  from "../telefonos/telefonos-create";
import helpers from '../../../mixins/helpers'
export default {
  props:{setTelefonosData:{type:Array,default:()=>[]}},
 name: 'Index',
 mixins:[helpers],
 components:{
   TelefonoCreate
 },
 data(){

    return {
       columns: [
                    {name: 'telefono', label: 'TELEFONO', field: 'telefono', sortable: true, align: 'left'},
                    {name: 'tipo', label: 'TIPO', field: 'tipo', sortable: true, align: 'left'},
                    {name: 'Action', label: 'ACCIONES', field: 'Action', sortable: false, align: 'center'},
                   
                ],
                 telefonos: [
                    
                ],
                 filter: '',
                show_filter: false,
                detailTelefono:[],
                tipoTelefono:[{label:'Residencial',id:1},
                              {label:'Celular',id:2},
                              {label:'Trabajo',id:3}],
                ShowRegistrationModule:false,
                reCreateComponet:0,
                currentTelefono:'',
                tempData:[]
    }
 },
 methods:{
  
   getTelefonoData(data){
     if (data != null) {

          console.log(JSON.stringify(data))
          let PhoneID     =  this.getMaxID(this.telefonos,'id') + 1
          let objtelefono = JSON.parse(JSON.stringify(data))
          let description = {id:'',telefono:'',tipo:''}
          description.id       =   objtelefono.id
          description.telefono = objtelefono.numero
          description.tipo     = this.filtrarJson(this.tipoTelefono,'id',objtelefono.tipo_id)[0].label 
          let estado = this.$store.getters['Phones/getStateRegistro']
           console.log(estado)      
          if(estado == 'editing'){
            this.telefonos.forEach(function(item,index,object){
                if(item.id == objtelefono.id){
                                 
                    item.tipo_id        = objtelefono.tipo_id
                    item.numero         = objtelefono.numero
                }
            })
              this.detailTelefono.forEach(function(item,index,object){
              if(item.id == objtelefono.id){
                   item.tipo      =    description.tipo
                   item.telefono    =    description.telefono
              }
            })  
              
          

          }else if(estado == 'creating'){
             description.id        =  PhoneID
             objtelefono.id       =  0
             this.detailTelefono.push(description)
             this.telefonos.push(objtelefono);
           
          }
          this.$store.commit('Phones/SET_REGISTRO_STATE', '');
          this.ShowRegistrationModule = false;
          this.forceRender()
         
      } else {
          this.ShowRegistrationModule = false;
          this.forceRender()
      }
        this.$emit('getTelefono',this.telefonos)
   },
   forceRender(){
      this.reCreateComponet += 1
   },
   cancelar(){
       this.$store.commit('Phones/SET_REGISTRO_STATE', '');
       this.$emit('getTelefono',null)
   },
   removePhone(data){
      this.detailTelefono.forEach(function(item, index, object) {
         if (item.id === data.id) {
              object.splice(index, 1);
         }
      }); 
    this.tempData.forEach(function(item, index, object) {
         if (item.id === data.id) {
              object.splice(index, 1);
         }
      })
      
   },
   editPhone(id){
     
      let  currentPhone = {
           id:     null, 
           numero: null,
           tipo_id:null
          }
       
       for(let i = 0; i<this.telefonos.length;i++){
         if(this.telefonos[i].id == id){
            currentPhone.id        =  id
            currentPhone.numero    =  this.telefonos[i].numero,
            currentPhone.tipo_id   =  this.telefonos[i].tipo_id
          }
       }   
     console.log(JSON.stringify(currentPhone))
    
     this.$store.commit('Phones/SET_REGISTRO_STATE', 'editing');
     this.$store.commit('Phones/SET_CURRENT_PHONE',currentPhone);
      this.ShowRegistrationModule = true; 
     this.forceRender() 
    
   },
   showCreatePhoneModule(){
           this.ShowRegistrationModule= true   
   },
   createPhone(){
     this.$store.commit('Phones/SET_REGISTRO_STATE', 'creating');
     this.currentTelefono = null
     this.showCreatePhoneModule()
   },
   showDetailTelefonos(data){
     console.log('show detail phome...')
     let i; 
     let estado = this.$store.getters['Phones/getStateRegistro']
     for(i = 0; i < data.length;i++){
         let description      = {id:'',telefono:'',tipo:''}  
         let localPhomeType   = JSON.parse(JSON.stringify(this.tipoTelefono));
         if(estado == 'creating'){
            description.id = tempData.length + 1
         }else{
            description.id       = data[i].id
         }
        
         description.telefono = data[i].numero
         description.tipo     = this.filtrarJson(localPhomeType,'id',data[i].tipo_id)[0].label
         this.detailTelefono.push(description)
       
     }
    
   },
   aplicar(){
     this.telefonos = JSON.parse(JSON.stringify(this.tempData)); 
     console.log(JSON.stringify(this.telefonos))
     this.$emit("getTelefono", this.telefonos);
   }
  
},
   created: function(){
      console.log('INDICE TELEFONOS MOUNTED')
      this.telefonos = this.setTelefonosData
      this.tempData = JSON.parse(JSON.stringify(this.telefonos))
      this.$store.commit('Phones/SET_REGISTRO_STATE', '');
      if(this.telefonos.length > 0){
        this.showDetailTelefonos(this.tempData)
     }
   }
 }
</script>
<style scoped>
     .imgbtnsize{
       font-size: 1.900em;
     }
</style>