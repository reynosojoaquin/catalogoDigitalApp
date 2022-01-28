<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          icon="menu"
          aria-label="Menu"
        />

        <q-toolbar-title>
          Lotery 2.0
        </q-toolbar-title>

        <q-space />

        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn
            round
            flat
            color="white"
            :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
            @click="$q.fullscreen.toggle()"
            v-if="$q.screen.gt.sm"
          >
            <!--            <q-tooltip>Messages</q-tooltip>-->
          </q-btn>
          <q-btn round flat color="white" icon="notifications">
            <q-badge color="red" text-color="white" floating>
              5
            </q-badge>
            <q-menu>
              <q-list style="min-width: 100px">
                <messages></messages>
                <q-card class="text-center no-shadow no-border">
                  <q-btn
                    label="View All"
                    style="max-width: 120px !important;"
                    flat
                    dense
                    class="text-indigo-8"
                  ></q-btn>
                </q-card>
              </q-list>
            </q-menu>
            <!--            <q-tooltip>Notifications</q-tooltip>-->
          </q-btn>
          <q-btn round flat>
            <q-avatar size="26px">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
            </q-avatar>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-primary text-white"
    >
      <q-list>
        <q-item to="/" active-class="q-item-no-link-highlighting">
          <q-item-section avatar>
            <q-icon name="dashboard" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Dashboard</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item icon="store" label="Bancas">
          <q-list class="q-pl-lg">
            <q-item
              to="/Bancas/index"
              active-class="q-item-no-link-highlighting"
            >
              <q-item-section avatar>
                <q-icon name="list_alt" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Index</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              to="/Bancas/Consultas"
              active-class="q-item-no-link-highlighting"
            >
              <q-item-section avatar>
                <q-icon name="find_in_page" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Consultas</q-item-label>
              </q-item-section>
            </q-item>

            <q-expansion-item icon= "fas fa-male" label="Vendedores">
              <q-list class="q-pl-lg">
                <q-item
                  to="/Bancas/Vendedores/index"
                  active-class="q-item-no-link-highlighting"
                 
                >
                  <q-item-section avatar>
                    <q-icon name="list_alt" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Index</q-item-label>
                  </q-item-section>
                </q-item>
                
              </q-list>
            </q-expansion-item>
          </q-list>
        </q-expansion-item>

        <q-expansion-item icon="settings" label="Administracion">
          <q-expansion-item
            icon="account_circle"
            label="Usuarios"
            :header-inset-level="0.6"
          >
            <q-item
              to="/usuarios/index"
              class="q-ml-xl"
              style="margin-left: 55px  !important;"
              active-class="q-item-no-link-highlighting"
            >
              <q-item-section avatar>
                <q-icon name="list_alt" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Index</q-item-label>
              </q-item-section>
            </q-item>
          </q-expansion-item>

          <q-expansion-item
            icon="admin_panel_settings"
            label="Roles"
            :header-inset-level="0.6"
          >
            <q-item
              to="/roles/index"
              class="q-ml-xl"
              style="margin-left: 55px  !important;"
              active-class="q-item-no-link-highlighting"
            >
              <q-item-section avatar>
                <q-icon name="list_alt" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Index</q-item-label>
              </q-item-section>
            </q-item>
          </q-expansion-item>
        </q-expansion-item>
      </q-list>
    </q-drawer>

    <q-page-container class="bg-grey-2">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import EssentialLink from "components/EssentialLink";
import Messages from "./Messages";

export default {
  name: "MainLayout",

  components: {
    Messages,
    EssentialLink
  },

  data() {
    return {
      leftDrawerOpen: false,
      iconVendorUrl: require('assets/shop-vendor.png') 
    };
  }
};
</script>
