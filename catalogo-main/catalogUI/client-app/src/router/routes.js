const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/Dashboard/Dashboard.vue')},
      {path: '/Bancas', component: () => import('pages/Bancas/index.vue')},
      {path: '/Bancas/index', component: () => import('pages/Bancas/index.vue')},
      {path: '/Bancas/Create', component: () => import('pages/Bancas/Create.vue')},
      {path: '/Bancas/Configuracion', component: () => import('pages/Bancas/Configuracion.vue')},
      {path: '/Bancas/Consultas', component: () => import('pages/Bancas/Consultas.vue')},
      {path: '/Bancas/Vendedores/index', component: () => import('pages/Bancas/Vendedores/index.vue')},
      {path: '/Bancas/Vendedores/Create', component: () => import('pages/Bancas/Vendedores/Create.vue')},


      {path: '/Terminales/index', component: () => import('pages/Terminales/index.vue')},
      {path: '/Terminales/create', component: () => import('pages/Terminales/Create.vue')},
      {path: '/Terminales/Configuracion', component: () => import('pages/Terminales/Configuracion.vue')},
      {path: '/usuarios/index', component: () => import('pages/Administracion/usuarios/index.vue')},
      {path: '/usuarios/create', component: () => import('pages/Administracion/usuarios/create.vue')},
      {path: '/roles/index', component: () => import('pages/Administracion/roles/index.vue')},
      {path: '/roles/create', component: () => import('pages/Administracion/roles/create.vue')},
      {path: '/telefonos/index', component: () => import('pages/shared/Telefonos/index.vue')},
      {path: '/telefonos/create', component: () => import('pages/shared/Telefonos/Create.vue')},
      {path: '/direcciones/index', component: () => import('pages/shared/Direcciones/index.vue')},
      {path: '/direcciones/create', component: () => import('pages/shared/Direcciones/create.vue')}
     
    ]
  },
  {
    path: '/Lock',
    component: () => import('pages/LockScreen.vue')
  },
  {
    path: '/Maintenance',
    component: () => import('pages/Maintenance.vue')
  },
  {
    path: '/Pricing',
    component: () => import('pages/Pricing.vue')
  },
  {
    path: '/Login-1',
    component: () => import('pages/Login-1.vue')
  },
  {
    path: '/Mail',
    component: () => import('layouts/Mail.vue')
  },
  {
    path: '/Lock-2',
    component: () => import('pages/LockScreen-2.vue')
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
