const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Dashboard.vue') },
      { path: 'dashboard', component: () => import('pages/Dashboard.vue') },
      { path: 'jugadas', component: () => import('pages/Jugada.vue') },
      { path: 'ganadores', component: () => import('pages/ganadores.vue') },
      { path: 'escanear', component: () => import('pages/escanear.vue') },
      { path: 'cuadre', component: () => import('pages/cuadre.vue') },
      { path: 'configuracion', component: () => import('pages/configuracion.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
