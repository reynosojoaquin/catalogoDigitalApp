<template>
  
      <q-card >
        <q-card class="q-mt-md">
          <q-card-section class="q-pa-none">
            <q-table
              title="Busqueda"
              :data="data2"
              :columns="columns"
              row-key="name"
              :filter="filter"
            >
              <template v-slot:top-right>
                <q-input
                  v-if="show_filter"
                  filled
                  borderless
                  dense
                  debounce="300"
                  v-model="filter"
                  placeholder="Search"
                >
                  <template v-slot:append>
                    <q-icon name="search" />
                  </template>
                </q-input>
                <q-btn
                  class="q-ml-sm"
                  icon="filter_list"
                  @click="show_filter = !show_filter"
                  flat
                />
              </template>

              <template v-slot:body-cell-Action="props">
                <q-td :props="props">
                  <q-btn
                    icon="done_outline"
                    size="sm"
                    class="q-ml-sm"
                    flat
                    dense
                    @click="onOKClick"
                  />
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
        <q-card-actions align="right">
          <q-btn color="primary" label="Cancel" @click="onCancelClick" />
        </q-card-actions>
      </q-card>
 

</template>

<script>
export default {
  name: "clientes-busqueda",
  data() {
    return {
      columns: [
        { name: "id", label: "ID", field: "id", sortable: true, align: "left" },
        {
          name: "nombre",
          label: "NOMBRE",
          field: "nombre",
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
      data2: [
        {
          id: "0001",
          nombre: "Joaquin Reynoso",
          acciones: ""
        },
        {
          id: "0002",
          nombre: "Chamel Reynoso",
          acciones: ""
        },
        {
          id: "0003",
          nombre: "Ismel Reynoso",
          acciones: ""
        },
        {
          id: "0004",
          nombre: "Patrick Morla",
          acciones: ""
        },
        {
          id: "0005",
          nombre: "Julian Felino",
          acciones: ""
        },
        {
          id: "0006",
          nombre: "Yoskar ariel",
          acciones: ""
        },
        {
          id: "0007",
          nombre: "Ariel Kelly",
          acciones: ""
        },
        {
          id: "0008",
          nombre: "Miguel angel valerio",
          acciones: ""
        },
        {
          id: "0009",
          nombre: "Bruno mars",
          acciones: ""
        },
        {
          id: "00010",
          nombre: "Juan luis  guerra",
          acciones: ""
        }
      ],
      filter: "",
      show_filter: false
    }
  },
    
    methods:{
         show () {
           this.$refs.dialog.show()
        },

          // following method is REQUIRED
          // (don't change its name --> "hide")
          hide(){
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
          }
    }
  }

</script>

