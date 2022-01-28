<template>
   <q-page padding>
     <q-toolbar inset class="bg-primary text-white">
          <q-breadcrumbs active-color="white" style="font-size: 16px">
            <q-breadcrumbs-el label="Home" icon="home" />
            <q-breadcrumbs-el label="Components" icon="widgets" />
            <q-breadcrumbs-el label="Toolbar" />
          </q-breadcrumbs>
     </q-toolbar>
      <q-card >
        <q-card class="q-mt-md">
          <q-card-section class="q-pa-none">
            <q-card-section>
        <div class="text-h6 text-grey-8">
         Configuracion Terminal inventario quiniela
      </div>
      </q-card-section>
             <q-tabs
        v-model="tab"
        inline-label
        class="bg-indigo-10 text-white shadow-2"
         align="left"
      >
        <q-tab name="Quiniela" icon="receipt" label="Quiniela" />
        <q-tab name="tipo_jugada" icon="list" label="Tipo Jugada" />
        
      </q-tabs>
       <q-separator />

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="Quiniela">
             <q-table
         
          :data="quiniela"
          :columns="quiniela_columns"
          row-key="numero"
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
              

            </q-td>
          </template>


        </q-table>
          </q-tab-panel>

          <q-tab-panel name="tipo_jugada">
             <q-table
       
          :data="tipo_jugada"
          :columns="tipo_jugada_columns"
          row-key="tipo"
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

            </q-td>
          </template>


        </q-table>
          </q-tab-panel>
           </q-tab-panels>
          </q-card-section>
        </q-card>
       
      </q-card>
 
   </q-page>
</template>

<script>
export default {
  name: "busqueda-clientes",
  data() {
    return {
       tab: 'Quiniela',
       filter: "",
       show_filter: false,
       quiniela_columns:[{name: 'numero', label: 'NUMERO', field: 'numero', sortable: false, align: 'left'},
                    {name: 'valor_permitido', label: 'V. Permitido', field: 'valor_permitido', sortable: true, align: 'left'},
                    {name: 'Action', label: 'ACCIONES', field: 'Action', sortable: false, align: 'center'}
                    ],
      tipo_jugada_columns:[{name: 'tipo', label: 'TIPO JUGADA', field: 'tipo', sortable: false, align: 'left'},
                    {name: 'valor_permitido', label: 'V. Permitido', field: 'valor_permitido', sortable: true, align: 'left'},
                    {name: 'Action', label: 'ACCIONES', field: 'Action', sortable: false, align: 'center'}
                    ],
      quiniela: [
      {numero:'1', valor_permitido:'10',Action:''},
      {numero:'2', valor_permitido:'10',Action:''},
      {numero:'3', valor_permitido:'10',Action:''},
      {numero:'4', valor_permitido:'10',Action:''},
      {numero:'5', valor_permitido:'10',Action:''},
      {numero:'6', valor_permitido:'10',Action:''},
      {numero:'7', valor_permitido:'10',Action:''},
      {numero:'8', valor_permitido:'10',Action:''},
      {numero:'9', valor_permitido:'10',Action:''},
      ],
      tipo_jugada: [
      {tipo:'Quiniela', valor_permitido:'10',Action:''},
      {tipo:'Pale', valor_permitido:'10',Action:''},
      {tipo:'Tripleta', valor_permitido:'10',Action:''},
      {tipo:'Super Pale', valor_permitido:'10',Action:''}
      ]
    }
  },
    
    methods:{
        
    }
  }

</script>

