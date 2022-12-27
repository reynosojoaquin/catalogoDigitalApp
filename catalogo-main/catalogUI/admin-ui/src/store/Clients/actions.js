import { axiosInstance } from 'boot/axios'


export function fetchClients(/* context */) {
  
  return   axiosInstance.get('/cliente')
}

export function create(context, newClient) {
  return axiosInstance.post('/cliente', newClient)
}

export function remove(context, clientId) {
  return axiosInstance.delete(`/cliente/${clientId}`)
}

export function put(context, client){
  return axiosInstance.put('/cliente',client)
}
