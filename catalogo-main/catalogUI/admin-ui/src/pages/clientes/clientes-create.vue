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
          Nuevo cliente
        </div>
      </q-card-section>
      <q-separator></q-separator>
      <q-card-section class="q-mb-md">
        <q-form @submit.prevent="client.id ? update() : create()">
          <div class="row q-gutter-lg ">
            <div class="col-9 ">
              <div class="row">
                <div class="col-12">
                  <q-input
                    class="full-width"
                    v-model="client.nombres"
                    label="Nombre"
                    placeholder="NOMBRE"
                    hint="Nombre Cliente"
                    :rules="required"
                    lazy-rules
                  />
                </div>
              </div>
              <div class="row">
                <div class="col-12">
                  <q-input
                    class="full-width"
                    v-model="client.apellidos"
                    label="Apellido"
                    placeholder="APELLIDO"
                    hint="Apellido Cliente"
                    :rules="required"
                    lazy-rules
                  />
                </div>
              </div>
              <div class="row">
                <div class="col-12">
                  <q-input
                    class="full-width"
                    v-model="client.cedula"
                    label="Cedula"
                    placeholder="CEDULA"
                    hint="Numero de cedula"
                    mask="###-#######-#"
                    :rules="required"
                    lazy-rules
                  />
                </div>
              </div>
              <div class="row">
                <div class="col-12">
                  <q-input
                    class="full-width"
                    v-model="client.correo"
                    label="Correo"
                    placeholder="CORREO"
                    hint="Correo Electronico"
                    type="email"
                    :rules="email"
                  />
                </div>
              </div>
              <div class="row">
                <div class="col-12">
                  <q-card class="full-width q-mt-lg">
                    <div class="q-gutter-sm ">
                      <q-radio
                        v-model="client.sexo"
                        val="masculino"
                        label="MASCULINO"
                      />
                      <q-radio
                        v-model="client.sexo"
                        val="femenino"
                        label="FEMENINO"
                      />
                      <q-radio
                        v-model="client.sexo"
                        val="undefined"
                        label="INDEFINIDO"
                      />
                    </div>
                  </q-card>
                </div>
              </div>
            </div>
            <div class="col-2 q-gutter-sm">
              <div class="row justify-center">
                
                  <q-card style="flex item-center justify-center centers  full-width">
                    <div class=" full-width " id="preview">
                      <q-img
                        v-if="client.url"
                        :src="client.url"
                        spinner-color="white"
                        style="height: 90%; max-width: 90%"
                      />
                    </div>
                  
                  </q-card>
                
              </div>
              <div class="row justify-center">
                <div class="col-12 row justify-center">
                 
                      <input
                        type="file"
                        name="file-1"
                        id="file-1"
                        class="inputfile inputfile-1"
                        @change="onFileChange"
                        
                      />
                      <label for="file-1">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          class="iborrainputfile"
                          width="50"
                          height="500"
                          viewBox="0 0 20 25"
                        >
                          <path
                            d="M0 0h24v24H0z" fill="none"/><circle cx="40" cy="40" r="3.2"/><path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"
                          ></path>
                        </svg>
                        <span class="iborrainputfile">Imagen</span>
                      </label>
                    
                </div>
              </div>
            </div>
          </div>
          <div class="row ">
            <div class="col-12">
              <q-card class="full-width q-mt-lg q-mb-lg">
                <div
                  class=" flex item-center justify-center centers q-pa-sm items-center  q-gutter-sm "
                >
                  <q-btn
                    color="orange-10"
                    text-color="white"
                    label="Direccion"
                    icon="room"
                    @click="selectArea('direccion')"
                  />
                  <q-btn
                    color="indigo-10"
                    label="Telefono"
                    icon="local_phone"
                    @click="selectArea('telefono')"
                  />
                  <q-btn
                    color="black"
                    label="Contacto"
                    icon="contacts"
                    @click="selectArea('contacto')"
                  />
                </div>
              </q-card>
               <q-card v-show="showRegisterArea">
                        <q-card v-show="IndexDireccion">
                          <direcciones_index  
                                :setLocationsData ="client.direcciones"
                                :key="reCreateIndexLocation"
                                @getDirection="getDireccionData"                                     
                          ></direcciones_index>
                        </q-card>
                        <q-card v-show="IndexTelefono">
                          <telefonos_index
                                :setTelefonosData ="client.telefonos"
                                :key="reCreateIndexTelefonos"
                                @getTelefono="getTelefonoData"
                          ></telefonos_index>
                        </q-card>
                        <q-card v-show="IndexContacto">
                          <contactos_index 
                           :setContactosData ="client.contactos" 
                           :key="reCreateIndexContacto"
                          @getContacto="getContactoData"></contactos_index>
                        </q-card>
                  
              </q-card>
            </div>
          </div>
          <div class="row q-mt-md">
            <div class="col-12  q-gutter-sm">
              <q-btn
                :loading="loding"
                type="submit"
                push
                color="teal"
                icon="save"
                label="Registrar"
              />
              <q-btn
                :loading="loding"
                push
                color="blue-grey"
                icon="gpp_bad"
                label="Cancelar"
                to="/Clientes/index"
              />
            </div>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
   
  </q-page>
</template>

<script>
import direcciones_index from "../shared/direcciones/direcciones-index";
import contactos_index from "../shared/contactos/contactos-index";
import telefonos_index from "../shared/telefonos/telefonos-index";
import FormRules from "src/mixins/FormRules";



export default {
  name: "pageCreateclient",
  mixins: [FormRules],
  components: { 
                direcciones_index,
                telefonos_index, 
                contactos_index,
              },
    data() {
    return {
      client: {
        id: null,
        nombres: null,
        apellidos: null,
        cedula: null,
        estado: 1,
        correo: null,
        sexo: null,
        url: null,
        telefonos: new Array,
        direcciones: new Array,
        contactos: new Array
      },
      loding: false,
      showRegisterArea: false,
      registerPhome: false,
      registerLocation: false,
      registerContact: false,
      IndexDireccion : false,
      IndexTelefono : false,
      IndexContacto : false,
      editing:false,
      registrationModule: false,
      reCreateIndexLocation:0,
      reCreateIndexTelefonos:0,
      reCreateIndexContacto:0,
      currentClient: null
    };
  },
  methods: {
    create() {
       console.log('REGISTRANDO  CLIENTE')
         this.loding = true;
         this.$store
          .dispatch("clients/create", this.client)
          .then(response => {
            this.$q.notify({
              type: "positive",
              position: "top",
              message: "Cliente creado satisfactoriamente"
            });
            this.$router.push("/clientes/index");
          })
          .catch(error => {
            console.log(error);
             this.$q.notify({
              type: "negative",
              position: "top",
              message: "Error al crear el cliente"
            });
          })
          .finally(() => {
            this.loding = false;
          });
     
    },
    update(){
      console.log('MODIFICANDO   CLIENTE')
        console.log(JSON.stringify(this.client))
        this.loding = true;
         this.$store
          .dispatch("clients/put", this.client)
          .then(response => {
            this.$q.notify({
              type: "positive",
              position: "top",
              message: "Cliente Modificado con exito"
            });
            this.$router.push("/clientes/index");
          })
          .catch(error => {
            console.log(error);
            
          })
          .finally(() => {
            this.loding = false;
          });
    },
    selectArea(value) {
      
          this.IndexDireccion = false;
          this.IndexTelefono = false;
          this.IndexContacto = false;
        switch (value) {
        case "direccion":
          this.IndexDireccion = true;
          break;
        case "telefono":
          this.IndexTelefono = true;
          break;
        case "contacto":
          this.IndexContacto = true;
          break;
         }
      this.showRegisterArea = true;
    },
    getDireccionData(data) {
      if (data != null) {
          console.log('ASIGNANDO DATOS DE LA DIRECCION AL CLIENTE')
          this.client.direcciones = JSON.parse(JSON.stringify(data));;
          console.log(JSON.stringify(this.client.direcciones))
       } 
        this.showRegisterArea = false;
    },

    getTelefonoData(data) {
      if (data != null) {
        let objtelefono = JSON.parse(JSON.stringify(data));
        this.client.telefonos = objtelefono;
        this.showRegisterArea = false;
      } else {
        this.showRegisterArea = false;
      }
    },
    getContactoData(data) {
        console.log('ASiGNANDO DATOS CONTACTOS AL CLIENTE')
      if (data != null) {
        let objContacto = JSON.parse(JSON.stringify(data));
        console.log(JSON.stringify(objContacto))
        this.client.contactos = objContacto;
        this.showRegisterArea = false;
      } else {
        this.showRegisterArea = false;
      }
    },
    cancelar() {
      console.log("cancelado");
    },
    onFileChange(e) {
      const file = e.target.files[0];
      this.client.url = URL.createObjectURL(file);
    },
     showRegistrationModule(value) {
      
          this.IndexDireccion = false;
          this.IndexTelefono = false;
          this.IndexContacto = false;
        switch (value) {
        case "direccion":
           this.IndexDireccion = true;
           this.forceReCreateIndexLocation()
          break;
        case "telefono":
          this.IndexTelefono = true;
          break;
        case "contacto":
          this.IndexContacto = true;
          break;
         }
      this.showRegisterArea = true;
    },
    forceReCreateIndexLocation(){
      this.reCreateIndexLocation += 1
    
    },
     forceReCreateIndexTelefono(){
      this.reCreateIndexTelefonos += 1
    },
    forceRecreateIndexContact(){
      this.reCreateIndexContacto += 1
    },
    
    setup()
    {
       
    }
 },created(){

     console.log('INICIANDO EL REGISTRO DE CLIENTES')
    const clientId = this.$route.params.id;
    if (clientId) {
           this.currentClient = JSON.parse(JSON.stringify(this.$store.getters['clients/getClients'].filter(client => client.id == clientId)[0]));
           this.$store.commit("clients/SET_CURRENT_CLIENT",this.currentClient);
           this.client = this.currentClient.persona;
           this.editing = true
       }
    this.setup()
  }
};
</script>
<style>
#preview {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height:200px;
  min-width: 150px;
}

#preview img {
  max-width: 100%;
  max-height: 500px;
}



.container-input {
    text-align: center;
    background: #282828;
    border-top: 5px solid #c39f77;
    padding: 50px 0;
    border-radius: 6px;
    width: 50%;
    margin: 0 auto;
    margin-bottom: 20px;
}

.inputfile {
    width: 0.1px;
    height: 0.1px;
    opacity: 0;
    overflow: hidden;
    position: absolute;
    z-index: -1;
    

}

.inputfile + label {
    max-width: 80%;
    font-size: 0.25rem;
    font-weight: 700;
    text-overflow: ellipsis;
    white-space: nowrap;
    cursor: pointer;
    display: inline-block;
    overflow: hidden;
    padding: 0.325rem 0.90rem;
}

.inputfile + label svg {
    width: 1.5em;
    height: 1.5em;
    vertical-align: middle;
    fill: currentColor;
    margin-top: -0.25em;
    margin-right: 0.25em;
}

.iborrainputfile {
	font-size:13px; 
	font-weight:normal;
	font-family: 'Lato';
}

/* style 1 */

.inputfile-1 + label {
    color: #fff;
    background-color: #536941;
    border-radius: 8px;
    
}

.inputfile-1:focus + label,
.inputfile-1.has-focus + label,
.inputfile-1 + label:hover {
    background-color: #e9e6e3;
}

</style>
