<template>
  <div class="user-menu">
    <button @click="toggleMenu">{{ username }}</button>
    <div v-if="menuVisible" class="menu">
      <ul>
        <li @click="changePassword">Cambiar Contraseña</li>
        <li @click="logout">Cerrar Sesión</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserMenu',
  props: ['username'],
  data() {
    return {
      menuVisible: false
    }
  },
  methods: {
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
    changePassword() {
      // Lógica para cambiar la contraseña
      alert('Cambiar Contraseña');
    },
    logout() {
      // Lógica para cerrar sesión
      fetch('/api/logout', {
        method: 'POST'
      }).then(() => {
        this.$router.push('/login');
      });
    }
  }
}
</script>

<style scoped>
.user-menu {
  position: relative;
  display: inline-block;
}
button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
.menu {
  position: absolute;
  right: 0;
  top: 100%;
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.menu ul li {
  padding: 10px 20px;
  cursor: pointer;
}
.menu ul li:hover {
  background-color: #f0f0f0;
}
</style>
