<template>
  <q-page padding>
    <!-- content -->

    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6 text-grey-8">Nuevo telefono</div>
      </q-card-section>
      <q-separator></q-separator>
      <q-card-section class="q-mb-md">
        <q-form>
          <div class="row">
            <div class="col-12">
              <q-select
                v-model="telefono.tipo_id" 
                :options="tipoTelefono"
                emit-value
                map-options
                option-value="id"
                option-label="label"
                label="Tipo Telefono"
              />
            </div>
          </div>
          <div class="row q-gutter-lg">
            <div class="col-11">
              <q-input
                class="full-width"
                v-model="telefono.numero"
                label="Telefono"
                placeholder="TELEFONO"
                hint="Numero de telefono"
                mask="(###)-###-####"
              />
            </div>
          </div>
        </q-form>
      </q-card-section>
      <q-separator></q-separator>
      <q-card-section class="q-gutter-md">
        <q-btn
          push
          color="teal"
          icon="save"
          label="Registrar"
          @click="setTelefono"
        />
        <q-btn
          push
          color="blue-grey"
          icon="gpp_bad"
          label="Cancelar"
          @click="cancelar"
        />
      </q-card-section></q-card>
  </q-page>
</template>

<script>
import FormRules from "src/mixins/FormRules";

export default {
  name: "telefonos-create",
  mixins: [FormRules],
  data() {
    return {
           tipoTelefono:[{label:'Residencial',id:1},
                              {label:'Celular',id:2},
                              {label:'Trabajo',id:3}],
      model: null,
      telefono: {
        tipo_id: null,
        numero: null,
      },
    };
  },
  created: function () {
    console.log("REGISTRO TELEFONOS MOUNTED");
    let stateRegister = this.$store.getters["Phones/getStateRegistro"];
    if (stateRegister == "editing") {
      let currentPhone = this.$store.getters["Phones/getCurrentPhone"];
      this.telefono = JSON.parse(JSON.stringify(currentPhone));
     
    }
  },
  methods: {
   cancelar() {
      console.log("cancelando telefono....");
      this.$store.commit("Phones/SET_REGISTRO_STATE", "");
      this.$emit("getTelefono", null);
    },
    setTelefono() {
      this.$emit("getTelefono", this.telefono);
      this.telefono.tipo = null;
      this.telefono.numero = null;
    }
  },
};
</script>
