const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/dashboard/dashboard.vue')},
      {path: '/clientes', component: () => import('pages/clientes/clientes-index.vue')},
      {path: '/clientes/index', component: () => import('pages/clientes/clientes-index.vue')},
      {path: '/clientes/create', component: () => import('pages/clientes/clientes-create.vue')},
      {path: '/clientes/edit/:id', component: () => import('pages/clientes/clientes-create.vue')},
      {path: '/consorcios/index', component: () => import('pages/consorcios/consorcios-index.vue')},
      {path: '/consorcios/create', component: () => import('pages/consorcios/consorcios-create.vue')},
      {path: '/usuarios/index', component: () => import('pages/administracion/usuarios/usuarios-index.vue')},
      {path: '/usuarios/create', component: () => import('pages/administracion/usuarios/usuarios-create.vue')},
      {path: '/roles/index', component: () => import('pages/administracion/roles/roles-index.vue')},
      {path: '/roles/create', component: () => import('pages/administracion/roles/roles-create.vue')},
      {path: '/telefonos/index', component: () => import('pages/shared/telefonos/telefonos-index.vue')},
      {path: '/telefonos/create', component: () => import('pages/shared/telefonos/telefonos-create.vue')},
      {path: '/direcciones/index', component: () => import('pages/shared/direcciones/direcciones-index.vue')},
      {path: '/contactos/create', component: () => import('pages/shared/contactos/contactos-create.vue')},
      {path: '/contactos/index', component: () => import('pages/shared/contactos/contactos-index.vue')},
      {path: '/direcciones/create', component: () => import('pages/shared/direcciones/direcciones-create.vue')}
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '/:catchAll(.*)',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
