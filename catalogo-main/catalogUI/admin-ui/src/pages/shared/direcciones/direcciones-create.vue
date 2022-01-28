<template>
  <q-page padding>
    <!-- content -->

    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6 text-grey-8">Nueva Direccion</div>
      </q-card-section>
      <q-separator></q-separator>
      <q-card-section class="q-mb-md">
        <q-form>
          <div class="row q-gutter-lg">
            <div class="col-11">
              <q-select
                v-model="direccion.tipo_id"
                :options="tipoDireccion"
                emit-value
                map-options
                option-value="id"
                option-label="Descripcion"
                label="Tipo Direccion"
              />
            </div>
          </div>
          <div class="row q-gutter-lg">
            <div class="col-11">
              <q-select
                v-model="provinciaID"
                :options="provincias"
                emit-value
                map-options
                option-value="id"
                option-label="Nombre"
                label="Provincia"
              />
            </div>
          </div>
          <div class="row q-gutter-lg">
            <div class="col-11">
              <q-select
                v-model="ciudadId"
                :options="ciudadesFiltered"
                emit-value
                map-options
                option-value="id"
                option-label="Nombre"
                label="Ciudad"
              />
            </div>
          </div>
          <div class="row q-gutter-lg">
            <div class="col-11">
              <q-select
                v-model="direccion.sector_id"
                :options="sectoresFiltered"
                emit-value
                map-options
                option-value="id"
                option-label="Nombre"
                label="Sector"
              />
            </div>
          </div>
          <div class="row q-gutter-lg">
            <div class="col-11">
              <q-input
                class="full-width"
                v-model="direccion.calle"
                label="Calle"
                placeholder="CALLE"
                hint="Calle de la Direccion"
              />
            </div>
          </div>

          <div class="row q-gutter-lg">
            <div class="col-11">
              <q-input
                class="full-width"
                v-model="direccion.numero"
                label="Numero"
                placeholder="NUMERO"
                hint="Numero de la direccion"
              />
            </div>
          </div>

          <div class="row q-gutter-lg">
            <div class="col-11">
              <q-input
                class="full-width"
                v-model="direccion.apartamento"
                label="Apartamento"
                placeholder="APARTAMENTO"
                hint="Apartamento de la direccion"
              />
            </div>
          </div>

          <div class="row q-mt-sm q-gutter-sm">
            <div class="col-1">
              <q-btn size="20px" round color="teal" icon="person_pin" />
            </div>
            <div class="col-5">
              <q-input
                class="full-width"
                v-model="direccion.longitud"
                label="Longitud"
                placeholder="LONGITUD"
                hint="Longitud Ubicacion"
              />
            </div>
            <div class="col-5">
              <q-input
                class="full-width"
                v-model="direccion.latitude"
                label="Latitude"
                placeholder="LATITUDE"
                hint="Latitude Ubicacion"
              />
            </div>
          </div>
        </q-form>
      </q-card-section>
      <q-separator></q-separator>
      <q-card-section class="q-mt-sm q-gutter-sm">
        <q-btn
          push
          color="teal"
          @click="setDireccion"
          icon="save"
          label="Registrar"
        />

        <q-btn
          push
          color="blue-grey"
          icon="gpp_bad"
          label="Cancelar"
          style="background: #ff0080"
          @click="cancelar"
        />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import helpers from '../../../mixins/helpers'
export default {
  props: { setLocation: { type: String, default: () => "" } },
  name: "direcciones-create",
 mixins:[helpers],
  data() {
    return {
      url: null,
      ciudadId: null,
      provinciaID: null,
      tipoDireccion: [],
      provincias: [],
      ciudades: [],
      sectores: [],
      ciudadesFiltered: [],
      sectoresFiltered: [],
      direccion: {
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
      },
    };
  },
    watch: {
      provinciaID: function(value,oldval){
           this.setProvinciaID(value)
      },

      ciudadId: function(value,oldValue){
          this.setCiudadID(value)
      }
  },
  methods: {
   
    setTipoDireccion(value) {},
    setProvinciaID(value) {
      this.ciudadesFiltered = this.filtrarJson(
        this.ciudades,
        "provincia_id",
        value
      );
      this.direccion.provincia_id = value;
      return
    },
    setCiudadID(value) {
      this.sectoresFiltered = this.filtrarJson(
        this.sectores,
        "ciudad_id",
        value
      );
      this.direccion.ciudad_id = value;
    },
    setDireccion() {
      console.log("direccion registered");
      /* console.log(JSON.stringify(this.direccion))*/
      this.$emit("getDireccion", this.direccion);
      this.direccion.provincia_id = null;
      this.direccion.ciudad_id = null;
      this.direccion.sector_id = null;
      this.direccion.calle = null;
      this.direccion.numero = null;
      this.direccion.apartamento = null;
      this.direccion.longitud = null;
      this.direccion.latitude = null;
      this.direccion.tipo_id = null;
      this.provinciaID = null;
   
    },
    cancelar() {
      this.$store.commit("Locations/SET_REGISTRO_STATE", "");
      this.$emit("getDireccion", null);
    },
    setup() {
       this.provincias      =  JSON.parse(JSON.stringify(this.$store.getters["Locations/getProvincias"]))  
       this.ciudades        =  JSON.parse(JSON.stringify(this.$store.getters["Locations/getCiudades"]))
       this.sectores        =  JSON.parse(JSON.stringify(this.$store.getters["Locations/getSectores"]))
       this.tipoDireccion   =  JSON.parse(JSON.stringify(this.$store.getters["Locations/getTipoDirecciones"]))
 
      
    },
  },
  mounted: function () {
    console.log('MONTANDO EL MODULO DE CREACION DE DIRECCIONES') 
     this.setup();
    if (this.setLocation !== null) {
      let estado = this.$store.getters["Locations/getStateRegistro"];
      if (estado == "editing") {
        this.direccion = JSON.parse(this.setLocation);
        this.provinciaID = this.direccion.provincia_id
        this.ciudadId    = this.direccion.ciudad_id
        this.ciudadesFiltered = this.ciudades;
        this.sectoresFiltered = this.sectores;
         console.log(JSON.stringify(this.direccion))
         

      }
    }
  },
};
</script>
<style lang="sass" scoped>
.flex-break
  flex: 1 0 100% !important
  width: 0 !important
</style>
