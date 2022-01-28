import { axiosInstance } from 'boot/axios'

export function fetchPhones(/* context */) {
  return axiosInstance.get('/telefono')
}

export function create(context, newTelefono) {
  return axiosInstance.post('/telefono', newClient)
}

export function remove(context, clientId) {
  return axiosInstance.delete(`/telefono/${clientId}`)
}

