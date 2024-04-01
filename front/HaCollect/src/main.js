import { createApp } from 'vue'
import App from './App.vue'
import {router} from "./router"
import './index.css'
import { store } from './store.js'

var app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')