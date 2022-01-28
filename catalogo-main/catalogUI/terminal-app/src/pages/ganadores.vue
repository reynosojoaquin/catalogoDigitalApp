<template>
  <q-page padding>
    <q-card class="q-pa-sm">
      <q-card-section>
        <span class="text-h5">Numeros Ganadores</span>
      </q-card-section>
      <q-separator dark inset></q-separator>
      <q-field outlined label="Busqueda" stack-label>
        <template v-slot:control>
          <div class="self-center full-width no-outline" tabindex="0">
            <div class="row q-gutter-sm text-h6">
              <div class="column col-5"><q-select v-model="model" :options="options" label="Standard" /></div>
              <div class="column col-5">
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
              <div class="column col-1 flex flex-center">
                <q-btn round color="primary" icon="fas fa-search" />
              </div>
            </div>
          </div>
        </template>
      </q-field>
    </q-card>
    <div class="flex flex-center q-mt-lg">
      <div class="row">
        <div class="column col-12 flex flex-center"><span class="text-h3">LOTERIA</span></div>
        <div class="column col-12 flex flex-center "> <p class="text-h4 text-deep-purple-14">Loteka</p></div>
      </div>
  </div>
   <div class=" q-mt-lg">
      <div class="row ">
        <div class="column col-4 flex flex-center">
          <p class="text-h4 ">1</p>
          <p class="text-h3 text-blue-13">2</p>
        </div>
        <div class="column col-4 flex flex-center ">
          <p class="text-h4 ">2</p>
          <p class="text-h3 text-blue-13">5</p>
          </div>
         <div class="column col-4 flex flex-center ">
           <p class="text-h4 ">3</p>
           <p class="text-h3 text-blue-13">22</p>
           </div>
      </div>
  </div>
  </q-page>
</template>
<script>
export default {
  name: 'jugada',
  data () {
    return {
      model: null,
      options: ['Google', 'Facebook', 'Twitter', 'Apple', 'Oracle'],
      date: '2019/02/01'
    }
  }
}
</script>
