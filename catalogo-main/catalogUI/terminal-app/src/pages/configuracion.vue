<template>
  <q-page padding>
   <q-card class="q-pa-sm">
      <q-card-section>
        <span class="text-h5">Impresora</span>
      </q-card-section>
      <q-separator dark inset></q-separator>
      <q-field outlined label="ID" stack-label>
        <template v-slot:control>
          <div class="self-center full-width no-outline" tabindex="0">
            <div class="row q-gutter-sm text-h6">
              <div class="column col-10"><q-input  label="IMPRESORA" /></div>
              <div class="column col-1 flex flex-center">
                <q-btn round color="primary" icon="fas fa-search" />
              </div>
            </div>
          </div>
        </template>
      </q-field>
    </q-card>
     <q-page-sticky position="bottom-right" :offset="[14, 20]">
             <q-fab color="purple" icon="keyboard_arrow_up" direction="up">
        <q-fab-action color="secondary"  icon="far fa-save" />
      </q-fab>
    </q-page-sticky>
  </q-page>
</template>

<script>
export default {
  name: 'jugada'
}
</script>
