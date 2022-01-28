import { boot } from 'quasar/wrappers'
import createPersistedState from 'vuex-persistedstate'

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async ({app,router,store,Vue}) => {
  window.setTimeout(() => {
    createPersistedState()(store)
  }, 0)
})
