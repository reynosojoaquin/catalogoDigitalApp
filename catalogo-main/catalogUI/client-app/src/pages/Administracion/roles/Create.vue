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
             <div class="row ">
                <div class="col-12">
                 <q-card class="q-mt-md full-width">
                        <q-card-section>
                          <div class="text-h6 text-grey-8">
                          Permisos
                          </div>
                        </q-card-section>
                        <q-separator></q-separator>


                          <div class="q-pa-md q-gutter-sm">
                              <q-tree
                                :nodes="simple"
                                node-key="label"
                                class="full-width"
                                tick-strategy="leaf"
                               
                                />
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
        ph:null,
        simple: [
        {
          label: 'Permisos Globales',
          avatar: require('assets/baseline_local_police_black_48dp.png'),
          children: [
            {
              label: 'CONSORCIOS',
              icon: 'house_siding',
              children: [
                { label: 'Quality ingredients' },
                { label: 'Good recipe' }
              ]
            },
            {
              label: 'CLIENTES',
              icon: 'people_alt',
              disabled: false,
              children: [
                { label: 'Prompt attention' },
                { label: 'Professional waiter' }
              ]
            },
            {
              label: 'USUARIOS',
              icon: 'account_circle',
              children: [
                {
                  label: 'Happy atmosphere',
                  img: 'https://cdn.quasar.dev/img/logo_calendar_128px.png'
                },
                { label: 'Good table presentation' },
                { label: 'Pleasing decor' }
              ]
            },
             {
              label: 'ROLES',
              icon: 'admin_panel_settings',
              children: [
                {
                  label: 'Happy atmosphere (with image)',
                  img: 'https://cdn.quasar.dev/img/logo_calendar_128px.png'
                },
                { label: 'Good table presentation' },
                { label: 'Pleasing decor' }
              ]
            }
          ],
            ticked: [ 'Quality ingredients', 'Good table presentation' ],
        }
      ]
    } 
    
      
  }
   
}
</script>
