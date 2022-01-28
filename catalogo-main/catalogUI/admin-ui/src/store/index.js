import { createStore } from 'vuex'
import clients from '../store/Clients/index'
import Locations from '../store/Locations/index'
import Phones from '../store/Phones/index'
import Contacts from '../store/Contacts/index'
import createPersistedState from 'vuex-persistedstate'


export default function (/* { ssrContext } */) {
  const Store = createStore({
      modules: {
      clients,
      Locations, 
       Phones,
      Contacts,
    },
    Plugin: [new createPersistedState({
      storage: window.localStorage
    })],
    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: false
  })

  return Store
}
