import { axiosInstance } from 'boot/axios'

export function fetchLocations(/* context */) {
  return axiosInstance.get('/Direccion')
}

export function create(context, newClient) {
  return axiosInstance.post('/Direccion', newClient)
}

export function remove(context, clientId) {
  return axiosInstance.delete(`/Direccion/${clientId}`)
}

export function fetchLocationsType(){
  return axiosInstance.get('/tipoDireccion')
}

export function fetchProvincias(){
  return axiosInstance.get('/provincia')
}

export function fetchCiudades(){
  return axiosInstance.get('/ciudad')
}

export function fetchSectores(){
  return axiosInstance.get('/sector')
}