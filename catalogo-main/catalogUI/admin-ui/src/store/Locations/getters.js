
export function getTelefono (state) {
  return state.direccion
}

export function getStateRegistro(state,getters){
  return state.registroState
}

export function getTipoDirecciones(state, getters){
  return state.tiposDirecciones
}

export function getProvincias(state, getters){
  return state.provincias
}
export function getCiudades(state, getters){
  return state.ciudades
}
export function getSectores(state, getters){
  return state.sectores
}
export function getStatusDatos(state, getters){
  return state.cargarDatos
}