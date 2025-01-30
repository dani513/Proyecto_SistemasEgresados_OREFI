import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router';
import WelcomePage from './components/WelcomePage.vue';
import UserLogin from './components/UserLogin.vue';
import MainView from './components/MainView.vue';
import AddGraduate from './components/AddGraduate.vue';
import ConsultGraduate from './components/ConsultGraduate.vue';
import SearchEdit from './components/SearchEdit.vue';
import DirDec from './components/DirDec.vue';
import GenerateLetter from './components/GenerateLetter.vue'; // Importar el nuevo componente
import ListadoPromocion from './components/ListadoPromocion.vue'; // Importar el nuevo componente

Vue.config.productionTip = false;

Vue.use(VueRouter);

const routes = [
  { path: '/', component: WelcomePage },
  { path: '/login', component: UserLogin },
  { 
    path: '/main', 
    component: MainView,
    children: [
      { path: 'agregar', component: AddGraduate },
      { path: 'consultar', component: ConsultGraduate },
      { path: 'editar', component: SearchEdit }, 
      { path: 'direccion-decano', component: DirDec },
      { path: 'generar-carta', component: GenerateLetter },
      { path: 'listado-promocion', component: ListadoPromocion } // Añade la nueva ruta
      // Añade más rutas hijas según sea necesario
    ]
  }
];

const router = new VueRouter({
  routes
});

new Vue({
  render: h => h(App),
  router
}).$mount('#app');
