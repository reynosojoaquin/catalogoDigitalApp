<template>
 <q-page padding>
    <q-card class="q-pa-sm">
      <q-card-section>
        <span class="text-h5">Cierre de operaciones</span>
        <hr>
        <div class="q-mt-sm">
          <p class="text-h6">Nacional</p>
          <hr>
          <div class="row">
            <div class="column col-4">
              <div class="col"><p>Quiniela</p></div>
            </div>
            <div class="column col-4">
                <div class="col"><p>3</p></div>
            </div>
            <div class="column col-4 item-end">
              <div class="col"><p class="text-subtitle2 float-right">$200.00</p></div>
            </div>
          </div>
          <div class="row">
            <div class="column col-4">
              <div class="col"><p>Pale</p></div>
            </div>
            <div class="column col-4">
                <div class="col"><p>3</p></div>
            </div>
            <div class="column col-4 item-end">
              <div class="col"><p class="text-subtitle2 float-right">$400.00</p></div>
            </div>
          </div><div class="row">
            <div class="column col-4">
              <div class="col"><p>Tripleta</p></div>
            </div>
            <div class="column col-4">
                <div class="col"><p>3</p></div>
            </div>
            <div class="column col-4 item-end">
              <div class="col"><p class="text-subtitle2 float-right">$600.00</p></div>
            </div>
          </div>
          <div class="row">
            <div class="column col-4">
              <div class="col"><p>S. Pale</p></div>
            </div>
            <div class="column col-4">
                <div class="col"><p>3</p></div>
            </div>
            <div class="column col-4 item-end">
              <div class="col"><p class="text-subtitle2 float-right">$800.00</p></div>
            </div>
          </div>
          <hr>
          <div class="row">
               <div class="column col-6">
                   <div class="col"><p class=" text-h6 ">Total</p></div>
               </div>
               <div class="column col-6 ">
                 <div class="col "><p class="float-right text-h6">$5000</p></div>
              </div>
          </div>
        </div>
      </q-card-section>
      <q-separator dark inset></q-separator>
    </q-card>
    <q-card  class="q-mt-sm q-pa-sm bg-yellow-1">
      <div class="row ">
            <div class="column text-h6 col-4">
              <div class="col"><p>Total General</p></div>
            </div>
            <div class="column col-4 flex flex-center">
              <div class="col"><p class="border-line q-mt-md q-ml-sm"></p></div>
            </div>
             <div class="column col-4 item-end">
              <div class="col"><p class="float-right text-h6">$664.00</p></div>
            </div>
      </div>
      <div class="row ">
            <div class="column text-h6 col-4">
              <div class="col"><p>Quiniela</p></div>
            </div>
            <div class="column col-4 flex flex-center">
              <div class="col"><p class="border-line q-mt-md q-ml-sm"></p></div>
            </div>
             <div class="column col-4 item-end">
              <div class="col"><p class="float-right text-h6">$4.00</p></div>
            </div>
      </div><div class="row ">
            <div class="column text-h6 col-4">
              <div class="col"><p>Pale</p></div>
            </div>
            <div class="column col-4 flex flex-center">
              <div class="col"><p class="border-line q-mt-md q-ml-sm"></p></div>
            </div>
             <div class="column col-4 item-end">
              <div class="col"><p class="float-right text-h6">$64.00</p></div>
            </div>
      </div><div class="row ">
            <div class="column text-h6 col-4">
              <div class="col"><p>Tripleta</p></div>
            </div>
            <div class="column col-4 flex flex-center">
              <div class="col"><p class="border-line q-mt-md q-ml-sm"></p></div>
            </div>
             <div class="column col-4 item-end">
              <div class="col"><p class="float-right text-h6">$50.00</p></div>
            </div>
      </div><div class="row ">
            <div class="column text-h6 col-4">
              <div class="col"><p>S. Pale</p></div>
            </div>
            <div class="column col-4 flex flex-center">
              <div class="col"><p class="border-line q-mt-md q-ml-sm"></p></div>
            </div>
             <div class="column col-4 item-end">
              <div class="col"><p class="float-right text-h6">$20.00</p></div>
            </div>
      </div>
      <div class="row flex flex-center">
        <div class="column items-center">
          <div class="col text-h6">
            <p>Numero de tickets emitidos 20</p>
          </div>
        </div>
      </div>
    </q-card>
    <q-page-sticky position="bottom-right" :offset="[14, 20]">
             <q-fab color="purple" icon="keyboard_arrow_up" direction="up">
        <q-fab-action color="secondary"  icon="far fa-save" />
        <q-fab-action color="primary"  icon="far fa-paper-plane" />
      </q-fab>
    </q-page-sticky>
  </q-page>
</template>
<script>
export default {
  name: 'jugada'
}
</script>
<style scoped>
.border-line
{

  border-style: dashed;
  min-width: 160px;
}
</style>
