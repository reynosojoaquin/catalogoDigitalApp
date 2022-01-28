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
         Nueva  Banca
        </div>
      </q-card-section>
       <q-separator></q-separator>
      <q-card-section  class="q-mb-md" >
        <q-form    >
             <div class="row q-gutter-lg ">
                <div class="col-11 ">
                      <div class="row">
                        <div class="col-12">
                          <q-input class="full-width" v-model="id" label="ID" placeholder="ID" hint="bancaID"  />
                        </div>
                     
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="nombre" label="Franquicia No." placeholder="FRANQUICIA No." hint="Numero de franquicia"  />
                         </div>
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="apellido" label="Nombre" placeholder="NOMBRE" hint="Nombre Banca"  />
                         </div> 
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="cedula" label="No. Sucursal" placeholder="No SUCURSAL" hint="Numero de sucursal"  />
                          </div>
                      </div>
                    
                      
                      
                </div>
                 
             </div>
             <div class="row ">
                        <div class="col-12">
                                   <q-card class="full-width q-mt-lg">
                                <div class=" flex item-center justify-center centers q-pa-sm items-center  q-gutter-sm ">
                                      <q-btn color="orange-10" text-color="white" label="Direccion" icon="room" />
                                      <q-btn color="indigo-10" label="Telefono" icon="local_phone" />
                                      <q-btn color="black" label="Contacto" icon="contacts"/>
                                      <q-btn color="teal" label="Configuraciones" icon="build"/>
                                </div>
                            </q-card>
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
