<template>
  <div class="main-view">
    <nav>
      <div class="logo-container">
        <img src="@/assets/logo1.png" alt="Logo" class="logo">
      </div>
      <ul>
        <li><router-link to="/main/agregar" class="nav-link">Agregar Graduando</router-link></li>
        <li><router-link to="/main/consultar" class="nav-link">Consultar Graduando</router-link></li>
        <li><router-link to="/main/editar" class="nav-link">Editar Egresado</router-link></li>
        <li><router-link to="/main/direccion-decano" class="nav-link">DIR_DEC</router-link></li>
        <li><router-link to="/main/generar-carta" class="nav-link">Generar Carta</router-link></li>
        <li><router-link to="/main/listado-promocion" class="nav-link">Listado Promoción</router-link></li>
      </ul>
      <div class="user-menu-container">
        <UserMenu :username="username"></UserMenu>
      </div>
    </nav>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import UserMenu from './UserMenu.vue';

export default {
  name: 'MainView',
  components: {
    UserMenu
  },
  data() {
    return {
      username: 'Usuario' // Cambia esto para obtener el nombre real del usuario desde el estado o API
    }
  },
  created() {
    // Aquí puedes obtener el nombre real del usuario desde la sesión o una API
    this.fetchUsername();
  },
  methods: {
    fetchUsername() {
      // Obtener el token desde localStorage
      const token = localStorage.getItem('token');

      // Incluir el token en los encabezados de la solicitud
      fetch('/api/get-username', {
        method: 'GET',
        headers: {
          'Authorization': token
        }
      })
        .then(response => response.json())
        .then(data => {
          this.username = data.username;
        });
    }
  }
}
</script>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  background: url('@/assets/background.jpg') no-repeat center center fixed; /* Imagen de fondo */
  background-size: cover; /* Asegura que la imagen cubra toda la pantalla */
}

.main-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

nav {
  background-color: rgba(0, 0, 102, 0.8); /* Color de fondo del nav */
  padding: 10px 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  margin-right: 20px; /* Separar un poco el logo del menú */
}

.logo {
  height: 70px; /* Tamaño del logo más grande */
}

nav ul {
  list-style-type: none;
  padding: 0;
  display: flex;
  align-items: center;
  margin: 0 auto; /* Centrar las opciones */
}

nav ul li {
  margin-right: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 16px;
  padding: 10px 15px;
  border-radius: 20px; /* Estilo de cápsula */
  background-color: #336699; /* Azul más claro */
  transition: background-color 0.3s, transform 0.3s;
}

.nav-link:hover {
  background-color: #5a9bd3;
  transform: translateY(-2px);
}

.user-menu-container {
  color: black; /* Texto en blanco */
  font-size: 16px; /* Tamaño del texto */
}

.content {
  padding: 20px;
  flex: 1;
  background: rgba(255, 255, 255, 0.8); /* Fondo semitransparente */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 20px;
}
</style>
