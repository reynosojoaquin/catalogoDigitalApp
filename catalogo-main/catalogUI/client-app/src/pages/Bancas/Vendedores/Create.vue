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
         Nuevo vendedor
        </div>
      </q-card-section>
       <q-separator></q-separator>
      <q-card-section  class="q-mb-md" >
        <q-form    >
             <div class="row q-gutter-lg ">
                <div class="col-9 ">
                      <div class="row">
                        <div class="col-12">
                          <q-input class="full-width" v-model="id" label="ID" placeholder="ID" hint="Cliente ID"  />
                        </div>
                     
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="nombre" label="Nombre" placeholder="NOMBRE" hint="Nombre Vendedor"  />
                         </div>
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="apellido" label="Apellido" placeholder="APELLIDO" hint="Apellido vededor"  />
                         </div> 
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="cedula" label="Cedula" placeholder="CEDULA" hint="Numero de cedula"  />
                          </div>
                      </div>
                      <div class="row">
                         <div class="col-12">
                          <q-input class="full-width" v-model="correo" label="Correo" placeholder="CORREO" hint="Correo Electronico"  />
                          </div>
                      </div>
                      <div class="row">
                         <div class="col-12">
                            <q-card class="full-width q-mt-lg">
                                <div class="q-gutter-sm ">
                                  <q-radio v-model="sexo" val="Masculino" label="MASCULINO" />
                                  <q-radio v-model="sexo" val="Femenino" label="FEMENINO" />
                                </div>
                            </q-card>
                          </div>
                      </div>
                      
                </div>
                 <div class="col-2 q-gutter-sm">
                   <div class="row justify-center">
                 <div class="col-12">
                    <q-card style="q-pb-md full-width">
                        <div class="q-pa-md q-gutter-sm">
                        <q-img
                            :src= "url"
                            spinner-color="white"
                            style="height: 140px; max-width: 150px"
                          />
                        </div>
                    </q-card>
                    </div>
                    </div>
                    <div class="row justify-center">
                      <div class="col-12">
                        <q-btn  class="full-width" push color="teal" icon="photo_camera"   label="Buscar"  />
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
