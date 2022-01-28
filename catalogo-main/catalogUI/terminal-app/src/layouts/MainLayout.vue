<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Terminal App
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
    <q-card class="q-pt-sm q-pb-sm bg-primary text-white">
       <q-icon name="style" class="q-mr-md" style="font-size: 5em; " />
       <span style="font-size: 2.5em;">TERMINAL</span>
    </q-card>
      <q-list>
        <q-item-label
          header
          class="text-grey-8"
        >
          Menu principal
        </q-item-label>
        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import EssentialLink from 'components/EssentialLink.vue'

const linksData = [
  {
    title: 'DashBoard',
    caption: 'Dashboard',
    icon: 'insert_chart',
    link: 'dashboard'
  },
  {
    title: 'Realizar Jugada',
    caption: 'Realizar jugada',
    icon: 'store',
    link: 'jugadas'
  },
  {
    title: 'Numeros ganadores',
    caption: 'Numeros ganadores',
    icon: 'plus_one',
    link: 'ganadores'
  },
  {
    title: 'Escanear Jugada',
    caption: 'escanear jugada',
    icon: 'qr_code_scanner',
    link: 'escanear'
  },
  {
    title: 'Cuadre del dia',
    caption: 'Cuadre',
    icon: 'fas fa-calculator',
    link: 'cuadre'
  },
  {
    title: 'Configuracion',
    caption: 'Configuracion',
    icon: 'fas fa-tools',
    link: 'configuracion'
  },
  {
    title: 'Salir',
    caption: 'salir',
    icon: 'fas fa-door-open',
    link: 'https://awesome.quasar.dev'
  }
]

export default {
  name: 'MainLayout',
  components: { EssentialLink },
  data () {
    return {
      leftDrawerOpen: false,
      essentialLinks: linksData
    }
  }
}
</script>
