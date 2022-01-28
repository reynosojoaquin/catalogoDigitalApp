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
         Nueva  Terminal
        </div>
      </q-card-section>
       <q-separator></q-separator>
      <q-card-section  class="q-mb-md" >
        <q-form    >
             <div class="row q-gutter-lg ">
                <div class="col-11 ">
                      <div class="row">
                        <div class="col-12">
                          <q-input class="full-width" v-model="id" label="ID" placeholder="ID" hint="terminalID"  />
                        </div>
                     
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="nombre" label="Descripcion" placeholder="DESCRIPCION" hint="Descripcion Termminal"  />
                         </div>
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="apellido" label="Imei" placeholder="IMEI" hint="Imei Terminal"  />
                         </div> 
                      </div>
                      <div class="row">
                           <div class="col-11">
                          <q-input   label="Persona" placeholder="PERSONA" hint="Persona"  />
                         </div> 
                         <div class="col-1 q-mt-md q-pl-xl" > <q-btn round color="primary" icon="search" ></q-btn></div>
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
 
  </q-page>
</template>

<script>
export default {
  data()
  {
      return{
        url: 'user_male2-512.png',
        sexo,
        id,
        nombre,
        apellido,
        correo,
        cedula
      }
  }
   
}
</script>
