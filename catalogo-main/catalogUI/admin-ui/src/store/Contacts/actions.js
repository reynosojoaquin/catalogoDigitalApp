import { axiosInstance } from 'boot/axios'

export function fetchContacts(/* context */) {
  return axiosInstance.get('/contactos')
}

export function create(context, newConctato) {
  return axiosInstance.post('/contactos', newContacto)
}

export function remove(context, clientId) {
  return axiosInstance.delete(`/contacto/${clientId}`)
}

