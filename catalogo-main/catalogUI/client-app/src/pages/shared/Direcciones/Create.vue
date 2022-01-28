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
         Nuevo Rol
        </div>
      </q-card-section>
       <q-separator></q-separator>
      <q-card-section  class="q-mb-md" >
        <q-form>
             <div class="row q-gutter-lg ">
                <div class="col-11 ">
                      <q-input class="full-width" v-model="ph" label="NOMBRE" placeholder="NOMBRE" hint="Role Nombre"  />
                </div>
              </div>
          
             </div>
              <div class="row q-gutter-lg ">
                <div class="col-11 ">
                      <q-input class="full-width" v-model="ph" label="NOMBRE" placeholder="NOMBRE" hint="Role Nombre"  />
                </div>
              </div>
          
             </div>
              <div class="row q-gutter-lg ">
                <div class="col-11 ">
                      <q-input class="full-width" v-model="ph" label="NOMBRE" placeholder="NOMBRE" hint="Role Nombre"  />
                </div>
              </div>
          
             </div>
               <div class="row q-gutter-lg ">
                 <div class="col-11"> 
                             <q-select v-model="model" :options="tipoDireccion" label="Tipo Direccion" />
                  </div>
              </div>
   
               <div class="row q-mt-sm q-gutter-sm">
                    <div  class="col-1 "> 
                      <q-btn size="20px" round   color="teal" icon="person_pin" />
                    </div>
                    <div class="col-5">
                        <q-input class="full-width" v-model="ph" label="Longitud" placeholder="LONGITUD" hint="Longitud Ubicacion"  />
                    </div>
                    <div class="col-5">
                        <q-input class="full-width" v-model="ph" label="Latitude" placeholder="LATITUDE" hint="Latitude Ubicacion"  />
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
        ph:null,
        model: null,
        tipoDireccion: ['Residencial','Trabajo']
    } 
    
      
  }
   
}
</script>
<style lang="sass" scoped>
.flex-break
  flex: 1 0 100% !important
  width: 0 !important


</style>
