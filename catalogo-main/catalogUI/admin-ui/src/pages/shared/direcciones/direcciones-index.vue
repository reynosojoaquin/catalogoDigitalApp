<template>
  <q-page padding>
    <q-card>
      <q-card-section>
        <div class="text-h6 text-grey-8">
          Indice Direcciones
          <span class="float-right">
            <q-btn
              round
              color="primary"
              icon="add_location_alt"
              @click="createLocation()"
            />
          </span>
        </div>
      </q-card-section>
      <q-card-section class="q-pa-none">
        <q-table
          title="Busqueda"
          :rows="detailLocation"
          :columns="columns"
          row-key="id"
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

          <template v-slot:body-cell-action="props">
            <q-td :props="props">
              <div>
                <q-btn
                  icon="edit"
                  size="sm"
                  flat
                  dense
                  @click="editLocation(props.row.id)"
                />

                <q-btn
                  icon="delete"
                  size="sm"
                  class="q-ml-sm"
                  flat
                  dense
                  @click="removeLocation(props.row)"
                />
              </div>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
      <q-btn
        class="q-mt-sm q-mb-sm q-ml-sm"
        push
        color="accent"
        icon="cancel"
        label="Cancelar"
        @click="cancelar()"
      />
       <q-btn
        class="q-mt-sm q-mb-sm q-ml-sm"
        push
        color="blue-grey"
        icon="check_circle_outline"
        label="Aplicar"
        @click="aplicar()"
      />
    </q-card>
    <q-card class="q-mt-sm" v-show="ShowRegistrationModule">
      <LocationCreate
        :setLocation="currentLocation"
        :key="reCreateComponet"
        @getDireccion="getDireccionData"
      ></LocationCreate>
    </q-card>
  </q-page>
</template>

<script>
import LocationCreate from "../direcciones/direcciones-create";
import helpers from "../../../mixins/helpers.js";
import { createMemoryHistory } from 'vue-router';

export default {
  props: { setLocationsData:{type:Array, default: () => [] } },
  name: "Index",
  mixins: [helpers],
  components: {
    LocationCreate,
  },
  data() {
    return {
      columns: [
        {
          name: "tipo",
          label: "TIPO",
          field: "tipo",
          sortable: true,
          align: "left",
        },
        {
          name: "detalle",
          label: "DETALLE",
          field: "detalle",
          sortable: true,
          align: "left",
        },
        {
          name: "action",
          label: "ACCIONES",
          field: "action",
          sortable: false,
          align: "left",
        },
      ],
      direcciones: null,
      tempData:null,
      ciudades: [],
      sectores: [],
      tipoDireccion: [],
      provincias: [],
      filter: "",
      show_filter: false,
      ShowRegistrationModule: false,
      detailLocation: [
        ],
      reCreateComponet: 0,
      currentLocation: null,
      clienteID:null
    };
  },
   created() {
      console.log("MONTANDO EL INDICE DE DIRECCIONES");
      this.setup();
      if (this.tempData.length > 0) {
        this.showDetailLocation(this.tempData);
      }
    },
  methods: {
    getDireccionData(data) {
      if (data != null) {
        let objDireccion = JSON.parse(JSON.stringify(data));
        let description = { id: "", detalle: "", tipo: "" };
       
        description = this.createDetailLocation(data);
        let locationID = this.getMaxID(this.tempData, "id") + 1;
        console.log(locationID);
        let estado = this.$store.getters["Locations/getStateRegistro"];

        console.log(estado);

        if (estado == "editing") {
          this.direcciones.forEach(function (item, index, object) {
            if (item.id == data.id) {
              item.tipo_id = data.tipo_id;
              item.provincia_id = data.provincia_id;
              item.ciudad_id = data.ciudad_id;
              item.sector_id = data.sector_id;
              item.calle = data.calle;
              item.numero = data.numero;
              item.apartamento = data.apartamento;
              item.longitud = data.longitud;
              item.latitude = data.latitude;
              item.persona_id = data.persona_id
            }
          });

           this.detailLocation.forEach(function (item, index, object) {
            if (item.id == data.id) {
              item.tipo = description.tipo;
              item.detalle = description.detalle;
            }
          });
      
        } else if (estado == "creating") {
          description.id = locationID;
          objDireccion.id = 0;
          objDireccion.persona_id = this.clienteID;
          this.detailLocation.push(description);
          this.tempData.push(objDireccion);
         
        }

        this.ShowRegistrationModule = false;
      
      } else {
        this.ShowRegistrationModule = false;
       
      }
       this.$store.commit("Locations/SET_REGISTRO_STATE", "");
      this.$emit("getDirection", this.tempData);
    },
    aplicar(){
        this.direcciones = JSON.parse(JSON.stringify(this.tempData)); 
        this.$emit("getDirection", this.tempData);
    },
    forceRender() {
      this.reCreateComponet += 1;
    },
    cancelar() {
      this.$emit("getDirection", null);
    },
    removeLocation(data) {
      this.detailLocation.forEach(function (item, index, object) {
        if (item.id === data.id) {
          object.splice(index, 1);
        }
      });
      this.tempData.forEach(function (item, index, object) {
        if (item.id === data.id) {
          object.splice(index, 1);
        }
      });
    
    },
    editLocation(id) {
      this.$store.commit("Locations/SET_REGISTRO_STATE", "editing");
      let currentLocation = {
        id: null,
        tipo_id: null,
        provincia_id: null,
        ciudad_id: null,
        sector_id: null,
        calle: null,
        numero: null,
        apartamento: null,
        longitud: null,
        latitude: null,
        persona_id:null
      }
     
    
      this.tempData.forEach(function (item, index, object) {
        if (item.id == id) {
          currentLocation.id = id;
          (currentLocation.tipo_id = item.tipo_id),
            (currentLocation.provincia_id = item.provincia_id),
            (currentLocation.ciudad_id = item.ciudad_id),
            (currentLocation.sector_id = item.sector_id),
            (currentLocation.calle = item.calle),
            (currentLocation.numero = item.numero),
            (currentLocation.apartamento = item.apartamento),
            (currentLocation.longitud = item.longitud),
            (currentLocation.latitude = item.latitude),
            (currentLocation.persona_id = item.persona_id);
        }
      });
      this.currentLocation = JSON.stringify(currentLocation);
      this.ShowRegistrationModule = true;
  
    },
    showCreateLocationModule() {
      this.ShowRegistrationModule = true;
    },
    createLocation() {
      this.$store.commit("Locations/SET_REGISTRO_STATE", "creating");
      this.showCreateLocationModule();
    },
    createDetailLocation(data) {
      let description = { id: "", detalle: "", tipo: "" };
      let localCities = JSON.parse(JSON.stringify(this.ciudades));
      let localSectors = JSON.parse(JSON.stringify(this.sectores));
      let localLocationType = JSON.parse(JSON.stringify(this.tipoDireccion));
      let city = this.filtrarJson(localCities, "id", data.ciudad_id)[0];
      let sector = this.filtrarJson(localSectors, "id", data.sector_id)[0];
      let tipo = this.filtrarJson(localLocationType, "id", data.tipo_id)[0];
      description.detalle =
        city.Nombre +
        "," +
        sector.Nombre +
        ", " +
        data.calle +
        ", " +
        data.numero +
        " " +
        data.apartamento;
      description.tipo = tipo.Descripcion;
      return description;
    },
    showDetailLocation(data) {
      let i, id;
      for (i = 0; i < data.length; i++) {
        let description = { id: "", detalle: "", tipo: "" };
        description = this.createDetailLocation(data[i]);
        description.id = data[i].id;
        this.detailLocation.push(description);
      }
    },
    setup() {
      //CARGANDO DATOS DIRECCIONES
       this.provincias      =  JSON.parse(JSON.stringify(this.$store.getters["Locations/getProvincias"]))  
       this.ciudades        =  JSON.parse(JSON.stringify(this.$store.getters["Locations/getCiudades"]))
       this.sectores        =  JSON.parse(JSON.stringify(this.$store.getters["Locations/getSectores"]))
       this.tipoDireccion   =  JSON.parse(JSON.stringify(this.$store.getters["Locations/getTipoDirecciones"]))
       let objData          =  JSON.parse(JSON.stringify(this.$store.getters["clients/getCurrentClient"]))
        if (this.direcciones === null) {
            this.direcciones = objData.persona.direcciones
            this.tempData = JSON.parse(JSON.stringify(this.direcciones))
            this.clienteID = objData.id
        }
   
       //CARGANDO DATOS CONTACTOS

       
    },
  },
 
};
</script>
<style scoped>
.imgbtnsize {
  font-size: 1.9em;
}
</style>
