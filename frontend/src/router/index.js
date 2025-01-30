import Vue from 'vue'
import Router from 'vue-router'
import SelectSearchType from '@/components/SelectSearchType.vue'
import SearchEdit from '@/components/SearchEdit.vue'
import DirDec from '@/components/DirDec.vue'
import GenerateLetter from '@/components/GenerateLetter.vue' // Importar el nuevo componente
import ListadoPromocion from '@/components/ListadoPromocion.vue';

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/consultar',
      name: 'Consultar',
      component: SelectSearchType
    },
    {
      path: '/main/editar',
      name: 'Editar',
      component: SearchEdit
    },
    {
      path: '/main/direccion-decano',
      name: 'DirDec',
      component: DirDec
    },
    {
      path: '/main/generar-carta',
      name: 'GenerarCarta',
      component: GenerateLetter
    },
    {
      path: '/main/listado-promocion',
      name: 'ListadoPromocion',
      component: ListadoPromocion
    }
  ]
})
