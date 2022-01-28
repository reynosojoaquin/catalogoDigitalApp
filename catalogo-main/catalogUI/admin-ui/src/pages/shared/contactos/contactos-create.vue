<template>
  <q-page padding>
    <!-- content -->
   
    <q-card class="q-mt-md ">
       <q-card-section>
        <div class="text-h6 text-grey-8">
         Nuevo Contacto
        </div>
      </q-card-section>
       <q-separator></q-separator>
      <q-card-section  class="q-mb-md" >
        <q-form>
            <div class="row">
                <div class="col-12"> 
                    <q-select v-model="contacto.tipo_id" 
                     :options="tipoContacto" 
                     emit-value
                     map-options
                     option-value="value"
                     option-label="label"
                    label="Tipo Contacto" />
                </div>
            </div>
             <div class="row q-gutter-lg ">
                <div class="col-11 ">
                      <q-input class="full-width" 
                      v-model="contacto.nombre" label="Nombre"
                       placeholder="NOMBRE"
                        hint="Nombre del Contacto"  />
                </div>
                <div class="col-11 ">
                      <q-input class="full-width" 
                      v-model="contacto.apellido" label="Apellido"
                       placeholder="APELLIDO"
                        hint="Apellido del Contacto"  />
                </div>
                 <div class="col-11 ">
                      <q-input class="full-width" 
                      v-model="contacto.telefono" label="Telefono"
                       placeholder="TELEFONO"
                        hint="Telefono del Contacto"
                        mask="(###)###-####"
                      />
                </div>
                 <div class="col-11 ">
                      <q-input class="full-width" 
                      v-model="contacto.direccion" label="Direccion"
                      placeholder="DIRECCION"
                      hint="Direccion del Contacto"  />
                </div>
             </div>
     
           
      </q-form>  
      </q-card-section> 
      <q-separator></q-separator>  
      <q-card-section class="q-gutter-md"> 
        <q-btn 
              push 
              color="teal" 
              icon="save"  
              label="Registrar"  
              @click="setContacto"
        />
         <q-btn
          push
          color="blue-grey"
          icon="gpp_bad"
          label="Cancelar"
          @click="cancelar"     
        />
      </q-card-section>
       
    </q-card>
 
  </q-page>
</template>

<script>
export default {
  data()
  {
      return{
        tipoContactoID:null,
        tipoContacto:[
        {label:'Esposa(o)',value:1},
        {label:'Hijo(a)',value:2},
        {label:'Hermano(a)',value:3}],
         contacto:{
          id:null,
          nombre:   null,
          apellido: null,
          telefono: null,
          tipo_id:  null,
          direccion:null,
          persona_id:null
        }
      }      
  },
  methods:{
    cancelar()
    {
        this.$store.commit('Contacts/SET_REGISTRO_STATE', '')
        this.$emit('getContacto',null);
    },
    setContacto()
    {
        this.$emit('getContacto',this.contacto);
        this.tipoContactoID = null
        this.contacto.tipo_id   =  null;
        this.contacto.telefono = null;
        this.contacto.nombre   = null;
        this.contacto.apellido = null;
        this.contacto.direccion = null;     
    }
  },
  mounted(){
     let stateRegister  =  this.$store.getters['Contacts/getStateRegistro']
     console.log(stateRegister)
     if(stateRegister  == 'editing'){
        let currentContact = this.$store.getters['Contacts/getCurrentContact']
        this.contacto =  JSON.parse(JSON.stringify(currentContact))  
      //  console.log(JSON.stringify(this.telefono))
     }
 
  }
   
}
</script>
