<template>
  <q-page padding>
    <!-- content -->
    <q-toolbar inset class="bg-primary text-white">
          <q-breadcrumbs active-color="white" style="font-size: 16px">
            <q-breadcrumbs-el label="Home" icon="home" />
            <q-breadcrumbs-el label="Components" icon="widgets" />
            <q-breadcrumbs-el label="Toolbar" />
          </q-breadcrumbs>
     </q-toolbar>
    <q-card class="q-mt-md ">
       <q-card-section>
        <div class="text-h6 text-grey-8">
         Nuevo Consorcio
        </div>
      </q-card-section>
       <q-separator></q-separator>
      <q-card-section  class="q-mb-md" >
        <q-form   >
             <div class="row q-gutter-lg ">
                <div class="col-11 ">
                      <div class="row">
                        <div class="col-12">
                          <q-input class="full-width"  label="ID" placeholder="ID" hint="Usuario ID"  />
                        </div>
                     
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" label="Nombre" placeholder="NOMBRE" hint="Nombre Usuario"  />
                         </div>
                      </div>
                      <div class="row">
                         <div class="col-11">
                          <q-input   label="Cliente" placeholder="CLIENTE" hint="Propietario del consorcio"  />
                         </div> 
                         <div class="col-1 q-mt-md q-pl-xl" > <q-btn round color="primary" icon="search" @click="show"></q-btn></div>
                      </div>
                 
                </div>
              
             </div>

      </q-form>  
      </q-card-section> 
     
      <q-separator></q-separator>  
      <q-card-section>
        <q-btn push color="teal" icon="save"  label="Registrar"  />
     
      </q-card-section>
       
    </q-card>     
    <q-dialog ref="dialog" v-model="toolbar" class="busquedadialog">
        <q-card class="q-dialog-plugin full-width">
               <busqueda-clientes></busqueda-clientes>
         </q-card>
   </q-dialog>
  </q-page>
</template>

 
<script>
import busquedadialog from '../clientes/clientes-busqueda';


export default {
   components: {'busqueda-clientes': busquedadialog},
  data()
  {
      return{
        url: 'user_male2-512.png',
        toolbar:false,
        persistent:true
      }
  },
 
   methods: {
    // following method is REQUIRED
    // (don't change its name --> "show")
    getData (data) {
      
    },

    // following method is REQUIRED
    // (don't change its name --> "hide")
    hide () {
      this.$refs.dialog.hide()
    },

    onDialogHide () {
      // required to be emitted
      // when QDialog emits "hide" event
      this.$emit('hide')
    },

    onOKClick () {
      // on OK, it is REQUIRED to
      // emit "ok" event (with optional payload)
      // before hiding the QDialog
      this.$emit('ok')
      // or with payload: this.$emit('ok', { ... })

      // then hiding dialog
      this.hide()
    },

    onCancelClick () {
      // we just need to hide dialog
      this.hide()
    },
     show () {
           this.$refs.dialog.show()
           console.log(busquedadialog)
    }
  }
   
}
</script>
