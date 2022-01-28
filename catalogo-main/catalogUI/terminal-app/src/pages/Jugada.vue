<template>
  <q-page padding>
    <q-card>
      <q-card-section>
        <span class="text-h4 q-mr-lg ">Total</span>
        <span class="text-h2 ">27.00</span>
      </q-card-section>
    </q-card>
    <q-card bordered class="q-mt-sm jugada-container" >
      <q-card-section>
        <q-banner dense class="bg-primary text-white">
          <div class="row">
            <div class="text-h6 text-weight-bold   column col-4">
              <span>12</span>
              <span>Quiniela</span>
              <span>NA-T</span>
            </div>
            <div class="column flex flex-center col-4"><span class="text-h3">25.0</span></div>
            <div class=" flex flex-center column col-4">
              <q-btn size="30px" flat icon="fas fa-trash-alt" />
            </div>
          </div>
        </q-banner>
      </q-card-section>
    </q-card>
    <q-card class="q-mt-sm">
      <q-card-section >
        <div class="row q-gutter-sm text-h6">
       <div class="column col-2"> <q-input  label="1" /></div>
       <div class="column col-2"> <q-input  label="2" /></div>
       <div class="column col-2"><q-input   label="3" /></div>
       <div class="column col-2"><q-input  label="Monto" /></div>
       <div class="column flex flex-center">
         <q-toggle
         label="SP"
         left-label
      />
      </div>
       </div>
      </q-card-section>
    </q-card>
    <q-page-sticky position="bottom-right" :offset="[14, 120]">
             <q-fab color="purple" icon="keyboard_arrow_up" direction="up">
        <q-fab-action color="primary"  icon="fas fa-ban" />
        <q-fab-action color="secondary"  icon="far fa-file" />
        <q-fab-action color="primary"  icon="mail" />
        <q-fab-action color="secondary"  icon="fas fa-print" />
      </q-fab>
    </q-page-sticky>
  </q-page>
</template>
<script>
export default {
  name: 'jugada'
}
</script>
<style>
  .jugada-container{
    height: 390px;
  }
</style>
