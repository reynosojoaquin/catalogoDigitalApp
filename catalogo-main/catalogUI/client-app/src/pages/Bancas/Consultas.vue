<template>
  <q-page padding>
    <q-toolbar inset class="bg-primary text-white q-mb-md">
      <q-breadcrumbs active-color="white" style="font-size: 16px">
        <q-breadcrumbs-el label="Home" icon="home" />
        <q-breadcrumbs-el label="Components" icon="widgets" />
        <q-breadcrumbs-el label="Toolbar" />
      </q-breadcrumbs>
    </q-toolbar>
    <q-card class=" q-mb-sm">
      <q-card-section>
        <div class="text-h6 text-grey-8">
          Consulta Bancas
        </div>
      </q-card-section>
    </q-card>
    <q-separator></q-separator>
    <q-card>
      <q-card-section>
        <div class="row  justify-between">
          <div class="col-3 column ">
            <q-select
              filled
              v-model="model"
              use-input
              input-debounce="0"
              label="Simple filter"
              :options="options"
              @filter="filterFn"
              
            >
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>
          <div class="col-3 column ">
            <q-select
              filled
              v-model="model"
              use-input
              input-debounce="0"
              label="Simple filter"
              :options="options"
              @filter="filterFn"
             
            >
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>
          <div class="col-3 column q-gutter-x-lg">
            <q-select
              filled
              v-model="model"
              use-input
              input-debounce="0"
              label="Simple filter"
              :options="options"
              @filter="filterFn"
             
            >
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>
          <div class="column  col-2 items-end">
            <q-btn round color="primary" icon="search" ></q-btn>
          </div>
        </div>
        <div class="row   q-mt-sm">
        <div class="column">
          <q-field outlined label="Rango de Fecha" class="full-width" stack-label>
           <template v-slot:control>
              <div class="self-center full-width no-outline" tabindex="0">
                     <div class="col-3 column ">
            <q-input filled v-model="date" mask="date" :rules="['date']">
                <template v-slot:append>
                   <q-icon name="event" class="cursor-pointer">
                     <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                      <q-date v-model="date">
                         <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Close" color="primary" flat />
                        </div>
                      </q-date>
                      </q-popup-proxy>
                    </q-icon>
                </template>
              </q-input>
          </div>
          <div class="col-3 column ">
             <q-input filled v-model="date" mask="date" :rules="['date']">
      <template v-slot:append>
        <q-icon name="event" class="cursor-pointer">
          <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
            <q-date v-model="date">
              <div class="row items-center justify-end">
                <q-btn v-close-popup label="Close" color="primary" flat />
              </div>
            </q-date>
          </q-popup-proxy>
        </q-icon>
      </template>
    </q-input>
          </div>
          <div class="col-3 column q-gutter-x-lg">
          
          </div>
          <div class="column  col-2 items-end">
           
          </div>

                
              </div>
           </template>
         </q-field>
          
          </div>   
        
     

        </div>
      </q-card-section>
    </q-card>
    <q-separator></q-separator>
    <q-card class="q-mt-md">
      <q-table
        :data="quiniela"
        :columns="quiniela_columns"
        row-key="numero"
        :filter="filter"
      >
        <template v-slot:body-cell-Action="props">
          <q-td :props="props">
            <q-btn icon="edit" size="sm" flat dense />
            <q-btn icon="delete" size="sm" class="q-ml-sm" flat dense />
          </q-td>
        </template>
      </q-table>
    </q-card>
  
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="row  ">
          <div class="col-4 column ">
              <div class="row ">
                  <div class="column col-6"><span class="text-h6"> Quiniela</span></h3></div>
                  <div class="column col-6"><span class="text-h6">0.00</span></div>
              </div>
              <div class="row ">
                <div class="column col-6"><span class="text-h6">Pale</span></div>
                  <div class="column col-6"><span class="text-h6">0.00</span></div>
              </div>
              <div class="row ">
                <div class="column col-6"><span class="text-h6">S.&nbsp;Pale</span></div>
                  <div class="column col-6"><span class="text-h6">0.00</span></div>
              </div>
              <div class="row ">
                <div class="column col-6"><span class="text-h6"> Tripleta</span></div>
                  <div class="column col-6"><span class="text-h6">0.00</span></div>
              </div>
          </div>
          <div class="col-4 column q-gutter-lg flex item-center justify-center centers ">
           
                  <div class="column col-6"><p  class="text-h2 accent"> Total</p></div>
                   <div class="column col-6"><span class="text-h2"> 0.00</span></div>
            
          </div>
          
        </div>
        </div>
        <div class="row"></div>
      </q-card-section>
    </q-card>
    </q-card>
  </q-page>
</template>

<script>
const stringOptions = [
  'Google', 'Facebook', 'Twitter', 'Apple', 'Oracle'
]

export default {
  name: "busqueda-clientes",
  data() {
    return {
       model: null,
      options: stringOptions,
      tab: "Quiniela",
      filter: "",
      show_filter: false,
      quiniela_columns: [
        {
          name: "numero",
          label: "NUMERO",
          field: "numero",
          sortable: false,
          align: "left"
        },
        {
          name: "valor_permitido",
          label: "V. Permitido",
          field: "valor_permitido",
          sortable: true,
          align: "left"
        },
        {
          name: "Action",
          label: "ACCIONES",
          field: "Action",
          sortable: false,
          align: "center"
        }
      ],
      tipo_jugada_columns: [
        {
          name: "tipo",
          label: "TIPO JUGADA",
          field: "tipo",
          sortable: false,
          align: "left"
        },
        {
          name: "valor_permitido",
          label: "V. Permitido",
          field: "valor_permitido",
          sortable: true,
          align: "left"
        },
        {
          name: "Action",
          label: "ACCIONES",
          field: "Action",
          sortable: false,
          align: "center"
        }
      ],
      quiniela: [
        { numero: "1", valor_permitido: "10", Action: "" },
        { numero: "2", valor_permitido: "10", Action: "" },
        { numero: "3", valor_permitido: "10", Action: "" },
        { numero: "4", valor_permitido: "10", Action: "" },
        { numero: "5", valor_permitido: "10", Action: "" },
        { numero: "6", valor_permitido: "10", Action: "" },
        { numero: "7", valor_permitido: "10", Action: "" },
        { numero: "8", valor_permitido: "10", Action: "" },
        { numero: "9", valor_permitido: "10", Action: "" }
      ],
      tipo_jugada: [
        { tipo: "Quiniela", valor_permitido: "10", Action: "" },
        { tipo: "Pale", valor_permitido: "10", Action: "" },
        { tipo: "Tripleta", valor_permitido: "10", Action: "" },
        { tipo: "Super Pale", valor_permitido: "10", Action: "" }
      ]
    };
  },

  methods: {
     filterFn (val, update) {
      if (val === '') {
        update(() => {
          this.options = stringOptions

          // with Quasar v1.7.4+
          // here you have access to "ref" which
          // is the Vue reference of the QSelect
        })
        return
      }

      update(() => {
        const needle = val.toLowerCase()
        this.options = stringOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
      })
    }
  
            }
            
}
</script>
<style scoped>
.customSize{
  max-width: 83% !important;
}

</style>