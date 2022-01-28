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
          Clientes
          <span class="float-right">
            <q-btn
              to="/Clientes/Create"
              round
              color="primary"
              icon="person_add"
            />
          </span>
        </div>
      </q-card-section>
      <q-card-section class="q-pa-none">
        <q-table
          title="Busqueda"
          :rows="clients"
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
                @click="$router.push(`/clientes/edit/${props.row.id}`)"
                icon="edit"
                size="sm"
                flat
                dense
              />
              <q-btn
                @click="removeClient(props.row)"
                icon="delete"
                size="sm"
                class="q-ml-sm"
                flat
                dense
              />
              <q-btn
                to="/telefonos/index"
                icon="phone"
                size="sm"
                class="q-ml-sm"
                flat
                dense
              />
              <q-btn
                to="/direcciones/index"
                icon="place"
                size="sm"
                class="q-ml-sm"
                flat
                dense
              />
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import "es6-promise/auto";
export default {
  name: "Index",
  mounted() {
     this.loadClients();
     this.setup();
      
  },
  created() {
   
  },
  data() {
    return {
      columns: [
        {
          name: "id",
          label: "ID",
          field: "id",
          sortable: true,
          align: "left",
        },
        {
          name: "nombre",
          label: "NOMBRE",
          field: (row) => row.persona.nombres,
          sortable: true,
          align: "left",
        },
        {
          name: "Action",
          label: "ACCIONES",
          field: "Action",
          sortable: false,
          align: "center",
        },
      ],
      filter: "",
      show_filter: false,
      clients: [],
    };
  },
  methods: {
    removeClient(client) {
      const remove = window.confirm(
        "Esta seguro que desea eliminar este cliente ?"
      );
      if (remove) {
        const $store = useStore();
        $store
          .dispatch("clients/remove", client.id)
          .then((response) => {
            console.log(response);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    loadClients() {
      this.$store
        .dispatch("clients/fetchClients")
        .then((response) => {
          this.clients = response.data.data;
          this.$store.commit("clients/SET_CLIENTS", response.data.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    cargarLocalidades(){
     let cargarData = this.$store.getters["Locations/getStatusDatos"];
      console.log("Inicio carga de datos localidades");
      if (cargarData == true) {
        console.log("cargado datos localidades");
        //CARGANDO TIPO DE DIRECCIONES AL SISTEMA
        this.$store
          .dispatch("Locations/fetchLocationsType")
          .then((response) => {
            this.tipoDireccion = response.data.data;
            this.$store.commit(
              "Locations/SET_TIPO_DIRECCION",
              response.data.data
            );
          })
          .catch((error) => {
            console.log(error);
          });

        //CARGANDO PROVINCIAS AL SISTEMA

        this.$store
          .dispatch("Locations/fetchProvincias")
          .then((response) => {
            this.provincias = response.data.data;
            this.$store.commit("Locations/SET_PROVINCIAS", response.data.data);
           })
          .catch((error) => {
            console.log(error);
          });

        //CARGANDO CIUDADES AL SISTEMA

        this.$store
          .dispatch("Locations/fetchCiudades")
          .then((response) => {
            this.ciudades = response.data.data;
            this.$store.commit("Locations/SET_CIUDADES", response.data.data);
          })
          .catch((error) => {
            console.log(error);
          });

        //CARGANDO SECTORES AL SISTEMA

        this.$store
          .dispatch("Locations/fetchSectores")
          .then((response) => {
            this.$store.commit("Locations/SET_SECTORES", response.data.data);
          })
          .catch((error) => {
            console.log(error);
          });
        this.$store.commit("Locations/SET_STATUS_DATA", false);
      }
    },
    setup(){
            this.cargarLocalidades()
    }
  },
};
</script>
<style scoped>
.imgbtnsize {
  font-size: 1.9em;
}
</style>
