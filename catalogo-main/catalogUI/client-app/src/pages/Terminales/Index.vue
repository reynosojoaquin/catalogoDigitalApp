<template>
  <q-page padding>
     <q-toolbar inset class="bg-primary text-white">
          <q-breadcrumbs active-color="white" style="font-size: 16px">
            <q-breadcrumbs-el label="Home" icon="home" />
            <q-breadcrumbs-el label="Components" icon="widgets" />
            <q-breadcrumbs-el label="Toolbar" />
          </q-breadcrumbs>
     </q-toolbar>
 

  <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6 text-grey-8">
         Indice Terminales
        <span class="float-right">
            <q-btn to="/Terminales/Create"  round color="primary" icon="smartphone"  />
        </span>
      </div>
      </q-card-section>
      <q-card-section class="q-pa-none">
        <q-table
          title="Busqueda"
          :data="data2"
          :columns="columns"
          row-key="name"
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
              <q-btn icon="edit" size="sm" flat dense/>
              <q-btn icon="delete" size="sm" class="q-ml-sm" flat dense/>
              <q-btn to="/Terminales/Configuracion" icon="app_settings_alt" size="sm" class="q-ml-sm" flat dense/>

            </q-td>
          </template>


        </q-table>
      </q-card-section>
  </q-card>


  </q-page>
</template>

<script>
export default {
 name: 'Index',
 data(){

    return {
       columns: [
                    {name: 'id', label: 'ID', field: 'id', sortable: true, align: 'left'},
                    {name: 'nombre', label: 'NOMBRE', field: 'nombre', sortable: true, align: 'left'},
                    {name: 'Action', label: 'ACCIONES', field: 'Action', sortable: false, align: 'center'}
                   
                ],
                 data2: [
                    {
                        id: '0001',
                        nombre: 'Banca la rapidita',
                        acciones: ''
                       
                    },
                    {
                        id: '0002',
                        nombre: 'banca la fortuna',
                        acciones: ''
                    }
                ],
                 filter: '',
                show_filter: false
    }
 }
}
</script>
<style scoped>
     .imgbtnsize{
       font-size: 1.900em;
     }
</style>