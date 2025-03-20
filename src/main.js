import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router';
import { loadFonts } from './plugins/webfontloader'
const naive = create({
  components: [NButton]
})
import {
  // create naive ui
  create,
  // component
  NButton
} from 'naive-ui'

const app = createApp()
app.use(naive)

loadFonts()

createApp(App)
  .use(vuetify)
  .use(naive)
  .use(router)
  .mount('#app')
